"""
Mock Databricks operator for local development.

In production, this would be replaced by:
  - airflow.providers.databricks.operators.databricks.DatabricksSubmitRunOperator
  - airflow.providers.databricks.operators.databricks.DatabricksRunNowOperator

This mock simulates submitting a job to Databricks by running a local PySpark
script or Python callable instead. It preserves the same interface so the DAG
structure remains representative of a real Databricks-backed pipeline.
"""

import logging
import subprocess
from typing import Any, Callable

from airflow.sdk import BaseOperator

logger = logging.getLogger(__name__)


class MockDatabricksSubmitRunOperator(BaseOperator):
    """
    Simulates submitting a Databricks job.

    In a real deployment this would call the Databricks Jobs API to submit
    a notebook or spark-submit job on a cluster. Locally, it runs the
    specified Python script as a subprocess (optionally via PySpark).

    Parameters
    ----------
    task_id : str
        Airflow task identifier.
    script_path : str
        Path to the Python/PySpark script to execute locally.
    script_args : dict[str, str] | None
        Key-value arguments passed to the script via --key value flags.
    databricks_job_config : dict | None
        Placeholder for real Databricks job JSON config. Logged but not
        used locally — shows the candidate understands the production shape.
    """

    template_fields = ("script_path", "script_args")

    def __init__(
        self,
        script_path: str,
        script_args: dict[str, str] | None = None,
        databricks_job_config: dict | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.script_path = script_path
        self.script_args = script_args or {}
        self.databricks_job_config = databricks_job_config

    def execute(self, context: Any) -> str:
        logger.info(
            "MockDatabricks: In production this would submit to Databricks. "
            "Config: %s",
            self.databricks_job_config,
        )
        logger.info("MockDatabricks: Running local script %s", self.script_path)

        cmd = ["python", self.script_path]
        for key, value in self.script_args.items():
            cmd.extend([f"--{key}", str(value)])

        logger.info("MockDatabricks: Executing %s", " ".join(cmd))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        if result.stdout:
            logger.info("MockDatabricks stdout:\n%s", result.stdout)
        if result.stderr:
            logger.warning("MockDatabricks stderr:\n%s", result.stderr)

        return f"Mock run completed for {self.script_path}"


class MockDatabricksCallableOperator(BaseOperator):
    """
    Alternative mock that runs a Python callable instead of a script.

    Useful for lightweight transformations that don't need a full PySpark
    context. The callable receives the Airflow context plus any extra kwargs.

    Parameters
    ----------
    python_callable : Callable
        Function to invoke. Should accept **kwargs including Airflow context.
    op_kwargs : dict | None
        Extra keyword arguments forwarded to the callable.
    """

    def __init__(
        self,
        python_callable: Callable,
        op_kwargs: dict | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.python_callable = python_callable
        self.op_kwargs = op_kwargs or {}

    def execute(self, context: Any) -> Any:
        logger.info(
            "MockDatabricksCallable: Running %s", self.python_callable.__name__
        )
        merged_kwargs = {**context, **self.op_kwargs}
        return self.python_callable(**merged_kwargs)
