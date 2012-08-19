
$(function() {

    $('body').midgardCreate({
        url: function() {
            return 'javascript:false;';
        },
        toolbar: 'full'
    });

    $('.create-toolbar-floating').html($('.create-ui-toolbar-dynamictoolarea'));
    $('.create-toolbar-right').html($('.create-ui-toolbar-statustoolarea'));

    // Fake Backbone.sync since there is no server to communicate with
    Backbone.sync = function(method, model, options) {
        if (console && console.log) {
            console.log('Model contents', model.toJSONLD());
        }
        options.success(model);
    };
});