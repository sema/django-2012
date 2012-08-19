// Load the Visualization API
google.load('visualization', '1.0', {'packages':['corechart']});

$(
    /**
     * Simple Google Charts wrapper for drawing activity graphs. Will make callbacks to server for data. 
     * 
     * Requires "https://www.google.com/jsapi"
     * 
     * Template modified from Google charts Column Chart example.
     */
    function(){

        function drawVisualization(arrays, title, target_id, width, height, vTitle, hTitle) {
            // Create and populate the data table.
            var data = 
                google.visualization.arrayToDataTable(
                    arrays
                );

            // Create and draw the visualization.
            new google.visualization.ColumnChart(document.getElementById(target_id)).
                draw(data,
                     {title: title,
                      width:width, height:height,
                      isStacked: true,
                      vAxis: {title: vTitle},
                      hAxis: {title: hTitle}}
                    );
        }
        function drawUserGraph(){
            function draw(model, response){
                data = { title: model.get('title'), width: 600, height:400, vTitle: model.get("vTitle"), hTitle: model.get("hTitle"),
                         table: model.get('table')               
                       };
                drawVisualization(data.table, data.title, 'usergraph', data.width, data.height, data.vTitle, data.hTitle);
            };
            new UserGraph({id: getUser()}).
                fetch({success: draw, error: draw});
        }

        function getUser(){
            return 1;
        }

        // Set a callback to run when the Google Visualization API is loaded.
        google.setOnLoadCallback(drawUserGraph);
    }
);
