from rest_framework import serializers
from todo.models import Task
from accounts.models import Profile

class TaskSerializer(serializers.ModelSerializer):
    absolute_url = serializers.HyperlinkedIdentityField(
        view_name='todo:api:tasks-detail',lookup_field='pk')

    class Meta:
        model = Task
        fields = ['id','title','complete','absolute_url','user']
        read_only_fields = ['user']

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('absolute_url',None)
        return rep
    
    def create(self, validated_data):
        validated_data['user'] = Profile.objects.get(user__id=self.context.get('request').user.id)
        return super().create(validated_data)