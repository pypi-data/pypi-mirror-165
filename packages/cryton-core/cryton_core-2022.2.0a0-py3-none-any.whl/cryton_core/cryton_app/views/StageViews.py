import yaml

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, extend_schema_view

from cryton_core.cryton_app import util, serializers, exceptions
from cryton_core.cryton_app.models import StageModel
from cryton_core.lib.util import exceptions as core_exceptions
from cryton_core.lib.models.stage import Stage


@extend_schema_view(
    list=extend_schema(description="List Stages.", parameters=[serializers.ListSerializer]),
    retrieve=extend_schema(description="Get existing Stage."),
)
class StageViewSet(util.InstanceViewSet):
    """
    Stage ViewSet.
    """
    queryset = StageModel.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = serializers.StageSerializer

    @extend_schema(
        description="Delete Stage.",
        responses={
            204: serializers.DetailStringSerializer,
            404: serializers.DetailStringSerializer,
        }
    )
    def destroy(self, request: Request, *args, **kwargs):
        stage_id = kwargs.get('pk')
        try:
            Stage(stage_model_id=stage_id).delete()
        except core_exceptions.StageObjectDoesNotExist:
            raise exceptions.NotFound()

        return Response({'detail': 'Deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        description="Validate Stage YAML.",
        request=serializers.StageValidateSerializer,
        responses={
            200: serializers.DetailStringSerializer,
            400: serializers.DetailStringSerializer
        }
    )
    @action(methods=["post"], detail=False)
    def validate(self, request: Request):
        received_dict = util.load_body_yaml(request.body)

        try:
            Stage.validate(received_dict)
        except (yaml.YAMLError, core_exceptions.ValidationError) as ex:
            raise exceptions.ValidationError(ex)

        msg = {'detail': 'Stage is valid.'}
        return Response(msg, status=status.HTTP_200_OK)
