from rest_framework import generics, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

class CreateUserView(generics.CreateAPIView):
	"""Create a new user"""

	serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
	"""Create New Auth Token for User"""
	serializer_class = AuthTokenSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
	"""Manage the authenticated users"""

	serializer_class = UserSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = [IsAuthenticated]

	def get_object(self):
		"""Retrieve and return authenticated user"""
		return self.request.user

