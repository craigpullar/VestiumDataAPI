# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location='', base_url='')

###############
# PHOTO MODEL #
###############

""" Photo model to store information
	on all the photos in the system """

class Photo(models.Model):


	# FIELDS #
	slug = models.CharField(max_length= 32)
	image = models.FileField(upload_to='/photos/')
	enabled = models.BooleanField(default=True)

	# GETTERS & SETTERS #
	def get_slug(self):
		return self.slug

	def set_slug(self,slug):
		self.slug = slug

	def get_image_path(self):
		return self.image

	def set_image_path(self,image_path):
		self.image = image_path

	def is_enabled(self):
		return self.isEnabled

	def set_enabled(self,enabled):
		self.enabled = enabled

	# REPRESENTATION #	
	def  __unicode__(self):
		return "%s - %s" % (self.getSlug(),self.getImagePath(),self.isEnabled())



###############
# USER MODELS #
###############

""" user model for system. Everyone who wants
	to use the app will have one of these """

class User(User):

	# UPLOAD PATH #
	def upload_to_profile():
		return 'mediafiles/user_images/profile_images/'

	def upload_to_cover():
		return 'mediafiles/user_images/cover_images/'

	# FIELDS #
	lastIpAddress = models.IPAddressField(blank = True)
	profileImageSlug = models.CharField(null = True, blank = True, max_length= 32)
	profileImagePath = models.FileField(null = True, blank = True,upload_to=upload_to_profile(),storage=fs)
	dateJoined = models.DateTimeField(auto_now_add=True, blank = True)
	blogEnabled = models.BooleanField(default=False)
	numFollowers = models.IntegerField(default=0)
	numPosts = models.IntegerField(default=0)
	numFollowing = models.IntegerField(default=0)
	coverImageSlug = models.CharField(null = True, blank = True, max_length= 32)
	coverImagePath = models.FileField(null = True, blank = True,upload_to=upload_to_cover(),storage=fs)

	#objects = BaseUserManager()

	# GETTERS & SETTERS #
	def get_last_ip_address(self):
		return self.ipAddress

	def set_last_ip_address(self,IpAddress):
		self.ipAddress = IpAddress

	def get_profile_image_slug(self):
		return self.profileImageSlug

	def set_profile_image_slug(self,slug):
		self.profileImageSlug = slug

	def get_profile_image_path(self):
		return self.profileImagePath

	def set_profile_image_path(self,image_path):
		self.profileImagePath = image_path

	def is_blog_enabled(self):
		return self.blogEnabled

	def set_blog_enabled(self,enabled):
		self.blogEnabled = enabled

	# REPRESENTATION #	
	def  __unicode__(self):
		return "%s" % (self.get_username())



##############
# BETA CODES #
##############

""" Model to store beta codes and their
	relevant user """

class BetaCode(models.Model):

	# FIELDS #
	user = models.ForeignKey(User)
	code = models.CharField(max_length=20)

	# GETTERS & SETTERS #
	def get_user(self):
		return self.user

	def set_user(self,user):
		self.user = user

	def get_code(self):
		return self.code

	def set_code(self,code):
		self.code = code

	def __unicode__(self):
		return "%s" % (self.get_code())

################
# BRAND MODEL #
################

""" Model for brands so they can be attatched to
items. This will be expanded upon when buy/sell 
comes in """

class Brand(models.Model):

	# FIELDS #
	name = models.CharField(max_length = 255)
	country = models.CharField(max_length = 255)
	website = models.CharField(max_length = 255)
	description = models.TextField()

	# GETTERS & SETTERS #
	def get_name(self):
		return self.name

	def set_name(self, name):
		self.name = name

	def get_country(self):
		return self.country

	def set_country(self,country):
		self.country = country

	def get_website(self):
		return self.website

	def set_website(self,website):
		self.website = website

	def get_description(self):
		return self.description

	def set_description(self,description):
		self.description = description

	# REPRESENTATION #	
	def  __unicode__(self):
		return "%s" % (self.get_name(),self.get_website())



##############
# POST MODEL #
##############

""" Model for all posts in the system. Generated
	by users when they upload an image """

class Post(models.Model):
	class Meta:
		get_latest_by = 'pubDate'

	# UPLAOD PATH #
	def upload_to():
		return 'user_images/post/images/'

	# FIELDS #
	imageSlug = models.CharField(null = True, blank = True, max_length= 32)
	imagePath = models.FileField(null = True, blank = True,upload_to=upload_to())
	description = models.CharField(max_length=140)
	user = models.ForeignKey(User,unique = False, related_name='posts')
	pubDate = models.DateTimeField(auto_now_add=True)
	pastel = models.IntegerField()
	numLikes = models.IntegerField(default=0)
	numComments = models.IntegerField(default=0)
	numShares = models.IntegerField(default=0)
	flagged = models.BooleanField(default = False,blank=True)

	# GETTERS & SETTERS #
	def get_photo(self):
		return self.imagePath.name

	def set_photo(self,photo):
		self.imagePath = photo

	def get_description(self):
		return self.description

	def set_description(self,description):
		self.decsription = description

	def get_user(self):
		return self.user

	def set_user(self,user):
		self.user = user

	def get_publish_date(self):
		return self.pubDate

	def set_publish_date(self,pub_date):
		self.pubDate = pub_date

	def get_pastel(self):
		return self.pastel

	def set_pastel(self,pastel):
		self.pastel = pastel

	def get_num_likes(self):
		return self.numLikes

	def set_num_likes(self,num_likes):
		self.numLikes = num_likes

	def get_num_comments(self):
		return self.numComments

	def set_num_comments(self,num_comments):
		self.numComments = num_comments

	def is_flagged(self):
		return self.flagged

	def set_flagged(self,flagged):
		self.flagged = flagged

	# REPRESENTATION #	
	def  __unicode__(self):
		return "%s %s %s " % (self.get_photo(),self.get_user(),self.get_publish_date())



########################
# SPONSORED POST MODEL #
########################

""" Model for a sponsored post. This will
	include the brand information the post
	is sponsoring """

class SponsoredPost(Post):

	# FIELDS #
	brand = models.ForeignKey(Brand)

	# GETTERS & SETTERS #
	def get_brand(self):
		return self.brand

	def set_brand(self,brand):
		self.brand = brand

	# REPRESENTATION #	
	def  __unicode__(self):
		return "%s" % (self.get_photo().get_slug(),self.get_user(),self.get_publish_date(),self.get_brand())



##################
# COMMENT MODELS #
##################

""" Model for comments on a post"""

class Comment(models.Model):

	# FIELDS #
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	content = models.CharField(max_length = 140)
	pubDate = models.DateTimeField(auto_now_add=True , blank = True)

	# GETTERS & SETTERS #
	def get_user(self):
		return self.user

	def set_user(self,user):
		self.user = user

	def get_post(self):
		return self.post

	def set_post(self,post):
		self.post = post

	def get_context(self):
		return self.context

	def set_context(self,context):
		self.context = context

	def get_publish_date(self):
		return self.pubDate

	def set_publish_date(self,pub_date):
		self.pubDate = pub_date

	# # REPRESENTATION #	
	# def  __unicode__(self):
	# 	return "%s" % (self.get_user().get_username(),self.get_post(),self.get_publish_date()(),self.get_context())



#######################
# RELATIONSHIP MODELS #
#######################

""" A model for defining who is following who.
	Follower -> Following """

class Relationship(models.Model):

	# FIELDS #
	follower = models.ForeignKey(User, related_name = 'relationship_follower')
	following = models.ForeignKey(User,  related_name = 'relationship_following')
	followDate = models.DateTimeField(auto_now_add=True, null=True)

	# GETTERS & SETTERS #
	def get_follower(self):
		return self.follower

	def set_follower(self,follower):
		self.follower = follower

	def get_following(self):
		return self.following

	def set_following(self,following):
		self.following = following

	def get_follow_date(self):
		return self.followDate

	def set_follow_date(self,follow_date):
		self.followDate = follow_date

	# REPRESENTATION #	
	def  __unicode__(self):
		return "{0}{1}{2}".format(self.get_follower().get_username(),self.get_following().get_username(),self.get_follow_date())



##############
# LIKE MODEL #
##############

""" A class for defining who has liked
	which post on the app. """

class Like(models.Model):

	# FIELDS #
	post = models.ForeignKey(Post)
	user = models.ForeignKey(User)

	# GETTERS & SETTERS #
	def get_post(self):
		return self.post

	def set_post(self,post):
		self.post = post

	def get_user(self):
		return self.user

	def set_user(self, user):
		self.user = user

	# # REPRESENTATION #	
	# def  __unicode__(self):
	# 	return "{0}{1}".format(self.get_post().get_description(), self.get_user().get_username())

###############
# SHARE MODEL #
###############

""" A class for defining who has 
	shared what post on the app. """

class Share(models.Model):

	# FIELDS #
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)

	# GETTERS & SETTERS #
	def get_user(self):
		return self.user

	def set_user(self,user):
		self.user = user

	def get_post(self):
		return self.post

	def set_post(self,post):
		self.post = post

################
# LABEL MODELS #
################

""" A class for a label, defining it's postion,
	angle and colour. As well as referencing 
	the photo it is attached to """

class Label(models.Model):

	# FIELDS #
	x = models.IntegerField()
	y = models.IntegerField()
	angle = models.IntegerField()
	colour = models.CharField(max_length = 10, default = 'black', blank=True)
	name = models.CharField(max_length = 255)
	description = models.TextField()
	link = models.CharField(max_length=20)
	imageSlug = models.CharField(null = True, blank = True, max_length= 32)
	imagePath = models.FileField(null = True, blank = True,upload_to='user_images/item_images/')
	#brand = models.ForeignKey(Brand)
	pubDate = models.DateTimeField(auto_now_add= True, blank = True)
	post = models.ForeignKey(Post, related_name='labels')

	# GETTERS & SETTERS #
	def get_photo(self):
		return self.photo

	def set_photo(self,photo):
		self.photo = photo

	def get_x(self):
		return self.x

	def set_x(self,x):
		self.x = x

	def get_y(self):
		return self.y

	def set_y(self, y):
		self.y = y

	def get_angle(self):
		return self.angle

	def set_angle(self,angle):
		self.angle = angle

	def get_colour(self):
		return self.colour

	def set_colour(self,colour):
		self.colour = colour

	def get_name(self):
		return self.name

	def set_name(self,name):
		self.name = name

	def get_description(self):
		return self.description

	def set_description(self,description):
		self.description = description

	def get_link(self):
		return self.link

	def set_link(self,link):
		self.link = link

	def get_geo_position(self):
		return self.geoPosition

	def set_geo_position(self,geo_position):
		self.geoPosition = geo_position

	def get_publish_date(self):
		return self.pubDate

	def set_publish_date(self,pub_date):
		self.pubDate = pub_date


	# # REPRESENTATION #	
	# def  __unicode__(self):
	# 	return "{0}{1}{2}{3}".format(self.post.id,self.get_x(),self.get_y(),self.get_angle())



##################
# ITEM TAG MODEL #
##################

""" A model for defining text tags for items. """

class ItemTag(models.Model):

	# FIELDS #
	label = models.ForeignKey(Label)
	content = models.CharField(max_length=63)

	# GETTERS & SETTERS #
	def get_item(self):
		return self.item

	def set_item(self,item):
		self.item = item

	def get_context(self):
		return self.context

	def set_context(self,context):
		self.context = context

	# REPRESENTATION #	
	def  __unicode__(self):
		return "%s" % (self.get_item().get_name(),self.get_context())



##################
# POST TAG MODEL #
##################

""" A model for defining text tags for posts. """

class PostTag(models.Model):

	# FIELDS #
	post = models.ForeignKey(Post)
	content = models.CharField(max_length = 63)

	# GETTER & SETTERS #
	def get_post(self):
		return self.post

	def set_post(self,post):
		self.post = post

	def get_context(self):
		return self.context

	def set_context(self,context):
		self.context = context


	# REPRESENTATION #	
	def  __unicode__(self):
		return "%s" % (self.get_post().get_description(),self.get_context())



#####################
# NOTIFCATION TYPES #
#####################

""" A model for storing the different types 
	of notifications and their messages """

class NotificationType(models.Model):

	# FIELDS #
	name = models.CharField(max_length = 255)
	message = models.CharField(max_length = 255)

	# GETTERS & SETTERS #
	def get_name(self):
		return self.name

	def set_name(self,name):
		self.name = name

	def get_message(self):
		return self.message

	def set_message(self,message):
		self.message = message

	# REPRESENTATION #
	def __unicode__(self):
		return ' %s ' % (self.get_name(), self.get_message())



################
# NOTIFICATION #
################

""" A model for storing a users notification """

class Notification(models.Model):

	# FIELDS #
	type = models.ForeignKey(NotificationType)
	user = models.ForeignKey(User)
	pubDate = models.DateTimeField(auto_now_add= True, blank = True)
	post = models.ForeignKey(Post)
	seen = models.BooleanField()

	# GETTERS & SETTERS #
	def get_type(self):
		return self.type

	def set_type(self,type):
		self.type = type

	def get_user(self):
		return self.user

	def set_user(self,user):
		self.user = user

	def get_publish_date(self):
		return self.pubDate

	def set_publish_date(self, pub_date):
		self.pubDate = pub_date

	def get_post(self):
		return self.post

	def set_post(self,post):
		self.post = post

	def is_seen(self):
		return self.seen

	def set_seen(self,seen):
		self.seen = seen

	# REPRESENTATION #
	def __unicode__(self):
		return '%s' % (self.get_type(),self.get_user())



###################
# LOGIN LOG MODEL #
###################

""" A model for logging everytime a user logs
	into the app. """

class LoginLog(models.Model):

	# FIELDS #
	user = models.ForeignKey(User)
	loginDate = models.DateTimeField(auto_now_add=True, blank=True)
	ipAddress = models.IPAddressField(blank = True,validators=[ 
			RegexValidator(
				regex = '\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
				message = 'IP Address did not pass validation',
				code = 'invalid_ip_address')
		])

	# GETTERS & SETTERS #
	def get_user(self):
		return self.user

	def set_user(self,user):
		self.user = user

	def get_login_date(self):
		return self.loginDate

	def set_login_date(self,login_date):
		self.loginDate = login_date

	def get_ip_address(self):
		return self.ipAddress

	def set_ip_address(self,address):
		self.ipAddress = address

	# REPRESENTATION #	
	def  __unicode__(self):
		return "%s" % (self.get_user().get_name(),self.get_login_date())



####################
# LOGOUT LOG MODEL #
####################

""" A model for logging everytime a user logs
	out of the app. """

class LogoutLog(models.Model):

	# FIELDS #
	user = models.ForeignKey(User)
	logoutDate = models.DateTimeField(auto_now_add=True, blank=True)

	# GETTERS & SETTERS #
	def get_user(self):
		return self.user

	def set_user(self,user):
		self.user = user

	def get_logout_date(self):
		return self.logoutDate

	def set_logout_date(self,logout_date):
		self.logoutDate = logout_date

	# REPRESENTATION #	
	def  __unicode__(self):
		return "%s" % (self.get_user().get_name(),self.get_logout_date())



######################
# BLOG ARTICLE MODEL #
######################

class Article(models.Model):

	# FIELDS #
	user = models.ForeignKey(User)
	title = models.CharField(max_length=255)
	content = models.TextField()
	pubDate = models.DateTimeField(auto_now_add=True)
	photos = models.ManyToManyField(Photo, null = True)
	background_image = models.FileField(upload_to='blog_images/')
	background_image_slug = models.CharField(max_length=63)

	# GETTERS & SETTERS #
	def get_user(self):
		return self.user

	def set_user(self,user):
		self.user = user

	def get_title(self):
		return self.title

	def set_title(self,title):
		self.title = title

	def get_content(self):
		return self.content

	def set_content(self,content):
		self.content = content

	def get_publish_date(self):
		return self.pubDate

	def set_publish_date(self,date):
		self.pubDate = date

	def get_Photos(self):
		return self.photos

	def set_photos(self,photos):
		self.photos = photos

	def get_background_image(self):
		return self.background_image

	def set_background_image(self,image):
		self.background_image = image

	def get_background_image_slug(self):
		return self.background_image_slug

	def set_background_image_slug(self,slug):
		self.background_image_slug = slug



######################
# BLOG COMMENT MODEL #
######################

class BlogComment(models.Model):

	# FIELDS #
	user = models.ForeignKey(User)
	article = models.ForeignKey(Article)
	content = models.CharField(max_length=255)
	pubDate = models.DateTimeField(auto_now_add=True)

	# GETTERS & SETTERS #
	def get_user(self):
		return self.user

	def set_user(self,user):
		self.user = user

	def get_article(self):
		return self.article

	def set_article(self,article):
		self.article = article

	def get_content(self):
		return self.content

	def set_content(self,content):
		self.content = content

	def get_publish_date(self):
		return self.pubDate

	def set_publish_date(self,date):
		self.pubDate = date