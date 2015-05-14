# myapp/api.py
# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from models import *
from authentication import OAuth20Authentication, UserOAuth20Authentication
from tastypie.authorization import DjangoAuthorization
from api_serializer import PrettyJSONSerializer as Serializer
from tastypie.authorization import Authorization
from validation import *
from User_Authentication import *
from slug_generator import slugGenerator
from base64 import b64decode
from django.core.files.base import ContentFile
from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS, ALL
from tastypie.fields import FileField
from datetime import datetime
from tastypie.bundle import Bundle

#################
# POST RESOURCE #
#################
class PostResource(ModelResource):
    file_field = fields.CharField(attribute= 'imagePath', null=True)
    file_field = fields.FileField(attribute = "imagePath", null=True)
    user = fields.ToOneField('api.api.PostUserResource',attribute='user', full=True)
    labels = fields.ToManyField('api.api.LabelResource', attribute='labels', full= True, null = True)
    class Meta:
        queryset = Post.objects.prefetch_related('user').all()
        resource_name = 'post'
        authorization = Authorization()
        always_return_data = True
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        list_allowed_methods = ['get', 'post']
        #validation = PostValidation()
        # filter = {'id': ALL,
        # "user": ALL_WITH_RELATIONS}

    def determine_format(self, request):
        return 'application/json'

    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        bundle.data['request_ip'] = bundle.request.META.get('REMOTE_ADDR')
        bundle.data['imagePathString'] = ""
        import logging
        logger = logging.getLogger(__name__)

        logger.debug("test")
        # file_field = getattr(bundle.obj, "imagePath")
        # bundle.data['image'] = file_field.file.read().encode("base64")

        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        #bundle.obj.setSlug(slugGenerator(bundle.data['photo_name']))
        bundle.obj.set_user(User.objects.get(pk=bundle.data.get('userId')))
        bundle.obj.get_user.numPosts += 1
        bundle.obj.get_user.save()
        return bundle

    def hydrate_imagePath(self, bundle):
        image_data = b64decode(bundle.data['imagePathString'])
        bundle.obj.imagePath = ContentFile(image_data, 'blaH.png')
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        user = User.objects.get(pk=bundle.request.GET['userId'])
        user.numPosts -= 1
        user.save()
        post = Post.objects.get(id=bundle.request.GET['postId'])
        post.delete()

#################
# USER RESOURCE #
#################
class UserResource(ModelResource):
    file_field = fields.CharField(attribute= 'profileImagePath',null=True)
    file_field = fields.FileField(attribute= "profileImagePath",null=True)
    posts = fields.ToManyField('api.api.PostResource', attribute='posts', full= True,null = True)
    class Meta:
        include_resource_uri = False
        queryset = User.objects.prefetch_related('posts').all()
        resource_name = 'user'
        authorization = Authorization()
        authentication = UserOAuth20Authentication()
        serializer = Serializer()
        #validation = UserValidation()
        always_return_data = True
        excludes = ['password']
        filtering = {
                    "post" : ALL_WITH_RELATIONS,
                    "username": ALL,
                    "id": ALL}

    def determine_format(self, request):
        return 'application/json'
    
    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        bundle.data['request_ip'] = bundle.request.META.get('REMOTE_ADDR')
        # file_field = getattr(bundle.obj, "profileImagePath")
        # bundle.data['profileImage'] = file_field.file.read().encode("base64")
        if 'password' in bundle.request.GET:
            if not bundle.obj.check_password(bundle.request.GET['password']):
                bundle = {'error': 'Invalid password'}
                return bundle 
            else:
                bundle.data['passwordVerified'] = True
        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        bundle.obj.lastIpAddress = bundle.request.META.get('REMOTE_ADDR')
        #bundle.obj.set_slug(slugGenerator(bundle.data['image_path']))
        if 'password' in bundle.data:
            bundle.obj.set_password(bundle.data['password'])
        return bundle

    def hydrate_profileImagePath(self,bundle):
        image_data = b64decode(bundle.data['profileImage'])
        bundle.obj.profileImagePath = ContentFile(image_data, 'blaH.png')  
        return bundle

"""
Extra resource so both user and post can call 
each other without infinite recursion """

class PostUserResource(ModelResource):
    class Meta:
        include_resource_uri = False
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
        authentication = UserOAuth20Authentication()
        serializer = Serializer()
        #validation = UserValidation()
        always_return_data = True
        excludes = ['password']
        filtering = {
                    "post" : ALL_WITH_RELATIONS}

    def dehydrate(self,bundle):
        bundle.data['request_ip'] = bundle.request.META.get('REMOTE_ADDR')
        # file_field = getattr(bundle.obj, "profileImagePath")
        # bundle.data['profileImage'] = file_field.file.read().encode("base64")
        return bundle

######################
# BETA CODE RESOURCE #
######################
class BetaCodeResource(ModelResource):
    class Meta:
        queryset = BetaCode.objects.all()
        resource_name = 'beta_code'
        authorization = Authorization()
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        #validation = BetaCodeValidation()

    def determine_format(self, request):
        return 'application/json'

    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        return bundle


##################
# SHARE RESOURCE #
##################

class ShareResource(ModelResource):
    class Meta:
        queryset = Share.objects.all()
        resource_name = 'share'
        authorization = Authorization()
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        
    def determine_format(self, request):
        return 'application/json'

    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        bundle.obj.set_post(Post.objects.get(pk=bundle.data.get('postId')))
        bundle.obj.post.numShares += 1
        bundle.obj.post.save()
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        post = Post.objects.get(pk=bundle.request.GET['postId'])
        post.numLikes -= 1
        post.save()
        share = Share.objects.get(id=bundle.request.GET['likeId'])
        share.delete()  

####################
# COMMENT RESOURCE #
####################
class CommentResource(ModelResource):
    post = fields.ForeignKey('api.api.PostResource','post', full=True)
    user = fields.ForeignKey(PostUserResource,'user', full=True)
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        authorization = Authorization()
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        list_allowed_methods = ['get', 'post']
        # validation = CommentValidation()
        always_return_data = True

    def determine_format(self, request):
        return 'application/json'

    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        bundle.obj.set_post(Post.objects.get(pk=bundle.data.get('postId')))
        bundle.obj.get_post.numComments += 1
        bundle.obj.get_post.save()
        return bundle



#########################
# RELATIONSHIP RESOURCE #
#########################
class RelationshipResource(ModelResource):
    follower = fields.ForeignKey(UserResource, 'follower',full= True)
    following = fields.ForeignKey(UserResource, 'following',full = True)
    class Meta:
        queryset = Relationship.objects.select_related('user','post').all()
        resource_name = 'relationship'
        authorization = Authorization()
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        # validation = RelationshipValidation()
        filtering = {
        "follower": ALL_WITH_RELATIONS,
        "following": ALL_WITH_RELATIONS,
        }
        always_return_data = True


    def obj_delete_list(self, bundle, **kwargs):
        following = User.objects.get(pk=bundle.request.GET['following_id'])
        follower = User.objects.get(pk=bundle.request.GET['follower_id'])
        following = User.objects.get(pk=bundle.request.GET['followingId'])
        following.numFollowers -= 1
        follower.numFollowing -= 1
        follower.save()
        following.save()
        r = Relationship.objects.get(following=following,follower=follower)
        r.delete()


    def determine_format(self, request):
        return 'application/json'

    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):

        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        bundle.obj.set_following(User.objects.get(pk=bundle.data.get('followingId')))
        bundle.obj.set_follower(User.objects.get(pk=bundle.data.get('followerId')))
        bundle.obj.get_following().numFollowers += 1
        bundle.obj.get_follower().numFollowing += 1
        bundle.obj.get_follower().save()
        bundle.obj.get_following().save()
        return bundle





#################
# LIKE RESOURCE #
#################
class LikeResource(ModelResource):
    post = fields.ForeignKey('api.api.PostResource','post', full=True)
    user = fields.ForeignKey(PostUserResource,'user', full=True)
    class Meta:
        queryset = Like.objects.all()
        resource_name = 'like'
        authorization = Authorization()
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        # validation = LikeValidation()
        list_allowed_methods = ['get', 'post']
        always_return_data = True
        filtering = {
        "id": ALL,
        }
    
    def determine_format(self, request):
        return 'application/json'

    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        bundle.obj.set_post(Post.objects.get(pk=bundle.data.get('postId')))
        bundle.obj.post.numLikes += 1
        bundle.obj.post.save()
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        post = Post.objects.get(pk=bundle.request.GET['postId'])
        post.numLikes -= 1
        post.save()
        like = Like.objects.get(id=bundle.request.GET['likeId'])
        like.delete()    






##################
# LABEL RESOURCE #
##################
class LabelResource(ModelResource):
    file_field = fields.CharField(attribute= 'imagePath',null=True)
    file_field = fields.FileField(attribute = "imagePath",null=True)
    post = fields.ToOneField(PostResource, 'post')
    class Meta:
        queryset = Label.objects.all()
        resource_name = 'label'
        authorization = Authorization()
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        # validation = LabelValidation()
        always_return_data = True

    def determine_format(self, request):
        return 'application/json'

    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        bundle.data['imagePathString'] = ""
        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        return bundle

    def hydrate_imagePath(self, bundle):
        image_data = b64decode(bundle.data['imagePathString'])
        bundle.obj.imagePath = ContentFile(image_data, 'blaH.png')
        return bundle



#####################
# ITEM TAG RESOURCE #
#####################
class ItemTagResource(ModelResource):
    class Meta:
        queryset = ItemTag.objects.all()
        resource_name = 'item_tag'
        authorization = Authorization()
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        validation = TagValidation()
        list_allowed_methods = ['get', 'post']

    def determine_format(self, request):
        return 'application/json'
    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        return bundle



#####################
# POST TAG RESOURCE #
#####################
class PostTagResource(ModelResource):
    class Meta:
        queryset = PostTag.objects.all()
        resource_name = 'post_tag'
        authorization = Authorization()
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        #validation = TagValidation()
        list_allowed_methods = ['get', 'post']

    def determine_format(self, request):
        return 'application/json'

    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        return bundle



#########################
# NOTIFICATION RESOURCE #
#########################
class NotificationResource(ModelResource):
    class Meta:
        queryset = Notification.objects.all()
        resource_name = 'notification'
        authorization = Authorization()
        #authentication = OAuth20Authentication()
        serializer = Serializer()
        validation = NotificationValidation()
        list_allowed_methods = ['get', 'post']

    def determine_format(self, request):
        return 'application/json'
    # Dehydrate - Requesting Data #
    def dehydrate(self,bundle):
        return bundle

    # Hydrate - Sending Data #
    def hydrate(self, bundle):
        return bundle   # Hydrate - Sending Data #

# ##################
# # BRAND RESOURCE #
# ##################
# class BrandResource(ModelResource):
#     class Meta:
#         queryset = Brand.objects.all()
#         resource_name = 'brand'
#         authorization = Authorization()
#         #authentication = OAuth20Authentication()
#         serializer = Serializer()
#         validation = BrandValidation()
#         list_allowed_methods = ['get', 'post']

#     def determine_format(self, request):
#         return 'application/json'

#     # Dehydrate - Requesting Data #
#     def dehydrate(self,bundle):
#         return bundle

#     # Hydrate - Sending Data #
#     def hydrate(self, bundle):
#         return bundle







#############################
# # SPONSORED POST RESOURCE #
# ###########################
# class SponsoredPostResource(ModelResource):
#     class Meta:
#         queryset = SponsoredPost.objects.all()
#         resource_name = 'sponsored_post'
#         authorization = DjangoAuthorization()
#         authentication = OAuth20Authentication()
#         serializer = Serializer()
#         list_allowed_methods = ['get', 'post']
#         validation = PostValidation()

#   def determine_format(self, request):
#       return 'application/json'
#   # Dehydrate - Requesting Data #
#   def dehydrate(self,bundle):
#       return bundle

#   # Hydrate - Sending Data #
#   def hydrate(self, bundle):
#       return bundle

# ##################
# # PHOTO RESOURCE #
# ##################
# class PhotoResource(ModelResource):
#     class Meta:
#         queryset = Photo.objects.all()
#         resource_name = 'photo'
#         authorization = Authorization()
#         #authentication = OAuth20Authentication()
#         serializer = Serializer()
#         validation = PhotoValidation()
#         list_allowed_methods = ['get', 'post']
        
#     def determine_format(self, request):
#         return 'application/json'

#     # Dehydrate - Requesting Data #
#     def dehydrate(self,bundle):
#         bundle.data['request_ip'] = bundle.request.META.get('REMOTE_ADDR')
#         return bundle

#     # Hydrate - Sending Data #
#     def hydrate(self,bundle):
#         bundle.obj.setIpAddress(bundle.request.META.get('REMOTE_ADDR'))
#         bundle.obj.setSlug(slugGenerator(bundle.data['photo_name']))
#         return bundle

