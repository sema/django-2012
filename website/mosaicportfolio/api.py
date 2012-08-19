
from tastypie.resources import ModelResource, fields

from mosaicportfolio.models import User, UserProfile

class UserResource(ModelResource):
    profile = fields.ToManyField('mosaicportfolio.api.UserProfileResource', 'profile', full=True)

    class Meta:
        queryset = User.objects.all().select_related()

class UserProfileResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = UserProfile.objects.all()