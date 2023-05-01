import random

from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from .models import *

class driverSerializer(serializers.ModelSerializer):
	quote = serializers.ReadOnlyField(source='quoteModel.quoteNumber')
	class Meta:
		model = driverModel
		fields ='__all__'

		def get_quote(self, obj):
			return obj.quotemodel


class vehicleSerializer(serializers.ModelSerializer):
	class Meta:
		model = vehicleModel
		fields ='__all__'


class quoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = quoteModel
		fields ='__all__'


class incidentSerializer(serializers.ModelSerializer):
	class Meta:
		model = incidentModel
		fields ='__all__'

class quoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = quoteModel
		fields ='__all__'