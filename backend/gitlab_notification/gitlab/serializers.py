from rest_framework import serializers
from gitlab.models import GitLab

class GitLabBotSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GitLab
        fields = '__all__'
    
    
    
