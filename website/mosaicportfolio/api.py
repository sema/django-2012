
from tastypie.resources import ModelResource, fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from mosaicportfolio.models import User, UserProfile

class UserResource(ModelResource):
    profile = fields.ToOneField('mosaicportfolio.api.UserProfileResource', 'profile', full=True)

    class Meta:
        queryset = User.objects.all().select_related()
        list_allowed_methods = ['get', 'put']
        detail_allowed_methods = ['get', 'put']

        authentication = Authentication()
        authorization = Authorization()

class UserProfileResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = UserProfile.objects.all()
        list_allowed_methods = ['get', 'put']
        detail_allowed_methods = ['get', 'put']

        authentication = Authentication()
        authorization = Authorization()