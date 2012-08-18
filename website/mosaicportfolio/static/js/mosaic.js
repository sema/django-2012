
$(function() {

    $('body').midgardCreate({
        url: function() {
            return 'javascript:false;';
        },
        toolbar: 'full'
    });

    $('.create-toolbar-left').html($('.create-ui-toolbar-dynamictoolarea'));
    $('.create-toolbar-right').html($('.create-ui-toolbar-statustoolarea'));

    $('.create-ui-btn').each(function(index, elm) {
        $(elm).addClass('btn btn-primary');
    });

    // Fake Backbone.sync since there is no server to communicate with
    Backbone.sync = function(method, model, options) {
        if (console && console.log) {
            console.log('Model contents', model.toJSONLD());
        }
        options.success(model);
    };
});