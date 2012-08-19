
var RepositoryView = Backbone.View.extend({

    projectUri: null,
    applicationState: null,

    initialize: function(options) {
        this.id = this.$('.repository-id').val();

        this.projectModel = options.projectModel;

        this.applicationState = options.applicationState;
        this.applicationState.on('change', this.render, this);

        this.projectModel.on('save', this.save, this);
    },

    render: function() {
        if (this.applicationState.get('editMode')) {
            this.$el.show();
        } else {
            this.$el.hide();
        }

    },

    save: function() {
        if (this.$('.repository-url').val() == '' || this.$('.repository-login').val() == '') {
            return;
        }

        console.log('saving');
        console.log(this.projectModel.get('resource_uri'));

        var repository = new Repository({
            url: this.$('.repository-url').val(),
            concrete_type: this.$('.repository-type').val(),
            login: this.$('.repository-login').val(),
            project: this.projectModel.get('resource_uri')
        });

        if (this.id != undefined) {
            repository.set('resource_uri', '/api/rest/v1/repository/' + this.id + '/');
            repository.set('id', this.id);
        }

        repository.save();
        repository.fetch();
    }

});

var ProjectView = Backbone.View.extend({

    userModel: null,

    initialize: function(options) {
        this.userModel = options.userModel;

        this.applicationState = options.applicationState;
        this.applicationState.on('save', this.save, this);
        this.applicationState.on('change', this.render, this);

        var id = this.$('.project-id').val();

        if (id != undefined && id != '') {
            this.model = new Project({
                id: id,
                resource_uri: '/api/rest/v1/project/' + id + '/'
            });

            var graphid = this.$('.graph').attr('id');
            ActivityGraphing().drawProjectGraph(id, 100, 260, graphid, true);

        } else {
            this.model = new Project();
        }

        var that = this;
        this.$('.repository').each(function(index, elm) {
            repository = new RepositoryView({
                el: $(elm),
                applicationState: that.applicationState,
                projectModel: that.model
            });

            repository.render();
        });

        repository = new RepositoryView({
            el: this.$('.repository-sample'),
            applicationState: that.applicationState,
            projectModel: that.model
        });

        repository.render();

    },

    render: function() {
        if (this.applicationState.get('editMode')) {
            this.$(".username-warning").show();
        }else{
            this.$(".username-warning").hide();
        }
    },

    save: function() {

        this.model.set('name', this.$('.project-name').html());
        this.model.set('tag_line', this.$('.project-tagline').html());
        this.model.set('description', this.$('.project-description').html());
        this.model.set('user', this.userModel.get('resource_uri'));

        var that = this;
        this.model.save().success(function() {
            that.model.trigger('save');
        });
    }

});

var ProjectsView = Backbone.View.extend({

    applicationState: null,
    userModel: null,

    events: {
        'click .newProject': 'newProject'
    },

    initialize: function(options) {
        this.applicationState = options.applicationState;
        this.applicationState.on('change', this.render, this);

        this.userModel = options.userModel;

        $('.project-sample').hide();

        var that = this;
        $('.project').each(function(index, elm) {
            new ProjectView({
                el: $(elm),
                applicationState: that.applicationState,
                userModel: that.userModel
            }).render();
        });
    },

    render: function() {

        var count = this.$('.project').length;

        this.$('.project-count').html(count);

        if (count > 0) {
            this.$('.no-project-message').hide();
        }

        if (this.applicationState.get('editMode') == false) {
            this.$('.newProject').hide();
        } else {
            this.$('.newProject').show();
        }
    },

    newProject: function() {
        var projectDom = $('.project-sample').clone();
        projectDom.removeClass('project-sample');
        projectDom.addClass('project');
        projectDom.show();

        new ProjectView({
            el: projectDom,
            applicationState: this.applicationState,
            userModel: this.userModel
        }).render();

        $('.project-list').prepend(projectDom);

        this.render();
    }



});

var PortfolioPage = Backbone.View.extend({

    applicationState: null,

    events: {
        'click .doEdit': 'editHandler',
        'click .doSave': 'saveHandler'
    },

    initialize: function(options) {

        this.applicationState = options.applicationState;
        this.userModel = options.userModel;

        this.applicationState.on('change', this.render, this);
        this.applicationState.on('save', this.save, this);

        $('.editable').hallo({
            plugins: {
                //'halloformat': {},
                //'halloblock': {},
                //'hallolists': {},
                //'halloreundo': {},
                //'hallolink': {}
            },
            editable: false
        })

        new ProjectsView({
            el: $('.projects'),
            applicationState: this.applicationState,
            userModel: this.userModel
        }).render();

    },

    render: function() {

        var editBtn = $('.doEdit');
        var saveBtn = $('.doSave');

        if (this.applicationState.get('editMode')) {
            editBtn.hide();
            saveBtn.show();
        } else {
            editBtn.show();
            saveBtn.hide();
        }

        var that = this;
        $('.editable').each(function(index, element) {

            $(element).hallo({editable: that.applicationState.get('editMode')});
            if (that.applicationState.get('editMode')) {
                $(element).addClass('editable-enabled');
            } else {
                $(element).removeClass('editable-enabled');
            }

        });

    },

    editHandler: function() {

        this.applicationState.set('editMode', true);
        this.applicationState.change();

    },

    saveHandler: function() {

        this.applicationState.set('editMode', false);
        this.applicationState.change();

        this.applicationState.trigger('save');

    },

    save: function() {

        var profile = this.userModel.get('profile');
        profile['tag_line'] = $('.portfolio-tagline').html();
        profile['about'] = $('.portfolio-about').html();

        this.userModel.set('first_name', $('.portfolio-name').html());
        this.userModel.set('profile', profile);
        this.userModel.save();
    }

});
