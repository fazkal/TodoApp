from rest_framework.routers import DefaultRouter
from .views import TodoListApiView,TodoDetailApiView

router = DefaultRouter()
router.register('task-list',TodoListApiView,basename='task-list')
router.register('task-detail', TodoDetailApiView, basename='task-detail')

urlpatterns = []
urlpatterns += router.urls