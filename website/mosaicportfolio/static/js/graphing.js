// Load the Visualization API
google.load('visualization', '1.0', {'packages':['corechart']});
/**
 * Simple Google Charts wrapper for drawing activity graphs. Will make callbacks to server for data. 
 * 
 * Requires "https://www.google.com/jsapi"
 * 
 * Template modified from Google charts Column Chart example.
 */
ActivityGraphing = function(){
    function drawVisualization(arrays, title, target, width, height, vTitle, hTitle) {
        google.setOnLoadCallback(function(){
                                     // Create and populate the data table.
                                     var data = 
                                         google.visualization.arrayToDataTable(
                                             arrays
                                         );

                                     // Create and draw the visualization.
                                     new google.visualization.ColumnChart(document.getElementById(target)).
                                         draw(data,
                                              {title: title,
                                               width:width, height:height,
                                               isStacked: true,
                                               vAxis: {title: vTitle},
                                               hAxis: {title: hTitle}}
                                             );
                                 }
                                );
    }
    function delayedDraw(height, width, target){
        function draw(model, response){
            var data = { title: model.get('title'), width: width, height:height, vTitle: model.get("vTitle"), hTitle: model.get("hTitle"),
                         table: model.get('table')               
                       };
            drawVisualization(data.table, data.title, target, data.width, data.height, data.vTitle, data.hTitle);
        };
        return draw;
    }

    function drawUserGraph(user, height, width, target){
        var draw = delayedDraw(height, width, target);
        new UserGraph({id:user}).
            fetch({success: draw});
    }
    function drawProjectGraph(project, height, width, target){
        var draw = delayedDraw(height, width, target);
        new ProjectGraph({id:project}).fetch({success: draw});
    }

    return {
        drawUserGraph: drawUserGraph,
        drawProjectGraph: drawProjectGraph
    };
};
