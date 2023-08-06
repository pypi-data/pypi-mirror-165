from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from cryton_core.cryton_app.views import PlanViews, StageViews, StepViews, RunViews, PlanExecutionViews, \
    StageExecutionViews, StepExecutionViews, ExecutionVariableViews, WorkerViews, LogViews, PlanTemplateViews


router = routers.DefaultRouter()
router.register(r'runs', RunViews.RunViewSet)
router.register(r'plans', PlanViews.PlanViewSet)
router.register(r'plan_executions', PlanExecutionViews.PlanExecutionViewSet)
router.register(r'stages', StageViews.StageViewSet)
router.register(r'stage_executions', StageExecutionViews.StageExecutionViewSet)
router.register(r'steps', StepViews.StepViewSet)
router.register(r'step_executions', StepExecutionViews.StepExecutionViewSet)
router.register(r'workers', WorkerViews.WorkerViewSet)
router.register(r'templates', PlanTemplateViews.PlanTemplateViewSet)
router.register(r'execution_variables', ExecutionVariableViews.ExecutionVariableViewSet)
router.register(r'logs', LogViews.LogViewSet, "log")


urlpatterns = [
    path('', router.get_api_root_view()),
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),
]
