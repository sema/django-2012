var User = Backbone.Model.extend({
    urlRoot: '/api/rest/v1/user/'
});

var UserGraph = Backbone.Model.extend({
   urlRoot: '/api/rest/v1/usergraph/'                                   
});

var ProjectGraph = Backbone.Model.extend({
   urlRoot: '/api/rest/v1/projectgraph/'                                   
});

var Project = Backbone.Model.extend({
    urlRoot: '/api/rest/v1/project/'
});

var ApplicationState = Backbone.Model.extend({

});

