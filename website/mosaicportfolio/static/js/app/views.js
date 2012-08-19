
var ProjectView = Backbone.View.extend({

    userModel: null,

    initialize: function(options) {
        this.userModel = options.userModel;

        this.applicationState = options.applicationState;
        this.applicationState.on('save', this.save, this);

        var id = this.$('.project-id').val();

        if (id != undefined && id != '') {
            this.model = new Project({
                id: id,
                resource_uri: '/api/rest/v1/project/' + id + '/'
            });
        } else {
            this.model = new Project();
        }
        ActivityGraphing().drawUserGraph(this.userModel.get('id'), 400, 800, "usergraph");
    },

    render: function() {

    },

    save: function() {

        this.model.set('name', this.$('.project-name').html());
        this.model.set('tag_line', this.$('.project-tagline').html());
        this.model.set('description', this.$('.project-description').html());
        this.model.set('user', this.userModel.get('resource_uri'));
        this.model.save();
        this.model.fetch();
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
                'halloformat': {},
                'halloblock': {},
                'hallolists': {},
                'halloreundo': {},
                'hallolink': {}
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
console.log($('.portfolio-name').html());
        this.userModel.set('first_name', $('.portfolio-name').html());
        this.userModel.set('profile', profile);
        this.userModel.save();
    }

});
