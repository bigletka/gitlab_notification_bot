from django.shortcuts import render
from rest_framework import (
    viewsets,
    mixins,
    status,
    generics
 )
import requests
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from gitlab.models import GitLab
from gitlab import serializers
from rest_framework.views import APIView


class GitLabEventsCreateView(generics.CreateAPIView):
    serializer_class = serializers.GitLabBotSerializer
   

class GitLabEventsRetrieveView(APIView):
    serializer_class = serializers.GitLabBotSerializer
 

    def get(self, request, chat_id):
        gitlab = GitLab.objects.get(chat_id = chat_id)
        if not gitlab:
            return Response({'status': 'details'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.GitLabBotSerializer(gitlab)
        return Response(serializer.data)
    
    def patch(self, request, chat_id):
        gitlab = GitLab.objects.get(chat_id = chat_id)
        if not gitlab:
            return Response({'status': 'details'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.GitLabBotSerializer(gitlab, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data="wrong parameters")
    




# def gitlabEvents(request):
   
#     data = fetchData()
    
#     return render(request, 'home.html', {'response' : data})
    



# def fetchData():
#     url = 'https://gitlab.easy-dev.ru/api/v4/projects/8/events'
#     token = 'glpat-fX6f8x_XAaq_Qkb-KiHc'
#     headers = {'PRIVATE-TOKEN': token}
#     response = requests.get(url, headers=headers)
#     data = response.content.decode()
#     return data   






