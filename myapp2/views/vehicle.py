from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers  import *

from ..models import *


@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/vehicle-list/',
		'Detail View':'/vehicle-detail/<str:pk>/',
		'Create':'/vehicle-create/',
		'Update':'/vehicle-update/<str:pk>/',
		'Delete':'/vehicle-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def vehicleList(request):
	vehicles = vehicleModel.objects.all().order_by('-id')
	serializer = vehicleSerializer(vehicles, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def vehicleDetail(request, pk):
	vehicles = vehicleModel.objects.get(id=pk)
	serializer = vehicleSerializer(vehicles, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def vehicleCreate(request):
	serializer = vehicleSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def vehicleUpdate(request, pk):
	vehicle = vehicleModel.objects.get(id=pk)
	serializer = vehicleSerializer(instance=vehicle, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def vehicleDelete(request, pk):
	vehicle = vehicleModel.objects.get(id=pk)
	vehicle.delete()

	return Response('vehicle deleted!')