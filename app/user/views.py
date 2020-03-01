from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
	"""Create a new user"""

	serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
	"""Create New Auth Token for User"""
	serializer_class = AuthTokenSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES	
