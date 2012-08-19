from tastypie.resources import ModelResource, fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from mosaicportfolio.models import User, UserProfile, Project
from tastypie.bundle import Bundle
from tastypie.resources import Resource, ModelResource, fields
import graphing
import logging

logger = logging.getLogger(__name__)

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
class GraphObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data    
class AbstractGraphResource(Resource):
    title = fields.CharField(attribute='title')
    hTitle = fields.CharField(attribute='hTitle')
    vTitle = fields.CharField(attribute='vTitle')
    table = fields.ListField(attribute='table')
    
    class Meta:
        include_resource_uri = False

class UserGraphResource(AbstractGraphResource):
    class Meta:
        allowed_methods = ['get']
        resource_name = 'usergraph'
        
    def obj_get(self, request=None, **kwargs):
        return GraphObject(initial = graphing.make_user_graph(User.objects.get(pk=kwargs['pk'])))

class ProjectGraphResource(AbstractGraphResource):
    class Meta:
        allowed_methods = ['get']
        resource_name = 'projectgraph'
        
    def obj_get(self, request=None, **kwargs):
        return GraphObject(initial = graphing.make_project_graph(Project.objects.get(pk=kwargs['pk'])))
