var init = true;
var MAX_RETRIES = 3;
var retries = MAX_RETRIES;
var g = false;
var time_range = false;
var soundLevelData = [];

var layout = {
    drawPoints: true,
    showRoller: true,
    animatedZooms: true,
    title: "Galileo Sensor Chart",
    labels: ['Time', 'Sound Level (1 - 1024)'],
    interactionModel: interactionModel
}

var compare = function (filter) {
    return function (a,b) { //closure
        var a = a[filter],
            b = b[filter];

        if (a < b) {
            return -1;
        }else if (a > b) {
            return 1;
        } else {
            return 0;
        }
    };
};

function initialiseGraph() {
    g = new Dygraph(document.getElementById("soundgraph"), soundLevelData, layout);
}

function updateGraph() {
    g.updateOptions({'file': soundLevelData});
}

function send() {
    setTimeout(function() {
        var output = {
            "init": init,
            "time": init ? 0 : g.xAxisRange()[1]
        };
        
        if(!init && g.xAxisRange()[0] < g.xAxisExtremes()[0]) {
            output.startTime = parseInt(g.xAxisRange()[0]/1000);
            output.endTime = parseInt(g.xAxisExtremes()[0]/1000);
            console.log("loading earlier data");
        } else if(!init && g.xAxisRange()[1] > g.xAxisExtremes()[1]) {
            output.startTime = parseInt(g.xAxisExtremes()[1]/1000)
            output.endTime = parseInt(g.xAxisRange()[1]/1000);
            console.log("loading later data");
        }
        
        if(isConnected(ws)) {
            retries = MAX_RETRIES;
            ws.send(JSON.stringify(output));
        } else if(retries-- > 0) {
            ws = connect();
        } else {
            alert("Unable to connect to server after " + MAX_RETRIES + " retries");
            clearInterval(c);
        }
    }, 1000);
}

function isConnected(ws) {
    return ws.readyState === 1;
}

function connect() {
    var socket = new WebSocket("ws://" + document.location.host + "/websocket");
    socket.onmessage = receive;
    return socket;
}

function disconnect() {
    ws.onclose = function () {}; // disable onclose handler first
    ws.close();
}

function parseRow(ele) {
    return [new Date(parseInt(ele[0])*1000), parseInt(ele[1])];
}

function receive(msg) {
    var data = JSON.parse(msg.data);
    var rows = data;
    console.log(rows.length);
    if(rows.length) {
        soundLevelData = soundLevelData.concat(rows.map(parseRow)).sort(function(a, b) {
            return a[0] - b[0];
        }).filter(function(ele, pos, arr) { return arr.indexOf(ele) == pos; });
        if(init) {
            initialiseGraph();
            init = false;
        } else updateGraph();
    }
    
    send();
}

function set_footer_position() {
    // https://stackoverflow.com/questions/23095645/forcing-footer-to-bottom-of-page-if-document-height-is-smaller-than-window-heig
    if ($(document.body).height() < $(window).height()) {
        $('footer').attr('style', 'position: fixed!important; bottom: 0; left: 0; right: 0;');
    } else {
        $('footer').attr('style', 'position: static');
    }
}

window.addEventListener('resize', function() {
    set_footer_position();
});

window.addEventListener("load", function() {
    if ("WebSocket" in window) {
        ws = connect();
    };
    
    set_footer_position();
    
    send();

    window.onbeforeunload = disconnect;
});
