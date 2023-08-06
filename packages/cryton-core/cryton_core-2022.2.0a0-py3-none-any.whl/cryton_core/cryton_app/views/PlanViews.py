import yaml

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

from cryton_core.cryton_app import util, serializers, exceptions
from cryton_core.cryton_app.models import PlanModel, PlanTemplateModel, RunModel, WorkerModel
from cryton_core.lib.util import util as core_util, exceptions as core_exceptions, creator
from cryton_core.lib.models.plan import Plan, PlanExecution


@extend_schema_view(
    list=extend_schema(description="List Plans.", parameters=[serializers.ListSerializer]),
    retrieve=extend_schema(description="Get existing Plan."),
)
class PlanViewSet(util.InstanceFullViewSet):
    """
    Plan ViewSet.
    """
    queryset = PlanModel.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = serializers.PlanSerializer

    @extend_schema(
        description="Create new Plan. There is no limit or naming convention for inventory files.",
        request=serializers.PlanCreateSerializer,
        examples=[
            OpenApiExample(
                "Multiple files upload",
                description="Uploading multiple inventory files.",
                value={
                    'template_id': 1,
                    'file1': "file content",
                    'file2': "file content",
                },
                request_only=True
            )
        ],
        responses={
            201: serializers.CreateDetailSerializer,
            400: serializers.DetailStringSerializer,
            404: serializers.DetailStringSerializer,
            500: serializers.DetailStringSerializer,
        }
    )
    def create(self, request: Request, **kwargs):
        # Get plan template ID from request
        try:
            template_id = int(request.data['template_id'])
        except (KeyError, ValueError, TypeError) as ex:
            raise exceptions.ValidationError(ex)

        # Read Plan template
        try:
            plan_template_obj = PlanTemplateModel.objects.get(id=template_id)
        except PlanTemplateModel.DoesNotExist:
            raise exceptions.NotFound(f"Nonexistent template_id: {template_id}.")

        with open(str(plan_template_obj.file.path)) as temp:
            plan_template = temp.read()

        # Get inventory files from request and load them
        inventory_variables = {}
        for inventory_file in request.FILES.values():
            try:
                inventory_variables.update(core_util.parse_inventory_file(inventory_file.read()))
            except ValueError as ex:
                raise exceptions.ValidationError(f"Cannot read inventory file. Original exception: {ex}. "
                                                 f"Inventory file: {inventory_file}.")

        # Either fill the Plan template or consider the template already filled
        if inventory_variables != {}:
            try:
                filled_plan_template = core_util.fill_template(plan_template, inventory_variables)
            except core_exceptions.PlanValidationError as ex:
                raise exceptions.ValidationError(f"File is not a Template, original exception: {ex}")
        else:
            filled_plan_template = plan_template

        # Create Plan Instance
        try:  # yaml.safe_load also discovers (in this case) unfilled Jinja variables
            plan_obj_id = creator.create_plan(yaml.safe_load(filled_plan_template))
        except (yaml.YAMLError, AttributeError) as ex:
            raise exceptions.ParseError(f"Couldn't load the final template, original exception: {ex}")
        except (core_exceptions.ValidationError, core_exceptions.CreationFailedError) as ex:
            raise exceptions.ValidationError(f"Couldn't create Plan from template, original exception: {ex}")

        msg = {'id': plan_obj_id, 'detail': 'Plan created.'}
        return Response(msg, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Delete Plan.",
        responses={
            204: serializers.DetailStringSerializer,
            404: serializers.DetailStringSerializer,
        }
    )
    def destroy(self, request: Request, *args, **kwargs):
        plan_id = kwargs.get('pk')
        try:
            Plan(plan_model_id=plan_id).delete()
        except core_exceptions.PlanObjectDoesNotExist:
            raise exceptions.NotFound()

        return Response({'detail': 'Deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        description="Validate Plan YAML.",
        request=serializers.PlanValidateSerializer,
        responses={
            200: serializers.DetailStringSerializer,
            400: serializers.DetailStringSerializer,
        }
    )
    @action(methods=["post"], detail=False)
    def validate(self, request: Request):
        received_dict = util.load_body_yaml(request.body)
        try:
            Plan.validate(received_dict.get('plan'))
        except (yaml.YAMLError, AttributeError, core_exceptions.ValidationError) as ex:
            raise exceptions.ValidationError(f"Plan is not valid. Original error: {ex}")

        msg = {'detail': "Plan is valid."}
        return Response(msg, status=status.HTTP_200_OK)

    @extend_schema(
        description="Create new PlanExecution and execute it.",
        request=serializers.PlanExecuteSerializer,
        responses={
            200: serializers.DetailStringSerializer,
            400: serializers.DetailStringSerializer
        }
    )
    @action(methods=["post"], detail=True)
    def execute(self, request: Request, **kwargs):
        plan_id = kwargs.get("pk")
        try:
            run_id = int(request.data['run_id'])
            worker_id = int(request.data['worker_id'])
        except (KeyError, ValueError, TypeError) as ex:
            raise exceptions.ValidationError(f"Wrong input. Original error: {ex}")

        if not PlanModel.objects.filter(id=plan_id).exists():
            raise exceptions.ValidationError(f"Wrong 'plan_id'.")
        if not WorkerModel.objects.filter(id=worker_id).exists():
            raise exceptions.ValidationError(f"Wrong 'worker_id'.")
        if not RunModel.objects.filter(id=run_id).exists():
            raise exceptions.ValidationError(f"Wrong 'run_id'.")

        plan_exec = PlanExecution(plan_model_id=plan_id, worker_id=worker_id, run_id=run_id)
        plan_exec.execute()

        msg = {'detail': f'PlanExecution with ID {plan_exec.model.id} successfully created and executed.'}
        return Response(msg, status=status.HTTP_200_OK)

    @extend_schema(
        description="Get Plan's YAML.",
        responses={
            200: serializers.DetailDictionarySerializer,
            404: serializers.DetailStringSerializer
        }
    )
    @action(methods=["get"], detail=True)
    def get_plan(self, _, **kwargs):
        plan_id = kwargs.get("pk")
        try:
            plan_dict = core_util.get_plan_yaml(plan_id)
        except PlanModel.DoesNotExist:
            raise exceptions.NotFound(f"Plan with ID {plan_id} does not exist.")

        msg = {"detail": plan_dict}
        return Response(msg, status=status.HTTP_200_OK)
