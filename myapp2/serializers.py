from rest_framework import serializers
from .models import *

class driverSerializer(serializers.ModelSerializer):
	class Meta:
		model = driverModel
		fields ='__all__'


class vehicleSerializer(serializers.ModelSerializer):
	class Meta:
		model = vehicleModel
		fields ='__all__'


class policySerializer(serializers.ModelSerializer):
	class Meta:
		model = policyModel
		fields ='__all__'

class incidentSerializer(serializers.ModelSerializer):
	class Meta:
		model = incidentModel
		fields ='__all__'