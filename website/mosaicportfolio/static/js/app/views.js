
var ProjectView = Backbone.View.extend({

    initialize: function(options) {
        this.applicationState = options.applicationState;
        this.applicationState.on('save', this.save, this);

        if (this.$('.project-id').val() != '') {
            this.mode = new
        }
    },

    render: function() {

    },

    save: function() {

    }

});

var ProjectsView = Backbone.View.extend({

    applicationState: null,

    events: {
        'click .newProject': 'newProject'
    },

    initialize: function(options) {
        this.applicationState = options.applicationState;

        this.applicationState.on('change', this.render, this);

        $('.project-sample').hide();
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
            applicationState: this.applicationState
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
                'halloformat': {}
            },
            editable: false
        });

        new ProjectsView({
            el: $('.projects'),
            applicationState: this.applicationState
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