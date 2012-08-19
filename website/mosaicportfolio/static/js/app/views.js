
var PortfolioPage = Backbone.View.extend({

    editMode: false,

    events: {
        'click .doEdit': 'editHandler',
        'click .doSave': 'saveHandler'
    },

    initialize: function(options) {

        this.userModel = options.userModel;

        $('.editabl').hallo({
            plugins: {
                'halloformat': {}
            },
            editable: false
        });

    },

    render: function() {

        var editBtn = $('.doEdit');
        var saveBtn = $('.doSave');

        if (this.editMode) {
            editBtn.hide();
            saveBtn.show();
        } else {
            editBtn.show();
            saveBtn.hide();
        }

        var that = this;
        $('.editable').each(function(index, element) {

            $(element).hallo({editable: that.editMode});
            if (that.editMode) {
                $(element).addClass('editable-enabled');
            } else {
                $(element).removeClass('editable-enabled');
            }

        });

    },

    editHandler: function() {

        this.editMode = true;
        this.render();

    },

    saveHandler: function() {

        this.editMode = false;

        var profile = this.userModel.get('profile');
        profile['tag_line'] = $('.portfolio-tagline').html();
        profile['about'] = $('.portfolio-about').html();

        this.userModel.set('first_name', $('.portfolio-name').html());
        this.userModel.set('profile', profile);
        this.userModel.save();

        this.render();

    }

});