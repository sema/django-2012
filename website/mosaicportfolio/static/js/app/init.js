$(function() {

    var user = new User({id: 1});
    user.fetch();

    var portfolioPage = new PortfolioPage({
        el: $('body'),
        userModel: user
    });

    portfolioPage.render();

});
