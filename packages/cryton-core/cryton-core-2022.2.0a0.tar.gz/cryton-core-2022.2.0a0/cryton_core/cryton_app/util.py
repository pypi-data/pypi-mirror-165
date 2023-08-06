from datetime import datetime
import yaml
import pytz

from rest_framework.viewsets import GenericViewSet, mixins
from django.db.models.query import QuerySet

from cryton_core.cryton_app import exceptions
from cryton_core.lib.util import util as core_util, constants


def filter_decorator(func):
    """
    Decorator for filtering of serializer results.
    :param func:
    :return: Filtered queryset
    """

    def inner(self):
        """
        Filter queryset using request's params.
        :param self:
        :return: Filtered queryset
        """
        # Create dictionary filter from request
        filters_dict = {key: value for key, value in self.request.query_params.items()}

        # Get rid of parameters that would get in a way of filter
        order_by_param = filters_dict.pop('order_by', 'id')
        filters_dict.pop('limit', None)
        filters_dict.pop('offset', None)

        # Obtain queryset
        queryset: QuerySet = func(self)

        # Update filters (optionally with __icontains)
        unsearchable_keys = [
            'run_id', 'plan_execution_id', 'stage_execution_id', 'step_execution_id', 'plan_model_id',
            'stage_model_id', 'step_model_id'
        ]
        filters_dict_update = {}

        for key, value in filters_dict.items():
            if key not in unsearchable_keys:
                filters_dict_update.update({key + '__icontains': value})
            else:
                filters_dict_update.update({key: value})

        # Filter and order queryset
        queryset = queryset.filter(**filters_dict_update)
        queryset = queryset.order_by(order_by_param)

        return queryset

    return inner


def load_body_yaml(request_body: str) -> dict:
    """
    Get YAML from body and use utf8 decoding.
    :param request_body: Incoming request data
    :return: YAML in dict representation
    """
    try:
        return yaml.safe_load(request_body)
    except Exception as ex:
        raise exceptions.ValidationError(str(ex))


def get_start_time(request_data: dict) -> datetime:
    """
    Parse start time and its timezone.
    :param request_data: Incoming request data
    :return: Normalized start time
    """
    time_zone = request_data.get('time_zone', 'utc')
    try:
        str_start_time = request_data['start_time']
    except KeyError:
        raise exceptions.ValidationError("'start_time' parameter unfilled!")

    try:
        start_time = datetime.strptime(str_start_time, constants.TIME_FORMAT)
    except ValueError:
        try:
            start_time = datetime.strptime(str_start_time, constants.TIME_FORMAT_DETAILED)
        except ValueError:
            raise exceptions.ValidationError(f"'start_time' parameter must be in '{constants.TIME_FORMAT}' or "
                                             f"'{constants.TIME_FORMAT_DETAILED}' format!")

    try:
        start_time = core_util.convert_to_utc(start_time, time_zone)
    except pytz.UnknownTimeZoneError:
        raise exceptions.ValidationError("Defined 'time_zone' is not supported!")

    return start_time


class BaseViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    A ViewSet that provides default list() action.
    """


class InstanceViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, BaseViewSet):
    """
    A ViewSet that provides default retrieve(), destroy(), and list() actions.
    """
    @filter_decorator
    def get_queryset(self):
        queryset = self.queryset

        return queryset


class InstanceFullViewSet(mixins.CreateModelMixin, InstanceViewSet):
    """
    A ViewSet that provides default retrieve(), destroy(), list(), and create() actions.
    """


class ExecutionViewSet(InstanceViewSet):
    """
    A ViewSet that provides default retrieve(), destroy(), list(), and create() actions.
    """


class ExecutionFullViewSet(InstanceFullViewSet):
    """
    A ViewSet that provides default retrieve(), destroy(), list(), and create() actions.
    """
