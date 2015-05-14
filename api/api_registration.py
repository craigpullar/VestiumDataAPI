from api import *
from tastypie.api import Api

#################################
# REGISTER RESOURCES FOR API V1 #
#################################

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
# v1_api.register(PhotoResource())
#v1_api.register(BrandResource())
v1_api.register(PostResource())
#v1_api.register(SponsoredPostResource())
v1_api.register(CommentResource())
v1_api.register(RelationshipResource())
# v1_api.register(ItemResource())
v1_api.register(LikeResource())
v1_api.register(LabelResource())
v1_api.register(ItemTagResource())
v1_api.register(PostTagResource())
v1_api.register(NotificationResource())
