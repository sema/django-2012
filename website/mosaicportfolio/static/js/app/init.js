$(function() {

      var user_pk = $('#user_pk').val();

      var user = new User({id: user_pk});
      user.fetch();

      var applicationState = new ApplicationState();
      applicationState.set('editMode', false);
      applicationState.change();

      var portfolioPage = new PortfolioPage({
                                                el: $('body'),
                                                userModel: user,
                                                applicationState: applicationState
                                            });

      portfolioPage.render();

      ActivityGraphing().drawUserGraph(user.get('id'), 400, 800, "usergraph");


  });
