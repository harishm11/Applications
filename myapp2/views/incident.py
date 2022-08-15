from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers  import *

from ..models import *


@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/incident-list/',
		'Detail View':'/incident-detail/<str:pk>/',
		'Create':'/incident-create/',
		'Update':'/incident-update/<str:pk>/',
		'Delete':'/incident-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def incidentList(request):
	incidents = incidentModel.objects.all().order_by('-id')
	serializer = incidentSerializer(incidents, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def incidentDetail(request, pk):
	incidents = incidentModel.objects.get(id=pk)
	serializer = incidentSerializer(incidents, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def incidentCreate(request):
	serializer = incidentSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def incidentUpdate(request, pk):
	incident = incidentModel.objects.get(id=pk)
	serializer = incidentSerializer(instance=incident, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def incidentDelete(request, pk):
	incident = incidentModel.objects.get(id=pk)
	incident.delete()

	return Response('incident deleted!')