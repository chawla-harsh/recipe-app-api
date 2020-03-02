from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
	return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
	"""Test the users api (public)"""

	def setUp(self):
		self.client = APIClient()

	def test_create_valid_user_success(self):
		payload = {
		'email': 'test@gmail.com',
		'password': 'test123',
		'name': 'test'
		}

		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		user = get_user_model().objects.get(**res.data)
		self.assertTrue(user.check_password(payload['password']))
		self.assertNotIn('password',res.data)

	def test_duplicate_user_exists(self):
		payload = {
		'email': 'test@gmail.com',
		'password': 'test123',
		'name': 'test'
		}

		create_user(**payload)

		res = self.client.post(CREATE_USER_URL, payload)
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


	def test_password_too_short(self):
		"""Password should me more thane 5 characters"""
		payload = {
		'email': 'test@gmail.com',
		'password': 'pw',
		'name': 'test'
		}

		res = self.client.post(CREATE_USER_URL, payload)
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
		user_exists = get_user_model().objects.filter(
			email = payload['email']
			).exists()

		self.assertFalse(user_exists)

	def test_token_for_user(self):
		"""Test token creation"""
		payload = {
		'email': 'test@gmail.com',
		'password': 'password'
		}

		create_user(**payload)
		res = self.client.post(TOKEN_URL, payload)
		self.assertIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_200_OK)

	def test_token_invalid_credentials(self):
		payload = {
		'email': 'test@gmail.com',
		'password': 'password'
		}
		create_user(**payload)
		res = self.client.post(TOKEN_URL, {'email': 'test@gmail.com', 'password': 'wrong'})

		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

	def test_create_token_no_user(self):
		payload = {
		'email': 'test@gmail.com',
		'password': 'password'
		}

		res = self.client.post(TOKEN_URL, payload)
		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

	def test_token_missing_password(self):
		res = self.client.post(TOKEN_URL, {'email': 'test@gmail.com', 'password':''})
		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

	def test_unauthenticated_user(self):
		res = self.client.get(ME_URL)
		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):

	def setUp(self):
		self.user = create_user(email= 'test@gmail.com', password= 'test123', name= 'test');
		self.client = APIClient()
		self.client.force_authenticate(user = self.user)

	def test_retrieve_profile_success(self):
		res=self.client.get(ME_URL)

		self.assertEqual(res.status_code,status.HTTP_200_OK)
		self.assertEqual(res.data, {
			'name': self.user.name,
			'email': self.user.email
			})

	def test_post_not_allowed(self):
		res = self.client.post(ME_URL, {})

		self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_update_user_profile(self):
		payload = {'name': 'newname'}

		res = self.client.patch(ME_URL, payload)

		self.user.refresh_from_db()
		self.assertEqual(self.user.name, payload['name'])
		self.assertEqual(res.status_code, status.HTTP_200_OK)

