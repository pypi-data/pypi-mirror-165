import yaml

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, extend_schema_view

from cryton_core.cryton_app import util, serializers, exceptions
from cryton_core.cryton_app.models import StepModel
from cryton_core.lib.util import exceptions as core_exceptions
from cryton_core.lib.models.step import Step


@extend_schema_view(
    list=extend_schema(description="List Steps.", parameters=[serializers.ListSerializer]),
    retrieve=extend_schema(description="Get existing Step."),
)
class StepViewSet(util.InstanceViewSet):
    """
    Step ViewSet.
    """
    queryset = StepModel.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = serializers.StepSerializer

    @extend_schema(
        description="Delete Step.",
        responses={
            204: serializers.DetailStringSerializer,
            404: serializers.DetailStringSerializer,
        }
    )
    def destroy(self, request: Request, *args, **kwargs):
        step_id = kwargs.get('pk')
        try:
            Step(step_model_id=step_id).delete()
        except core_exceptions.StepObjectDoesNotExist:
            raise exceptions.NotFound()

        return Response({'detail': 'Deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        description="Validate Step YAML.",
        request=serializers.StepValidateSerializer,
        responses={
            200: serializers.DetailStringSerializer,
            400: serializers.DetailStringSerializer
        }
    )
    @action(methods=["post"], detail=False)
    def validate(self, request: Request):
        received_dict = util.load_body_yaml(request.body)

        try:
            Step.validate(received_dict)
        except (yaml.YAMLError, core_exceptions.ValidationError, core_exceptions.StepTypeDoesNotExist) as ex:
            raise exceptions.ValidationError(ex)

        msg = {'detail': "Step is valid."}
        return Response(msg, status=status.HTTP_200_OK)
