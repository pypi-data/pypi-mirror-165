# Copyright 2021 Acryl Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from asyncio import tasks
from datetime import datetime, timedelta
import os
import sys
import subprocess
import logging
import asyncio
from collections import deque
from typing import Optional
from acryl.executor.execution.sub_process_task_common import SubProcessTaskUtil
from acryl.executor.execution.task import Task
from acryl.executor.execution.task import TaskError
from acryl.executor.result.execution_result import Type
from acryl.executor.context.executor_context import ExecutorContext
from acryl.executor.context.execution_context import ExecutionContext
from acryl.executor.common.config import ConfigModel

logger = logging.getLogger(__name__)

class SubProcessIngestionTaskConfig(ConfigModel):
    tmp_dir: str = "/tmp/datahub/ingest"
    heartbeat_time_seconds: int = 2
    max_log_lines: int = SubProcessTaskUtil.MAX_LOG_LINES

class SubProcessIngestionTaskArgs(ConfigModel):
    recipe: str
    version: str = "latest"
    debug_mode: str = "false" # Expected values are "true" or "false". 

class SubProcessIngestionTask(Task):

    config: SubProcessIngestionTaskConfig
    tmp_dir: str # Location where tmp files will be written (recipes) 
    ctx: ExecutorContext

    @classmethod
    def create(cls, config: dict, ctx: ExecutorContext) -> "Task":
        return cls(SubProcessIngestionTaskConfig.parse_obj(config), ctx)

    def __init__(self, config: SubProcessIngestionTaskConfig, ctx: ExecutorContext):
        self.config = config
        self.tmp_dir = config.tmp_dir
        self.ctx = ctx 

    async def execute(self, args: dict, ctx: ExecutionContext) -> None:

        exec_id = ctx.exec_id # The unique execution id. 

        exec_out_dir = f"{self.tmp_dir}/{exec_id}"

        # 0. Validate arguments 
        validated_args = SubProcessIngestionTaskArgs.parse_obj(args)

        # 1. Resolve the recipe (combine it with others)
        recipe: dict = SubProcessTaskUtil._resolve_recipe(validated_args.recipe, ctx, self.ctx)

        # 2. Write recipe file to local FS (requires write permissions to /tmp directory)
        file_name: str = "recipe.yml"  
        SubProcessTaskUtil._write_recipe_to_file(exec_out_dir, file_name, recipe)

        # 3. Spin off subprocess to run the run_ingest.sh script
        datahub_version = validated_args.version # The version of DataHub CLI to use. 
        plugins = recipe["source"]["type"] # The source type -- ASSUMPTION ALERT: This should always correspond to the plugin name. 
        debug_mode = validated_args.debug_mode
        command_script: str = "run_ingest.sh" # TODO: Make sure this is EXECUTABLE before running

        stdout_lines: deque[str] = deque(maxlen=self.config.max_log_lines)
        full_log_file = open(f"{exec_out_dir}/ingestion_log.txt", "w")

        report_out_file = f"{exec_out_dir}/ingestion_report.json"

        logger.info(f'Starting ingestion subprocess for exec_id={exec_id} ({plugins})')
        ingest_process = await asyncio.create_subprocess_exec(
            *[command_script, exec_id, datahub_version, plugins, self.tmp_dir, f"{exec_out_dir}/recipe.yml", report_out_file, debug_mode],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        # 4. Monitor and report progress.
        most_recent_log_ts: Optional[datetime] = None

        async def _read_output_lines() -> None:
            while True:
                assert ingest_process.stdout
                line_bytes = await ingest_process.stdout.readline()
                if not line_bytes:
                    logger.info(f'Got EOF from subprocess exec_id={exec_id} - stopping log monitor')
                    break
                line = line_bytes.decode("utf-8")
                
                nonlocal most_recent_log_ts
                most_recent_log_ts = datetime.now()

                full_log_file.write(line)
                sys.stdout.write(line)
                sys.stdout.flush()
                stdout_lines.append(line)

                await asyncio.sleep(0)
        
        async def _report_progress() -> None:
            while True:
                if ingest_process.returncode is not None:
                    logger.info(f'Detected subprocess return code exec_id={exec_id} - stopping logs reporting')
                    break

                await asyncio.sleep(self.config.heartbeat_time_seconds)

                # Report progress
                if ctx.request.progress_callback:
                    if most_recent_log_ts is None:
                        report = 'No logs yet'
                    else:
                        report = SubProcessTaskUtil._format_log_lines(stdout_lines)
                        current_time = datetime.now()
                        if most_recent_log_ts < current_time - timedelta(minutes=2):
                            message = f'WARNING: These logs appear to be stale. No new logs have been received since {most_recent_log_ts} ({(current_time - most_recent_log_ts).seconds} seconds ago). ' \
                                "However, the ingestion process still appears to be running and may complete normally."
                            report = f'{report}\n\n{message}'

                    # TODO maybe use the normal report field here?
                    ctx.request.progress_callback(report)

                full_log_file.flush()
                await asyncio.sleep(0)
        
        async def _process_waiter() -> None:
            await ingest_process.wait()
            logger.info(f'Detected subprocess exited exec_id={exec_id}')
        
        try: 
            await tasks.gather(_read_output_lines(), _report_progress(), _process_waiter())
        except asyncio.CancelledError:
            # Terminate the running child process 
            ingest_process.terminate()
            raise
        finally:
            full_log_file.close()

            if os.path.exists(report_out_file):
                with open(report_out_file,'r') as structured_report_fp:
                    ctx.get_report().set_structured_report(structured_report_fp.read())

            ctx.get_report().report_info(f"stdout={SubProcessTaskUtil._format_log_lines(stdout_lines)}")
            
            # Cleanup by removing the recipe file
            SubProcessTaskUtil._remove_directory(exec_out_dir)
        
        return_code = ingest_process.returncode
        if return_code != 0:
            # Failed
            ctx.get_report().report_info("Failed to execute 'datahub ingest'")
            raise TaskError("Failed to execute 'datahub ingest'") 
        
        # Report Successful execution
        ctx.get_report().report_info("Successfully executed 'datahub ingest'")


    def close(self) -> None:
        pass

    

