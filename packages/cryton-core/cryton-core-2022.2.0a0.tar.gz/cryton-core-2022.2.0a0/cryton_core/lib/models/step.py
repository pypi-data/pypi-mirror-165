from datetime import datetime
from typing import Union, Type, Optional
import re
import copy

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models.query import QuerySet
from django.core import exceptions as django_exc
from django.db.models import Q
from django.utils import timezone
import amqpstorm
from schema import Schema, Optional as SchemaOptional, SchemaError, Or, And

from cryton_core.cryton_app.models import StepModel, StepExecutionModel, SuccessorModel, ExecutionVariableModel, \
    OutputMappingModel, CorrelationEventModel

from cryton_core.etc import config
from cryton_core.lib.util import constants, exceptions, logger, states, util
from cryton_core.lib.models import worker, session
from cryton_core.lib.util.exceptions import StepTypeDoesNotExist
from enum import EnumMeta, Enum

from dataclasses import dataclass, asdict


@dataclass
class StepReport:
    id: int
    step_name: str
    state: str
    start_time: datetime
    finish_time: datetime
    std_err: str
    std_out: str
    mod_err: str
    mod_out: dict
    evidence_file: str
    result: str
    valid: bool


class Step:

    def __init__(self, **kwargs):
        """

        :param kwargs:
                 step_model_id: int = None,
                 stage_model_id: int = None,
                 arguments: str = None,
                 is_init: bool = None,
                 name: str = None
                 step_type: str = None
        """
        step_model_id = kwargs.get('step_model_id')
        if step_model_id:
            try:
                self.model = StepModel.objects.get(id=step_model_id)
            except django_exc.ObjectDoesNotExist:
                raise exceptions.StepObjectDoesNotExist("PlanModel with id {} does not exist."
                                                        .format(step_model_id))

        else:
            step_obj_arguments = copy.deepcopy(kwargs)
            step_obj_arguments.pop('next', None)
            step_obj_arguments.pop('output_mapping', None)
            # Set default prefix as step name
            if step_obj_arguments.get('output_prefix') is None:
                step_obj_arguments.update({'output_prefix': step_obj_arguments.get('name')})
            self.model = StepModel.objects.create(**step_obj_arguments)

    def delete(self):
        self.model.delete()

    @property
    def model(self) -> Union[Type[StepModel], StepModel]:
        self.__model.refresh_from_db()
        return self.__model

    @model.setter
    def model(self, value: StepModel):
        self.__model = value

    @property
    def stage_model_id(self) -> Union[Type[int], int]:
        return self.model.stage_model_id

    @stage_model_id.setter
    def stage_model_id(self, value: int):
        model = self.model
        model.stage_model_id = value
        model.save()

    @property
    def name(self) -> str:
        return self.model.name

    @name.setter
    def name(self, value: str):
        model = self.model
        model.name = value
        model.save()

    @property
    def step_type(self) -> str:
        return self.model.step_type

    @step_type.setter
    def step_type(self, value: str):
        model = self.model
        model.step_type = value
        model.save()

    @property
    def is_init(self) -> bool:
        return self.model.is_init

    @is_init.setter
    def is_init(self, value: bool):
        model = self.model
        model.is_init = value
        model.save()

    @property
    def is_final(self) -> bool:
        return self.model.is_final

    @is_final.setter
    def is_final(self, value: bool):
        model = self.model
        model.is_final = value
        model.save()

    @property
    def arguments(self) -> dict:
        return self.model.arguments

    @arguments.setter
    def arguments(self, value: dict):
        model = self.model
        model.arguments = value
        model.save()

    @property
    def output_prefix(self) -> str:
        return self.model.output_prefix

    @output_prefix.setter
    def output_prefix(self, value: bool):
        model = self.model
        model.output_prefix = value
        model.save()

    @property
    def execution_stats_list(self) -> QuerySet:
        """
        Returns StepExecutionStatsModel QuerySet. If the latest is needed, use '.latest()' on result.
        :return: QuerySet of StepExecutionStatsModel
        """
        return StepExecutionModel.objects.filter(step_model_id=self.model.id)

    @property
    def parents(self) -> QuerySet:
        return StepModel.objects.filter(id__in=SuccessorModel.objects.filter(
            successor_id=self.model.id).values_list('parent_id'))

    @property
    def successors(self) -> QuerySet:
        return StepModel.objects.filter(id__in=SuccessorModel.objects.filter(
            parent_id=self.model.id).values_list('successor_id'))

    @staticmethod
    def filter(**kwargs) -> QuerySet:
        """
        Get list of StepInstances according to no or specified conditions
        :param kwargs: dict of parameters to filter by
        :return:
        """
        if kwargs:
            try:
                return StepModel.objects.filter(**kwargs)
            except django_exc.FieldError as ex:
                raise exceptions.WrongParameterError(message=ex)
        else:
            return StepModel.objects.all()

    @classmethod
    def validate(cls, step_dict) -> bool:
        """
        Validate a step dictionary

        :raises:
            exceptions.StepValidationError
        :return: True
        """

        forbidden_output_prefixes = ["parent"]
        for step_object in StepModel.objects.all():
            forbidden_output_prefixes.append(step_object.name)

        conf_schema = Schema({
            'name': str,
            constants.STEP_TYPE: str,
            SchemaOptional('is_init'): bool,
            constants.ARGUMENTS: dict,
            SchemaOptional('next'): list,
            SchemaOptional('output_mapping'): [{'name_from': str, 'name_to': str}],
            SchemaOptional('output_prefix'): And(str, lambda x: (
                        x not in forbidden_output_prefixes and ("." not in x and "&" not in x)
            ), error="This output_prefix is not allowed")

        })

        try:
            conf_schema.validate(step_dict)
            StepType[step_dict[constants.STEP_TYPE]].value.validate(step_dict[constants.ARGUMENTS])

            if 'next' in step_dict.keys():
                for value_of_next in step_dict['next']:
                    cls.validate_next_parameter(value_of_next)
        except (SchemaError, StepTypeDoesNotExist) as ex:
            raise exceptions.StepValidationError(ex, step_name=step_dict.get('name'))

        return True

    @classmethod
    def validate_ssh_connection(cls, ssh_connection_dict):
        """
        Validate ssh_connection dictionary

        :raises:
            exceptions.StepValidationError
        :return: True
        """

        conf_schema = Schema(Or(
            {
                'target': str,
                SchemaOptional('username'): str,
                SchemaOptional(Or(
                    'password',
                    'ssh_key',
                    only_one=True,
                    error="Arguments 'password' and 'ssh_key' cannot be used together"
                )): str,
                SchemaOptional('port'): int
            }
        ))

        conf_schema.validate(ssh_connection_dict)

    @classmethod
    def validate_next_parameter(cls, next_dict):
        successor_types_without_any = constants.SUCCESSOR_TYPES_WITHOUT_ANY
        conf_schema = Schema(Or(
            {
                'type': And(str, lambda x: x in successor_types_without_any),
                'value': str,
                'step': str

            },
            {
                'type': And(str, lambda x: x == "any"),
                'step': str
            }
        ))

        conf_schema.validate(next_dict)

        if next_dict["type"] == constants.RESULT and next_dict["value"] not in constants.VALID_SUCCESSOR_RESULTS:
            raise SchemaError("Invalid value for type 'result' in the parameter 'next'")

        elif next_dict["type"] == constants.STATE and next_dict["value"] not in states.VALID_SUCCESSOR_STATES:
            raise SchemaError("Invalid value for type 'state' in the parameter 'next'")

    def add_successor(self, successor_id: int, successor_type: str, successor_value: Optional[str]) -> int:
        """
        Check if successor's parameters are correct and save it.
        :param successor_id:
        :param successor_type: One of valid types
        :param successor_value: One of valid values for specified type
        :raises:
            InvalidSuccessorType
            InvalidSuccessorValue
        :return: SuccessorModel id
        """
        if successor_type not in constants.VALID_SUCCESSOR_TYPES:
            raise exceptions.InvalidSuccessorType(
                "Unknown successor type. Choose one of valid types: {}".format(constants.VALID_SUCCESSOR_TYPES),
                successor_type
            )

        if (successor_type == constants.RESULT and successor_value not in constants.VALID_SUCCESSOR_RESULTS) or \
                (successor_type == constants.STATE and successor_value not in states.VALID_SUCCESSOR_STATES):
            raise exceptions.InvalidSuccessorValue(
                "Unknown successor value. Choose one of valid types: {}".format(constants.VALID_SUCCESSOR_RESULTS),
                successor_value
            )

        if successor_type == constants.ANY and successor_value is None:
            successor_value = ""

        successor = SuccessorModel(parent_id=self.model.id, successor_id=successor_id, type=successor_type,
                                   value=successor_value)
        successor.save()

        return successor.id


class StepWorkerExecute(Step):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.module_name = self.arguments[constants.MODULE]
        self.module_arguments = self.arguments[constants.MODULE_ARGUMENTS]

    @classmethod
    def validate(cls, step_arguments):
        """
        Validate arguments in 'worker/execute' step_type
        """
        worker_exec_valid_schema = Schema(Or(
            {
                constants.MODULE: str,
                constants.MODULE_ARGUMENTS: dict,
                SchemaOptional(constants.CREATE_NAMED_SESSION): str,
                SchemaOptional(constants.USE_ANY_SESSION_TO_TARGET): str
            },
            {
                constants.MODULE: str,
                constants.MODULE_ARGUMENTS: dict,
                SchemaOptional(constants.CREATE_NAMED_SESSION): str,
                SchemaOptional(constants.USE_NAMED_SESSION): str
            },
            {
                constants.MODULE: str,
                constants.MODULE_ARGUMENTS: dict,
                SchemaOptional(constants.SSH_CONNECTION): dict
            },
            {
                constants.MODULE: str,
                constants.MODULE_ARGUMENTS: dict,
                SchemaOptional(constants.SESSION_ID): int,
                SchemaOptional(constants.CREATE_NAMED_SESSION): str
            },
            only_one=True
        ))

        worker_exec_valid_schema.validate(step_arguments)

        if constants.SSH_CONNECTION in step_arguments:
            cls.validate_ssh_connection(step_arguments[constants.SSH_CONNECTION])


class StepEmpireAgentDeploy(Step):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def validate(cls, step_arguments):
        """
        Validate arguments in 'empire/agent-deploy' step type
        """
        agent_deploy_valid_schema = Schema(Or(
            {
                constants.LISTENER_NAME: str,
                SchemaOptional(constants.LISTENER_PORT): int,
                SchemaOptional(constants.LISTENER_OPTIONS): dict,
                SchemaOptional(constants.LISTENER_TYPE): str,
                constants.STAGER_TYPE: str,
                SchemaOptional(constants.STAGER_OPTIONS): dict,
                constants.AGENT_NAME: And(str, lambda n: n.isalnum(), error='Invalid agent_name format'),
                SchemaOptional(Or(
                    constants.USE_NAMED_SESSION,
                    constants.USE_ANY_SESSION_TO_TARGET,
                    only_one=True
                )): str
            },
            {
                constants.LISTENER_NAME: str,
                SchemaOptional(constants.LISTENER_PORT): int,
                SchemaOptional(constants.LISTENER_OPTIONS): dict,
                SchemaOptional(constants.LISTENER_TYPE): str,
                constants.STAGER_TYPE: str,
                SchemaOptional(constants.STAGER_OPTIONS): dict,
                constants.AGENT_NAME: And(str, lambda n: n.isalnum(), error='Invalid agent_name format'),
                SchemaOptional(constants.SESSION_ID): int
            },
            {
                constants.LISTENER_NAME: str,
                SchemaOptional(constants.LISTENER_PORT): int,
                SchemaOptional(constants.LISTENER_OPTIONS): dict,
                SchemaOptional(constants.LISTENER_TYPE): str,
                constants.STAGER_TYPE: str,
                SchemaOptional(constants.STAGER_OPTIONS): dict,
                constants.AGENT_NAME: And(str, lambda n: n.isalnum(), error='Invalid agent_name format'),
                SchemaOptional(constants.SSH_CONNECTION): dict
            },
            only_one=True
        ))

        agent_deploy_valid_schema.validate(step_arguments)

        if constants.SSH_CONNECTION in step_arguments:
            cls.validate_ssh_connection(step_arguments[constants.SSH_CONNECTION])


class StepEmpireExecute(Step):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def validate(cls, step_arguments):
        """
        Validate arguments in 'empire/execute' step type
        """
        empire_exec_valid_schema = Schema(
            Or(
                {
                    constants.USE_AGENT: And(str, lambda n: n.isalnum(), error='Invalid agent name format'),
                    constants.SHELL_COMMAND: str
                },
                {
                    constants.USE_AGENT: And(str, lambda n: n.isalnum(), error='Invalid agent name format'),
                    constants.MODULE: str,
                    SchemaOptional(constants.MODULE_ARGUMENTS): dict
                },
                only_one=True
            ), error="Wrong combination of arguments, please see documentation")

        empire_exec_valid_schema.validate(step_arguments)


class StepExecution:

    def __init__(self, **kwargs):
        """

        :param kwargs:
        (optional) step_execution_id: int - for retrieving existing execution
        step_model_id: int - for creating new execution
        """
        step_execution_id = kwargs.get('step_execution_id')
        if step_execution_id is not None:
            try:
                self.model = StepExecutionModel.objects.get(id=step_execution_id)
            except django_exc.ObjectDoesNotExist:
                raise exceptions.StepExecutionObjectDoesNotExist("StepExecutionStatsModel with id {} does not exist."
                                                                 .format(step_execution_id))

        else:
            self.model = StepExecutionModel.objects.create(**kwargs)

    def delete(self):
        self.model.delete()

    @property
    def model(self) -> Union[Type[StepExecutionModel], StepExecutionModel]:
        self.__model.refresh_from_db()
        return self.__model

    @model.setter
    def model(self, value: StepExecutionModel):
        self.__model = value

    @property
    def state(self) -> str:
        return self.model.state

    @state.setter
    def state(self, value: str):
        with transaction.atomic():
            StepExecutionModel.objects.select_for_update().get(id=self.model.id)
            if states.StepStateMachine(self.model.id).validate_transition(self.state, value):
                logger.logger.debug("stepexecution changed state", state_from=self.state, state_to=value)
                model = self.model
                model.state = value
                model.save()

    @property
    def result(self) -> str:
        return self.model.result

    @result.setter
    def result(self, value: str):
        model = self.model
        model.result = value
        model.save()

    @property
    def std_out(self) -> str:
        return self.model.std_out

    @std_out.setter
    def std_out(self, value: str):
        model = self.model
        model.std_out = value
        model.save()

    @property
    def std_err(self) -> str:
        return self.model.std_err

    @std_err.setter
    def std_err(self, value: str):
        model = self.model
        model.std_err = value
        model.save()

    @property
    def mod_out(self) -> dict:
        return self.model.mod_out

    @mod_out.setter
    def mod_out(self, value: dict):
        model = self.model
        model.mod_out = value
        model.save()

    @property
    def mod_err(self) -> str:
        return self.model.mod_err

    @mod_err.setter
    def mod_err(self, value: str):
        model = self.model
        model.mod_err = value
        model.save()

    @property
    def evidence_file(self) -> str:
        return self.model.evidence_file

    @evidence_file.setter
    def evidence_file(self, value: str):
        model = self.model
        model.evidence_file = value
        model.save()

    @property
    def start_time(self) -> Optional[datetime]:
        return self.model.start_time

    @start_time.setter
    def start_time(self, value: Optional[datetime]):
        model = self.model
        model.start_time = value
        model.save()

    @property
    def finish_time(self) -> Optional[datetime]:
        return self.model.finish_time

    @finish_time.setter
    def finish_time(self, value: Optional[datetime]):
        model = self.model
        model.finish_time = value
        model.save()

    @property
    def valid(self) -> bool:
        return self.model.valid

    @valid.setter
    def valid(self, value: bool):
        model = self.model
        model.valid = value
        model.save()

    @property
    def parent_id(self) -> int:
        return self.model.parent_id

    @parent_id.setter
    def parent_id(self, value: int):
        model = self.model
        model.parent_id = value
        model.save()

    @staticmethod
    def filter(**kwargs) -> QuerySet:
        """
        Get list of StepExecutionStatsModel according to specified conditions.

        :param kwargs: dict of parameters to filter by
        :return: Desired QuerySet
        """
        if kwargs:
            try:
                return StepExecutionModel.objects.filter(**kwargs)
            except django_exc.FieldError as ex:
                raise exceptions.WrongParameterError(message=ex)
        else:
            return StepExecutionModel.objects.all()

    def validate(self):
        """
        Validates Step Execution.

        :return:
        """
        pass

    def save_output(self, step_output: dict) -> None:
        """
        Save Step Execution output to StepExecutionModel.

        :param step_output: dictionary with keys: std_err, std_out
        :return: None
        """
        if (mod_out := step_output.get(constants.MOD_OUT)) is not None:
            output_mappings = OutputMappingModel.objects.filter(step_model=self.model.step_model)
            for output_mapping in output_mappings:
                util.rename_key(mod_out, output_mapping.name_from, output_mapping.name_to)

        model = self.model

        if (std_out := step_output.get(constants.STD_OUT)) is not None:
            model.std_out = std_out
        if (std_err := step_output.get(constants.STD_ERR)) is not None:
            model.std_err = std_err
        if mod_out is not None:
            model.mod_out = mod_out
        if (mod_err := step_output.get(constants.MOD_ERR)) is not None:
            model.mod_err = mod_err

        model.evidence_file = evidence_file if (evidence_file := step_output.get(constants.EVIDENCE_FILE)) \
            else 'No evidence '
        model.save()

        return None

    def _update_dynamic_variables(self, arguments: dict, parent_step_ex_id: Optional[int]) -> dict:
        """
        Update dynamic variables in mod_args (even with special $parent prefix)

        :param arguments: arguments that should be updated
        :param parent_step_ex_id: ID of the parent step of the current step execution
        :return: Arguments updated for dynamic variables
        """

        # Get list of dynamic variables
        vars_list = util.get_dynamic_variables(arguments)

        # Get their prefixes
        prefixes = util.get_prefixes(vars_list)
        vars_dict = dict()
        is_parent = False

        for prefix in prefixes:
            # If prefix is parent, get parents prefix
            if prefix == 'parent':
                if parent_step_ex_id is None:
                    raise RuntimeError("Parent must be specified for $parent prefix.")
                is_parent = True
                prefix = StepExecutionModel.objects.get(id=parent_step_ex_id).step_model.output_prefix

            tmp_dict = dict()

            for step_ex in StepExecutionModel.objects.filter(
                    step_model__output_prefix=prefix,
                    stage_execution__plan_execution=self.model.stage_execution.plan_execution
            ):
                if step_ex.mod_out:
                    tmp_dict.update(step_ex.mod_out)
            # Change parents prefix back to 'parent' for updating dictionary to substitute
            if is_parent:
                prefix = 'parent'
                is_parent = False
            vars_dict.update({prefix: tmp_dict})

        updated_arguments = util.fill_dynamic_variables(arguments, vars_dict)
        return updated_arguments

    @staticmethod
    def _update_arguments_with_execution_variables(arguments: dict, execution_vars: list) -> dict:
        """
        Update passed arguments with execution variables.

        :param arguments: Arguments to be updated with execution variables
        :param execution_vars: Execution variables to be passed to arguments
        :return: Updated arguments with execution variables
        """

        execution_vars_dict = dict()
        for execution_var in execution_vars:
            execution_vars_dict.update({execution_var.get('name'): execution_var.get('value')})

        return util.fill_execution_variables(arguments, execution_vars_dict)

    def update_step_arguments(self, arguments: dict, plan_execution_id: Type[int]) -> dict:
        """
        Update Step arguments with execution and dynamic variables.

        :param arguments: Arguments to be updated
        :param plan_execution_id: ID of the parent step of the current step execution
        :return: Updated arguments with execution and dynamic variables
        """
        execution_vars = list(ExecutionVariableModel.objects.filter(plan_execution_id=plan_execution_id).values())
        if execution_vars:  # TODO: re-raise error, handle it in execute(), set ERROR state
            arguments.update(self._update_arguments_with_execution_variables(arguments, execution_vars))
        # Update dynamic variables
        arguments.update(self._update_dynamic_variables(arguments, self.parent_id))

        return arguments

    def get_msf_session_id(self, step_obj: Step, plan_execution_id: Type[int]) -> Optional[str]:
        """
        Check if there should be used any session stored in database and get its session_id.

        :param step_obj: Step instance of current Step Execution
        :param plan_execution_id: Plan Execution ID of current Step Execution.
        :return: MSF Session id
        """
        step_arguments = step_obj.arguments
        use_named_session = step_arguments.get(constants.USE_NAMED_SESSION)
        use_any_session_to_target = step_arguments.get(constants.USE_ANY_SESSION_TO_TARGET)

        if use_named_session is not None:
            # Throws SessionObjectDoesNotExist
            try:
                return session.get_msf_session_id(use_named_session, plan_execution_id)
            except exceptions.SessionObjectDoesNotExist:
                err_msg = {'message': "No session with specified name open",
                           'session_name': use_named_session,
                           'plan_execution_id': plan_execution_id, 'step_id': step_obj.model.id}
                logger.logger.error(**err_msg)
                self.state = states.ERROR
                raise exceptions.SessionIsNotOpen(**err_msg)

        elif use_any_session_to_target is not None:
            # Get last session
            try:
                session_msf_id_lst = session.get_session_ids(use_any_session_to_target, plan_execution_id)
            except Exception as ex:  # TODO: too broad exception clause and wrong error may be raised
                raise exceptions.RabbitConnectionError(str(ex))

            if len(session_msf_id_lst) == 0 or session_msf_id_lst[-1] is None:
                err_msg = {'message': "No session to desired target open",
                           'plan_execution_id': plan_execution_id, 'step_id': step_obj.model.id}
                logger.logger.error(**err_msg)
                self.state = states.ERROR
                raise exceptions.SessionObjectDoesNotExist(**err_msg)
            return session_msf_id_lst[-1]

    def send_step_execution_request(self, rabbit_channel: amqpstorm.Channel, message_body: dict, reply_queue: str,
                                    target_queue: str) -> str:
        """
        Sends RPC request to execute step using RabbitMQ.

        :param rabbit_channel: Rabbit channel
        :param message_body: data that should be sent to worker
        :param reply_queue: Queue that worker should reply to
        :param target_queue: Queue on which should data be sent to worker(for example)
        :return: correlation_id of the sent message
        """
        with util.Rpc(rabbit_channel) as rpc:
            correlation_id = rpc.prepare_message(message_body, reply_queue)
            CorrelationEventModel.objects.create(correlation_id=correlation_id, step_execution_id=self.model.id)

            # TODO: Since the state is set, it isn't necessary to raise an error, or it should be handled in the
            #  execute method.
            response = rpc.call(target_queue)
            if response is None:
                self.state = states.ERROR
                raise exceptions.RabbitConnectionError("No response from Worker.")

            # TODO: When the execution returns immediately from Worker, it will throw an error due to unchanged state
            self.state = states.RUNNING
            return rpc.correlation_id

    def _prepare_execution(self, rabbit_channel: amqpstorm.Channel = None) -> [Type[int], worker.Worker,
                                                                               amqpstorm.Connection]:
        """
        Execute necessary actions and return variables needed for individual execution of each type of StepExecution.

        :param rabbit_channel: Rabbit channel
        :return: Plan execution id, worker instance of current plan, rabbit channel
        """
        states.StepStateMachine(self.model.id).validate_state(self.state, states.STEP_EXECUTE_STATES)
        logger.logger.debug("Executing Step", step_id=self.model.step_model_id)

        if rabbit_channel is None:
            rabbit_channel = util.rabbit_connection().channel()

        plan_execution_id = self.model.stage_execution.plan_execution_id
        step_worker_obj = self.model.stage_execution.plan_execution.worker
        worker_obj = worker.Worker(worker_model_id=step_worker_obj.id)

        # Set STARTING state
        self.start_time = timezone.now()
        self.state = states.STARTING

        return plan_execution_id, worker_obj, rabbit_channel

    def execute(self):
        """
        Execute current Step Execution.

        :return:
        """
        pass

    def report(self) -> dict:
        """
        Generate report containing output from Step Execution.

        :return: Step Execution report
        """
        report_obj = StepReport(id=self.model.id, step_name=self.model.step_model.name, state=self.state,
                                start_time=self.start_time, finish_time=self.finish_time, result=self.result,
                                mod_out=self.mod_out, mod_err=self.mod_err, std_out=self.std_out,
                                std_err=self.std_err, evidence_file=self.evidence_file, valid=self.valid)

        return asdict(report_obj)

    def get_regex_successors(self) -> QuerySet:
        """
        Get successors according to provided regex.

        :return: QuerySet of StepModel objects
        """
        succs_ids_set = set()
        # Get all successormodels that have regex specified in successor_value (starting with r' or r")
        successor_list = SuccessorModel.objects.filter(parent_id=self.model.step_model.id). \
            filter(Q(value__startswith='r"', value__endswith='"')
                   | Q(value__startswith="r'", value__endswith="'"))

        # Match all regex successors against actual value
        for successor_obj in successor_list:
            desired_successor_value = successor_obj.value
            regex = re.match(r"r[\"|\'](.*?)[\"|\']", desired_successor_value)
            # Gets successor_value from successor_type eg. self.mod_out for successor_type == 'mod_out'
            successor_value = getattr(self, successor_obj.type)
            # If regex matches -> add successor step_id to set
            if re.search(r"{}".format(regex.group(0)[2:-1]), str(successor_value)):
                matched_successor = successor_obj.successor.id
                succs_ids_set.add(matched_successor)

        # Convert set of IDs into actual StepModels
        succs_queryset = StepModel.objects.filter(id__in=succs_ids_set)
        return succs_queryset

    def get_successors(self) -> QuerySet:
        """
        Get Successors based on evaluated dependency.

        :return: QuerySet of StepModel objects
        """
        # Get step successor from DB
        successors_ids_set = set()
        for successor_type in SuccessorModel.objects.filter(parent_id=self.model.step_model.id). \
                values('type').distinct():
            successor_type = successor_type.get('type')
            # Add ANY successors and continue
            if successor_type == constants.ANY:
                matched_successor = SuccessorModel.objects.get(parent_id=self.model.step_model.id,
                                                               type=successor_type).successor.id
                successors_ids_set.add(matched_successor)
                continue
            # Get the actual value of successor_type
            try:
                successor_value = getattr(self, successor_type)
            except AttributeError:
                # This should be taken care of during Plan validation, but in any case:
                logger.logger.error("Wrong successor type.", type=successor_type)
                continue
            try:
                matched_successor = SuccessorModel.objects.get(parent_id=self.model.step_model.id,
                                                               type=successor_type,
                                                               value=successor_value).successor.id
            except ObjectDoesNotExist:
                pass
            else:
                successors_ids_set.add(matched_successor)

        successors_queryset = StepModel.objects.filter(id__in=successors_ids_set)

        regex_successors_queryset = self.get_regex_successors()
        result_queryset = successors_queryset | regex_successors_queryset

        return result_queryset

    def ignore(self) -> None:
        """
        Set IGNORE state to Step Execution and to all of its successors.

        :return: None
        """
        logger.logger.debug("Ignoring Step", step_id=self.model.step_model_id)
        # Stop recursion
        if self.state == states.IGNORED:
            return None
        # If any non SKIPPED parent exists (ignoring the one that called ignore())
        for par_step in Step(step_model_id=self.model.step_model.id).parents:
            step_exec_obj = StepExecutionModel.objects.get(step_model=par_step,
                                                           stage_execution=self.model.stage_execution)
            if step_exec_obj.state not in states.STEP_FINAL_STATES:
                return None
        # Set ignore state
        self.state = states.IGNORED
        # Execute for all successors
        for successor_step in Step(step_model_id=self.model.step_model.id).successors:
            step_ex_id = StepExecutionModel.objects.get(step_model=successor_step,
                                                        stage_execution=self.model.stage_execution).id
            step_ex_obj = StepExecution(step_execution_id=step_ex_id)
            step_ex_obj.ignore()

        return None

    def postprocess(self, ret_vals: dict) -> None:
        """
        Perform necessary things after executing Step like creating named sessions, update state, update successors
        and save Step Execution Output.

        :param ret_vals: output from Step Execution
        :return: None
        """
        logger.logger.debug("Postprocessing Step", step_id=self.model.step_model_id)
        step_obj = Step(step_model_id=self.model.step_model.id)

        # Check if any named session should be created:
        create_named_session = step_obj.arguments.get(constants.CREATE_NAMED_SESSION)
        if create_named_session is not None:
            msf_session_id = ret_vals.get(constants.RET_SESSION_ID)
            if msf_session_id is not None:
                session.create_session(self.model.stage_execution.plan_execution_id, msf_session_id,
                                       create_named_session)

        # Set final state, optionally save result
        return_code = ret_vals.get(constants.RETURN_CODE)
        self.finish_time = timezone.now()

        if return_code == constants.CODE_TERMINATED:
            self.state = states.TERMINATED
        elif return_code == constants.CODE_ERROR:
            self.state = states.ERROR
        else:
            self.state = states.FINISHED
            self.result = constants.RETURN_CODE_ENUM.get(return_code, constants.RESULT_UNKNOWN)

        # Store file, if present in returned object
        ret_file = ret_vals.get(constants.RET_FILE)
        if ret_file is not None:
            file_name = ret_file.get(constants.RET_FILE_NAME)
            file_content = ret_file.get(constants.RET_FILE_CONTENT)
            evidence_dir = self.model.stage_execution.plan_execution.evidence_dir
            file_path = util.store_evidence_file(file_name, file_content, evidence_dir)
            ret_vals.update({constants.EVIDENCE_FILE: file_path})

        # Store job output and error message
        self.save_output(ret_vals)

        # update Successors parents
        successor_list = self.get_successors()

        for successor_step in successor_list:
            successor_step_execution_model = StepExecutionModel.objects.get(
                step_model_id=successor_step.id, stage_execution_id=self.model.stage_execution_id, state=states.PENDING)
            StepExecution(step_execution_id=successor_step_execution_model.id).parent_id = self.model.id

        logger.logger.debug("Step postprocess finished", step_id=self.model.step_model_id)

        return None

    def ignore_successors(self) -> None:
        """
        Ignor/skip all successor Steps of current Step Execution.

        :return: None
        """
        logger.logger.debug("Ignoring Step successors", step_id=self.model.step_model_id)
        step_obj = Step(step_model_id=self.model.step_model.id)
        # Get correct step successor from DB which are to be executed
        successor_list = self.get_successors()
        # Get all possible successors
        all_successor_list = StepModel.objects.filter(
            id__in=step_obj.model.successors.all().values_list('successor'))
        # Set IGNORE steps (all successors which wont be executed and don't have parents
        successor_to_be_skipped = all_successor_list.difference(successor_list)
        for successor_step in successor_to_be_skipped:
            try:
                successor_step_exec_id = StepExecutionModel.objects.get(step_model_id=successor_step.id,
                                                                        stage_execution=self.model.stage_execution_id,
                                                                        state=states.PENDING).id
            except ObjectDoesNotExist:
                # Does not exist or is not PENDING
                continue
            StepExecution(step_execution_id=successor_step_exec_id).ignore()
        return None

    def execute_successors(self) -> None:
        """
        Execute all successors of current Step Execution.

        :return: None
        """
        logger.logger.debug("Executing Step successors", step_id=self.model.step_model_id)

        # Get correct step successor from DB which are to be executed
        successor_list = self.get_successors()

        # Execute all successors
        for successor_step_model in successor_list:
            successor_step_execution_model = StepExecutionModel.objects.get(
                step_model_id=successor_step_model.id,
                stage_execution_id=self.model.stage_execution_id,
                state=states.PENDING
            )
            successor_step_exec = StepExecutionType[successor_step_model.step_type].value(
                step_execution_id=successor_step_execution_model.id
            )
            try:
                successor_step_exec.execute()
            except (exceptions.SessionIsNotOpen, exceptions.SessionObjectDoesNotExist):
                pass
                # TODO: the error is logged and state is set in the self.get_msf_id().
                #  It shouldn't be handled here, but it the execute() method.
        return None

    def pause_successors(self) -> None:
        """
        Pause successor Steps of current Step Execution.

        :return: None
        """
        logger.logger.debug("Pausing Step successors", step_id=self.model.step_model_id)
        # Set all successors to PAUSED, so they can be recognized/executed when unpaused
        successor_list = self.get_successors()
        for step_obj in successor_list:
            successor_exec_id = StepExecutionModel.objects.get(stage_execution=self.model.stage_execution,
                                                               step_model_id=step_obj.id).id
            StepExecution(step_execution_id=successor_exec_id).state = states.PAUSED
            logger.logger.info('successors step execution paused', successor_exec_id=successor_exec_id)

        return None

    def kill(self):
        """
        Kill current Step Execution on Worker.

        :return: Dictionary containing return_code and std_err
        """
        logger.logger.debug("Killing Step", step_id=self.model.step_model_id)
        states.StepStateMachine(self.model.id).validate_state(self.state, states.STEP_KILL_STATES)

        state_before = self.state
        self.state = states.TERMINATING

        if state_before == states.PAUSED:
            self.finish_time = timezone.now()
            self.state = states.TERMINATED
        else:
            worker_obj = worker.Worker(worker_model_id=self.model.stage_execution.plan_execution.worker.id)
            correlation_id = self.model.correlation_events.first().correlation_id
            event_info = {constants.EVENT_T: constants.EVENT_KILL_STEP_EXECUTION,
                          constants.EVENT_V: {"correlation_id": correlation_id}}

            with util.Rpc() as worker_rpc:
                resp = worker_rpc.call(worker_obj.control_q_name, event_info)

            # The TERMINATED state is set in the `postprocess` method.
            resp_dict = resp.get('event_v')
            if resp_dict.get('return_code') != 0:
                logger.logger.warning("step execution not terminated", step_execution_id=self.model.id,
                                      stage_name=self.model.step_model.name, status='failure',
                                      error=resp_dict.get('std_err'))

        logger.logger.info("step execution terminated", step_execution_id=self.model.id,
                           stage_name=self.model.step_model.name, status='success')

    def re_execute(self) -> None:
        """
        Reset execution data and re-execute StepExecution.

        :return: None
        """
        states.StepStateMachine(self.model.id).validate_state(self.state, states.STEP_FINAL_STATES)
        self.reset_execution_data()
        self.execute()

    def reset_execution_data(self) -> None:
        """
        Reset changeable data to defaults.

        :return: None
        """
        states.StepStateMachine(self.model.id).validate_state(self.state, states.STEP_FINAL_STATES)

        with transaction.atomic():
            model = self.model
            StepExecutionModel.objects.select_for_update().get(id=model.id)

            model.state = states.PENDING
            model.start_time = None
            model.pause_time = None
            model.finish_time = None
            model.result = ""
            model.std_out = ""
            model.std_err = ""
            model.mod_out = dict()
            model.mod_err = ""
            model.evidence_file = ""
            model.valid = False
            model.parent_id = None
            model.save()


class StepExecutionWorkerExecute(StepExecution):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step_instance = StepWorkerExecute(step_model_id=self.model.step_model.id)

    def validate(self) -> bool:
        """
        Validate cryton attack module arguments.

        :return:
        """
        logger.logger.debug("Validating Cryton module", step_id=self.model.step_model_id)
        worker_obj = self.model.stage_execution.plan_execution.worker
        module_name = self.step_instance.module_name.replace('/', '.')
        arguments_validation = util.validate_attack_module_args(module_name,
                                                                self.step_instance.module_arguments,
                                                                worker_obj)
        if arguments_validation:
            self.valid = True
            return self.valid

    # TODO: Will be reworked together with the RabbitMQ implementation.
    def execute(self, rabbit_channel: amqpstorm.Channel = None) -> str:
        """
        Execute Step on worker specified in execution stats.

        :param rabbit_channel: Rabbit channel
        :return: Return Correlation ID
        """
        plan_execution_id, worker_obj, rabbit_channel = super()._prepare_execution(rabbit_channel)
        module_arguments = self.update_step_arguments(self.step_instance.module_arguments, plan_execution_id)
        session_id = self.get_msf_session_id(self.step_instance, plan_execution_id)

        if session_id:
            module_arguments[constants.SESSION_ID] = session_id

        message_body = {
            constants.STEP_TYPE: self.step_instance.step_type,
            constants.ARGUMENTS: {constants.MODULE: self.step_instance.module_name,
                                  constants.MODULE_ARGUMENTS: module_arguments}
        }

        target_queue = worker_obj.attack_q_name
        reply_queue = config.Q_ATTACK_RESPONSE_NAME

        correlation_id = self.send_step_execution_request(rabbit_channel, message_body, reply_queue, target_queue)

        # Log
        logger.logger.info("step execution executed", step_execution_id=self.model.id,
                           step_name=self.step_instance.name, status='success')

        return correlation_id


class StepExecutionEmpireExecute(StepExecution):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step_instance = StepEmpireExecute(step_model_id=self.model.step_model.id)

    def execute(self, rabbit_channel: amqpstorm.Channel = None) -> str:
        """
        Execute Step on worker specified in execution stats.

        :param rabbit_channel: Rabbit channel
        :return: Return Correlation ID
        """
        plan_execution_id, worker_obj, rabbit_channel = super()._prepare_execution(rabbit_channel)
        step_arguments = self.update_step_arguments(self.step_instance.arguments, plan_execution_id)

        message_body = {
            constants.STEP_TYPE: self.step_instance.step_type,
            constants.ARGUMENTS: step_arguments,
        }

        target_queue = worker_obj.attack_q_name
        reply_queue = config.Q_ATTACK_RESPONSE_NAME

        correlation_id = self.send_step_execution_request(rabbit_channel, message_body, reply_queue, target_queue)

        # Log
        logger.logger.info("step execution executed", step_execution_id=self.model.id,
                           step_name=self.step_instance.name, status='success')

        return correlation_id

    def validate(self):
        """
        Validates StepExecutionEmpireExecute.

        :return:
        """
        self.valid = True


class StepExecutionEmpireAgentDeploy(StepExecution):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step_instance = StepEmpireAgentDeploy(step_model_id=self.model.step_model.id)

    def execute(self, rabbit_channel: amqpstorm.Channel = None) -> str:
        """
        Execute Step on worker specified in execution stats.

        :param rabbit_channel: Rabbit channel
        :return: Return Correlation ID
        """
        plan_execution_id, worker_obj, rabbit_channel = super()._prepare_execution(rabbit_channel)
        step_arguments = self.update_step_arguments(self.step_instance.arguments, plan_execution_id)
        session_id = self.get_msf_session_id(self.step_instance, plan_execution_id)

        if session_id:
            step_arguments[constants.SESSION_ID] = session_id

        message_body = {
            constants.STEP_TYPE: self.step_instance.step_type,
            constants.ARGUMENTS: step_arguments
        }

        target_queue = worker_obj.agent_q_name
        reply_queue = config.Q_AGENT_RESPONSE_NAME

        correlation_id = self.send_step_execution_request(rabbit_channel, message_body, reply_queue, target_queue)

        # Log
        logger.logger.info("step execution executed", step_execution_id=self.model.id,
                           step_name=self.step_instance.name, status='success')

        return correlation_id

    def validate(self):
        """
        Validates StepExecutionEmpireAgentDeploy.

        :return:
        """
        self.valid = True


class StepTypeMeta(EnumMeta):
    """
    Overrides base metaclass of Enum in order to support custom exception when accessing not present item.
    """
    step_types = {
        constants.STEP_TYPE_WORKER_EXECUTE: "worker_execute",
        constants.STEP_TYPE_EMPIRE_EXECUTE: "empire_execute",
        constants.STEP_TYPE_DEPLOY_AGENT: "empire_agent_deploy"
    }

    def __getitem__(self, item):
        try:
            return super().__getitem__(StepTypeMeta.step_types[item])
        except KeyError:
            raise StepTypeDoesNotExist(item, constants.STEP_TYPES_LIST)


class StepType(Enum, metaclass=StepTypeMeta):
    """
    Keys according to cryton_core.lib.util.constants
    """
    empire_agent_deploy = StepEmpireAgentDeploy
    worker_execute = StepWorkerExecute
    empire_execute = StepEmpireExecute


class StepExecutionType(Enum, metaclass=StepTypeMeta):
    """
    Keys according to cryton_core.lib.util.constants
    """
    empire_agent_deploy = StepExecutionEmpireAgentDeploy
    worker_execute = StepExecutionWorkerExecute
    empire_execute = StepExecutionEmpireExecute
