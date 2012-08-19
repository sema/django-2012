
from tastypie.resources import ModelResource, fields

from mosaicportfolio.models import User, UserProfile

class UserProfileResource(ModelResource):

    class Meta:
        model = UserProfile.objects.all()

class UserResource(ModelResource):
    profile = fields.ForeignKey(UserProfileResource, 'profile', full=True)

    class Meta:
        model = User.objects.all().select_related()