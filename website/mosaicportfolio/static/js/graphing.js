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
    function drawVisualization(arrays, title, height, width, target, compact, vTitle, hTitle) {
        //        google.setOnLoadCallback(function(){
        // Create and populate the data table.
        var data = 
            google.visualization.arrayToDataTable(
                arrays
            );

        // Create and draw the visualization.
        new google.visualization.ColumnChart(document.getElementById(target)).
            draw(data,
                 {  title: compact? null: title,
                    width:width, height:height,
                    isStacked: true,
                    legend: {position: compact ? 'none': 'top' },
                    vAxis: {title: compact? null: vTitle, textColor: compact? '#ffffff': '#000000', gridlines: {count: compact? 0: 5}},
                    hAxis: {title: compact? null: hTitle, textColor: compact? '#ffffff': '#000000', gridlines: 3},
                    axisFontSize : compact? 0 : 'auto'
                 }
                );
        //                                 }
        //                                );
    }
    function delayedDraw(height, width, target, compact){
        function draw(model, response){
            var data = { title: model.get('title'), width: width, height:height, vTitle: model.get("vTitle"), hTitle: model.get("hTitle"),
                         table: model.get('table')               
                       };
            drawVisualization(data.table, data.title, data.height, data.width, target, compact, data.vTitle, data.hTitle);
        };
        return draw;
    }

    function drawUserGraph(user, height, width, target, compact){
        var draw = delayedDraw(height, width, target, compact);
        new UserGraph({id:user}).
            fetch({success: draw});
    }
    function drawProjectGraph(project, height, width, target, compact){
        var draw = delayedDraw(height, width, target, compact);
        new ProjectGraph({id:project}).fetch({success: draw});
    }

    return {
        drawUserGraph: drawUserGraph,
        drawProjectGraph: drawProjectGraph
    };
};
