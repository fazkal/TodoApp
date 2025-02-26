from rest_framework.routers import DefaultRouter
from .views import TodoTasksApiView

router = DefaultRouter()
router.register('tasks',TodoTasksApiView,basename='tasks')

app_name = "api"

urlpatterns = []
urlpatterns += router.urls