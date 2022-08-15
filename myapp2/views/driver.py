from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers  import *

from ..models import *


@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/driver-list/',
		'Detail View':'/driver-detail/<str:pk>/',
		'Create':'/driver-create/',
		'Update':'/driver-update/<str:pk>/',
		'Delete':'/driver-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def driverList(request):
	drivers = driverModel.objects.all().order_by('-id')
	serializer = driverSerializer(drivers, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def driverDetail(request, pk):
	drivers = driverModel.objects.get(id=pk)
	serializer = driverSerializer(drivers, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def driverCreate(request):
	serializer = driverSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def driverUpdate(request, pk):
	driver = driverModel.objects.get(id=pk)
	serializer = driverSerializer(instance=driver, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def driverDelete(request, pk):
	driver = driverModel.objects.get(id=pk)
	driver.delete()

	return Response('Driver deleted!')