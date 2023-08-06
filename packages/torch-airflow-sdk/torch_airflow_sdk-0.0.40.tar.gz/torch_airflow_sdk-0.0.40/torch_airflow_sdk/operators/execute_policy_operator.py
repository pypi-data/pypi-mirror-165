from airflow.models.baseoperator import BaseOperator
from torch_sdk.torch_client import TorchClient
from torch_airflow_sdk.initialiser import torch_credentials
from torch_sdk.constants import FailureStrategy
import logging
LOGGER = logging.getLogger("tasks")


class ExecutePolicyOperator(BaseOperator):
    """
    Description:
        ExecutePolicyOperator is used to execute a policy by passing policy_type and policy_id.
        It will return only after the execution ends if sync is set to True.

        :param policy_type: (String) Type of policy to be executed
        :param policy_id: (String) id of the policy to be executed
        :param incremental: (bool) optional Set it to True if full execution has to be done
        :param sync: (bool) optional Set it to True to execute policy in synchronous mode
        :param failure_strategy: (enum) optional Set it to decide if it should fail at error,
            fail at warning or never fail
    """

    def __init__(self, *, policy_type, policy_id, sync, incremental=False,
                 failure_strategy: FailureStrategy = FailureStrategy.DoNotFail, **kwargs):
        """
        :param policy_type: (PolicyType) Type of policy to be executed
        :param policy_id: (String) id of the policy to be executed
        :param incremental: (bool) optional Set it to True if full execution has to be done
        :param sync: (bool) optional Set it to True to execute policy in synchronous mode
        :param failure_strategy: (enum) optional Set it to decide if it should fail at error,
            fail at warning or never fail

        Example:
        from torch_sdk.constants import RuleExecutionStatus, FailureStrategy, PolicyType
        from torch_sdk.common import Executor
        operator_task = ExecutePolicyOperator(
            task_id='torch_pipeline_operator_test',
            policy_type=PolicyType.DATA_QUALITY,
            policy_id=46,
            sync=True,
            failure_strategy=FailureStrategy.FailOnError,
            dag=dag
        )

        In case you need to query the status in another task you need to pull the execution id from xcom by passing
        the policy name in the {policy_name}_execution_id. In this example the policy name of policy_id 46 is 'policy_with_email'

        After getting the execution_id you need to create object of Executor by passing policy_type and
        torch_client object and call get_result using the execution_id.

        def operator_result(**context):
            xcom_key = {policy_type.name}_{policy_id}_execution_id'
            task_instance = context['ti']
            # get the policy_name and execution id - then pull from xcom
            execution_id = task_instance.xcom_pull(key=xcom_key)
            if execution_id is not None:
                torch_client = TorchClient(**torch_credentials)
                result = torch_client.get_polcy_execution_result(policy_type=PolicyType.DATA_QUALITY, execution_id=execution_id)
        """
        super().__init__(**kwargs)
        self.policy_type = policy_type
        self.policy_id = policy_id
        self.incremental = incremental
        self.failure_strategy = failure_strategy
        self.sync = sync

    def execute(self, context):
        torch_client = TorchClient(**torch_credentials)
        execution_return = torch_client.execute_policy(
            policy_type=self.policy_type,
            policy_id=self.policy_id,
            sync=self.sync,
            incremental=self.incremental,
            failure_strategy=self.failure_strategy)
        if execution_return.id is not None:
            xcom_key = f'{self.policy_type.name}_{self.policy_id}_execution_id'
            task_instance = context['ti']
            # get the policy_name and execution id - then push them in xcom
            task_instance.xcom_push(key=xcom_key, value=execution_return.id)

