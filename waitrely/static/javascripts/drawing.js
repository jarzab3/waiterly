function drawing(x1, y1, x2, y2, state) {
    var can = document.getElementById('canvas');

    // can.innerHTML="";
        // document.body.innerHTML = '';


    var w = window.innerWidth;
    var h = window.innerHeight;

    x1 = (w / 12) * x1;
    y1 = (h / 17) * y1;

    x2 = (w / 12) * x2;
    y2 = (h / 17) * y2;


    // x1 = Math.floor((Math.random() * w) + 0);
    // y1 = Math.floor((Math.random() * h) + 0);
    //
    // x2 = Math.floor((Math.random() * w) + 0);
    // y2 = Math.floor((Math.random() * h) + 0);


    console.log("New", x1, y1, x2, y2);

    can.height = h;
    can.width = w;



    var ctx = can.getContext('2d');

    // ctx.clearRect(0,0,can.width,can.height);

    tw = 200;
    th = 100;

    function draw() {
        ctx.beginPath();
        ctx.strokeStyle = "#000000";
        ctx.setLineDash([1, 15]);
        ctx.moveTo(x1, y1);
        ctx.lineTo(w / 2, h / 2);
        ctx.stroke();

        ctx.beginPath();
        ctx.strokeStyle = "#000000";
        ctx.setLineDash([1, 15]);
        ctx.moveTo(x2, y2);
        ctx.lineTo(w / 2, h / 2);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(x1, y1, 20, 0, 2 * Math.PI);
        ctx.fillStyle = '#8fd369';
        ctx.fill();
        ctx.fillStyle = '#310b0b';
        ctx.fillText("W2", x1, y1 - 20);
        ctx.font = "12px Verdana";


        ctx.beginPath();
        ctx.arc(x2, y2, 20, 0, 2 * Math.PI);
        ctx.fillStyle = '#51416E';
        // "rgba(181,186,208,1)";
        ctx.fill();
        ctx.fillStyle = '#310b0b';
        ctx.fillText("W1", x2, y2 - 20);
        ctx.font = "12px Verdana";


        ctx.fillStyle = 'rgba(124,89,52,0.6)';
        ctx.fillRect(w / 2 - tw / 2, h / 2 - th / 2, tw, th);

        ctx.beginPath();
        ctx.arc(w / 2 - tw / 4, h / 2, 12, 0, 2 * Math.PI);
        if (state == 'full') {
            ctx.fillStyle = 'rgba(110,251,7,1)';
        } else {
            ctx.fillStyle = 'rgba(244,49,31,1)';
        }
        ctx.fill();
        // x += 2;
        // ctx.fillStyle = "rgba(0,0,0,0)";
        // ctx.fillRect(0, 0, can.width, can.height);
        // requestAnimationFrame(draw);
    }
    //
    requestAnimationFrame(draw);

}



function callAPI() {


    $.getJSON($SCRIPT_ROOT + '/_apiQuery', {
        apiQ0: "request"

    }, function (data) {

        var w1 = data["waiter1"];
        var w2 = data["waiter2"];

        var w1x = w1.x;
        var w1y = w1.y;

        var w2x = w2.x;
        var w2y = w2.y;

        // console.log(w1x);
        // console.log(w1y);
        drawing(w1x, w1y, w2x, w2y, 'empty');


        setTimeout(function () {
            callAPI()
        }, 1000);


        return false;

    });

}

$(document).ready(function () {
    callAPI();
});