from .serializers import TaskSerializer
from todo.models import Task
from accounts.models import Profile
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class TodoTasksApiView (viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["id", "complete"]
    search_fields = ["title"]
    ordering_fields = ["id","title"]

    def get_queryset(self):
        user_profile = Profile.objects.get(user=self.request.user)
        return Task.objects.filter(user=user_profile)
    

''' If we used ViewSet and DefaultRouter we should defined below functions
from rest_framework.response import Response
    def list(self, request):
        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    
    def get_object(self, queryset=None):  
        obj = get_object_or_404(Task,id=self.kwargs["todo_id"])
        return obj

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.delete()
        return Response({"detail": "successfully removed"},status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = TaskSerializer(
            data=request.data, instance=object, many=False
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)'''