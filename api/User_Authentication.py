from models import User


class User_Authentication(object):

	def authenticate(self, username=None, password=None):
		login_valid = User.objects.filter(username__iexact = username).count()
		password_valid = User.check_password(password, User.objects.get(username=username))
		if login_valid and password_valid:
			try:
				user = User.objects.get(username=username)
			except User.DoesNotExist:
				return False
			return user
		return False

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
