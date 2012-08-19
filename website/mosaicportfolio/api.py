from tastypie.resources import ModelResource, Resource, fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from mosaicportfolio.models import User, UserProfile, Project, ProjectRepository, Repository

import graphing
import logging

logger = logging.getLogger(__name__)

class LoggedInAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        return request.user.is_authenticated()

class UserAuthorization(Authorization):
    def is_authorized(self, request, object=None):

        if object is None:
            return True

        return object.pk == request.user.pk

    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(pk=request.user.pk)

        return object_list.none()

class UserResource(ModelResource):
    profile = fields.ToOneField('mosaicportfolio.api.UserProfileResource', 'profile', full=True)

    class Meta:
        queryset = User.objects.all().select_related()
        list_allowed_methods = ['get', 'put']
        detail_allowed_methods = ['get', 'put']

        authentication = LoggedInAuthentication()
        authorization = UserAuthorization()

        fields = ['first_name', 'last_name', 'email', 'id', 'date_joined', 'username']

class UserProfileAuthorization(Authorization):
    def is_authorized(self, request, object=None):

        if object is None:
            return True

        return object.user.pk == request.user.pk

    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(user=request.user)

        return object_list.none()

class UserProfileResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = UserProfile.objects.all()
        list_allowed_methods = ['get', 'put']
        detail_allowed_methods = ['get', 'put']

        authentication = LoggedInAuthentication()
        authorization = UserProfileAuthorization()

class ProjectAuthorization(Authorization):
    def is_authorized(self, request, object=None):

        if object is None:
            return True

        return object.user.pk == request.user.pk

    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(user=request.user)

        return object_list.none()

class ProjectResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = Project.objects.all()
        list_allowed_methods = ['get', 'put', 'post']
        detail_allowed_methods = ['get', 'put', 'post']

        authentication = LoggedInAuthentication()
        authorization = ProjectAuthorization()

class RepositoryAuthorization(Authorization):
    def is_authorized(self, request, object=None):

        if object is None:
            return True

        return object.project.user.pk == request.user.pk

    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(project__user=request.user)

        return object_list.none()

class RepositoryResource(ModelResource):

    project = fields.ToOneField(ProjectResource, 'project')

    url = fields.CharField()
    concrete_type = fields.CharField()

    class Meta:
        queryset = ProjectRepository.objects.all()
        list_allowed_methods = ['get', 'put', 'post']
        detail_allowed_methods = ['get', 'put', 'post']

        authentication = LoggedInAuthentication()
        authorization = RepositoryAuthorization()

    def dehydrate_url(self, bundle):
        return bundle.obj.repository.url

    def dehydrate_concrete_type(self, bundle):
        return bundle.obj.repository.concrete_type

    def hydrate(self, bundle):

        bundle.obj.repository, created = Repository.objects.get_or_create(
            concrete_type = bundle.data['concrete_type'],
            url = bundle.data['url']
        )

        return bundle

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




