
var User = Backbone.Model.extend({
    urlRoot: '/api/rest/v1/user/'
});

$(function() {

    var user = new User({id: 1});
    user.fetch();

    var editBtn = $('.doEdit');
    var saveBtn = $('.doSave');

    saveBtn.hide();

    $('.editabl').hallo({
        plugins: {
            'halloformat': {}
        },
        editable: false
    });

    function doEdit() {
        editBtn.hide();
        saveBtn.show();

        $('.editable').each(function(index, element) {

            $(element).hallo({editable: true});
            $(element).addClass('editable-enabled');
        });

    }

    function doSave() {
        editBtn.show();
        saveBtn.hide();

        $('.editable').each(function(index, element) {

            $(element).hallo({editable: false});
            $(element).removeClass('editable-enabled');
        });

        var profile = user.get('profile');
        profile['tag_line'] = $('.portfolio-tagline').html();
        profile['about'] = $('.portfolio-about').html();

        user.set('first_name', $('.portfolio-name').html());
        user.set('profile', profile);
        user.save();
    }

    $('.doEdit').bind('click', doEdit);
    $('.doSave').bind('click', doSave);

});