# -*- coding: utf-8 -*-

from tastypie.validation import Validation
from models import User
import re
from datetime import datetime



#########################
# USER VALIDATION CLASS #
#########################
class UserValidation(Validation):

	# REGEXS #
	username_regex = '^[a-zA-Z0-9_]*$'
	email_regex = '[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}'
	name_regex = "^[A-Z]'?[-a-zA-Z]+$"
	password_regex = '^.{6,16}$'

	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}

		regex = re.compile(self.username_regex)
		if not regex.match(bundle.data['username']):
			errors['username'] = 'Invalid username'

		regex = re.compile(self.email_regex)
		if not regex.match(bundle.data['email']):
			errors['email'] = 'Invalid email'

		regex = re.compile(self.name_regex)
		if not regex.match(bundle.data['first_name']):
			errors['first_name'] = 'Invalid first name'

		regex = re.compile(self.name_regex)
		if not regex.match(bundle.data['last_name']):
			errors['last_name'] = 'Invalid last name'

		regex = re.compile(self.password_regex)
		if not regex.match(bundle.data['password']):
			errors['password'] = 'Invalid Password'

		username_exists = User.objects.filter(username__iexact = bundle.data['username'])
		if username_exists:
			errors['username'] = 'Invalid username'

		email_exists = User.objects.filter(email__iexact = bundle.data['email'])
		if email_exists:
			errors['email'] = 'Invalid email'

		return errors



##########################
# PHOTO VALIDATION CLASS #
##########################
class PhotoValidation(Validation):
	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}
		acceptable_values = ['True','False']
		if bundle.data['is_enabled'] not in acceptable_values:
			errors['is_enabled'] = 'Invalid value'

		return errors



# ##########################
# # BRAND VALIDATION CLASS #
# ##########################
# class BrandValidation(Validation):
# 	def is_valid(self, bundle, request=None):
# 		if not bundle.data:
# 			return {'__all__': 'Not quite what I had in mind.'}

# 		errors = {}
# 		return errors



#########################
# POST VALIDATION CLASS #
#########################
class PostValidation(Validation):
	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}

		if len(bundle.data['description']) > 140:
			errors['description'] = "Invalid description"
		elif len(bundle.data['description']) < 0:
			errors['description'] = "Invalid description"

		if type(bundle.data['user']) is not int:
			errors['user'] = "Invalid user"
		if type(bundle.data['publish_date']) is not datetime:
			errors['publish_date'] = "Invalid date"
		elif bundle.data['publish_date'] < datetime.now():
			errors['publish_date'] = 'Invalid date'

		if type(bundle.data['pastel']) is not int:
			errors['pastel'] = "Invalid pastel"



		
		return errors



############################
# COMMENT VALIDATION CLASS #
############################
class CommentValidation(Validation):
	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}

		if type(bundle.data['user']) is not int:
			errors['user'] = "Invalid user"
		if type(bundle.data['post']) is not int:
			errors['post'] = "Invalid post"
		if len(bundle.data['content']) > 140:
			errors['content'] = "Invalid content"
		elif len(bundle.data['content']) < 0:
			errors['content'] = "Invalid content"	
		if type(bundle.data['publish_date']) is not datetime:
			errors['publish_date'] = "Invalid date"
		elif bundle.data['publish_date'] < datetime.now():
			errors['publish_date'] = 'Invalid date'

		return errors



#################################
# RELATIONSHIP VALIDATION CLASS #
#################################
class RelationshipValidation(Validation):
	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}

		if type(bundle.data['follower']) is not int:
			errors['follower'] = "Invalid follower"
		if type(bundle.data['following']) is not int:
			errors['following'] = "Invalid following"
		if type(bundle.data['follow_date']) is not datetime:
			errors['follow_date'] = "Invalid date"
		elif bundle.data['follow_date'] < datetime.now():
			errors['follow_date'] = 'Invalid date'

		return errors



#########################
# ITEM VALIDATION CLASS #
#########################
class ItemValidation(Validation):
	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}
		if type(bundle.data['post']) is not int:
			errors['post'] = "Invalid post"

		if len(bundle.data['description']) > 140:
			errors['description'] = "Invalid description"
		elif len(bundle.data['description']) < 0:
			errors['description'] = "Invalid description"
		elif type(bundle.data['description']) is not str:
			errors['description'] = "Invalid description"
		if type(bundle.data['image']) is not str:
			errors['image'] = "Invalid image"
		if type(bundle.data['latitude']) is not int:
			errors['latitude'] = "Invalid latitude"
		if type(bundle.data['longitude']) is not int:
			errors['longitude'] = "Invalid longitude"
		if type(bundle.data['publish_date']) is not datetime:
			errors['publish_date'] = "Invalid date"
		elif bundle.data['publish_date'] < datetime.now():
			errors['publish_date'] = 'Invalid date'

		return errors



#########################
# LIKE VALIDATION CLASS #
#########################
class LikeValidation(Validation):
	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}
		if type(bundle.data['user']) is not int:
			errors['user'] = "Invalid user"
		if type(bundle.data['post']) is not int:
			errors['post'] = "Invalid post"
		return errors



##########################
# LABEL VALIDATION CLASS #
##########################
class LabelValidation(Validation):
	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}

		if type(bundle.data['x']) is not int:
			errors['x'] = "Invalid x-coordinate"
		if type(bundle.data['y']) is not int:
			errors['y'] = "Invalid y-coordinate"
		if type(bundle.data['angle']) is not int:
			errors['angle'] = "Invalid angle"
		if -(180) <= bundle.data['angle'] <= 180:
			errors['angle'] = "Invalid angle"
		if type(bundle.data['colour']) is not str:
			errors['colour'] = "Invalid colour"
		if type(bundle.data['item']) is not int:
			errors['item'] = "Invalid item"
		return errors



########################
# TAG VALIDATION CLASS #
########################
class TagValidation(Validation):
	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}
		if bundle.data['item']:
			if type(bundle.data['item']) is not int:
				errors['item'] = "Invalid item"

		if bundle.data['post']:
			if type(bundle.data['post']) is not int:
				errors['post'] = "Invalid post"

		if type(bundle.data['content']) is not str:
			errors['content'] = "Invalid content"

		return errors



#################################
# NOTIFICATION VALIDATION CLASS #
#################################
class NotificationValidation(Validation):
	def is_valid(self, bundle, request=None):
		if not bundle.data:
			return {'__all__': 'Not quite what I had in mind.'}

		errors = {}
		if type(bundle.data['type']) is not int:
			errors['type'] = "Invalid type"

		if type(bundle.data['user']) is not int:
			errors['user'] = "Invalid user"

		if type(bundle.data['publish_date']) is not datetime:
			errors['publish_date'] = "Invalid date"
		elif bundle.data['publish_date'] < datetime.now():
			errors['publish_date'] = 'Invalid date'

		if type(bundle.data['post']) is not int:
			errors['post'] = "Invalid post"

		if type(bundle.data['is_seen']) is not bool:
			errors['is_seen'] = "Invalid seen"


		return errors