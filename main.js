const COLOR_BG = "black";
const COLOR_CUBE = "yellow";
const SPEED_X = 0.05;
const SPEED_Y = 0.15;
const SPEED_Z = 0.1;
const POINT3D = function(x,y,z){
    this.x = x;
    this.y = y;
    this.z = z;
}

var canvas = document.createElement("canvas");
document.body.appendChild(canvas);
var ctx = canvas.getContext("2d");

var k = 0

var h = document.documentElement.clientHeight;
var w = document.documentElement.clientWidth;
canvas.height = h;
canvas.width = w;

ctx.fillstyle = COLOR_BG;
ctx.strokeStyle = COLOR_CUBE;
ctx.lineWidth = w/500;
ctx.lineCap = "round";
let n;
let m;

function canvasLoop(e) {
    var movementX = e.movementX ||
        e.mozMovementX          ||
        e.webkitMovementX       ||
        0;
  
    var movementY = e.movementY ||
        e.mozMovementY      ||
        e.webkitMovementY   ||
        0;
  
    x += movementX;
    y += movementY;
  
    var animation = requestAnimationFrame(canvasLoop);
  
    tracker.innerHTML = "X position: " + x + ', Y position: ' + y;
  }

function lockChangeAlert() {
    if(document.pointerLockElement === canvas) {
      console.log('The pointer lock status is now locked');
      document.addEventListener("mousemove", canvasLoop, false);
    } else {
      console.log('The pointer lock status is now unlocked');  
      document.removeEventListener("mousemove", canvasLoop, false);
    }
  }
  

canvas.onclick = function() {
    canvas.requestPointerLock();
  }
  document.addEventListener('pointerlockchange', lockChangeAlert, false);

var cx = 0 + w/40;
var cy = 0 + h/20;
var cz = 0;
var size = h/20;
var vertices = [
    new POINT3D(cx - size, cy - size, cz - size),
    new POINT3D(cx + size, cy - size, cz - size),
    new POINT3D(cx + size, cy + size, cz - size),
    new POINT3D(cx - size, cy + size, cz - size),
    new POINT3D(cx - size, cy - size, cz + size),
    new POINT3D(cx + size, cy - size, cz + size),
    new POINT3D(cx + size, cy + size, cz + size),
    new POINT3D(cx - size, cy + size, cz + size)
];

var edges = [
    [0,1], [1,2], [2,3], [3,0],
    [4,5], [5,6], [6,7], [7,4],
    [0,4], [1,5], [2,6], [3,7]
];

var q = 0

var timeDelta, timeLast = 0;

requestAnimationFrame(loop);

function loop(timeNow) {

    timeDelta = timeNow - timeLast;
    timeLast = timeNow;

    ctx.fillRect(0,0,w,h);

    let angle = timeDelta * 0.001 * SPEED_Z * Math.PI * 2;
    for (let v of vertices) {
        let dx = v.x - cx;
        let dy = v.y - cy;
        let x = dx * Math.cos(angle) - dy * Math.sin(angle);
        let y = dx * Math.sin(angle) + dy * Math.cos(angle);
        v.x = x + cx;
        v.y = y + cy;
    }

    angle = timeDelta * 0.001 * SPEED_X * Math.PI * 2;
    for (let v of vertices) {
        let dy = v.y - cy;
        let dz = v.z - cz;
        let y = dy * Math.cos(angle) - dz * Math.sin(angle);
        let z = dy * Math.sin(angle) + dz * Math.cos(angle);
        v.y = y + cy;
        v.z = z + cz;
    }
    

    
    angle = timeDelta * 0.001 * SPEED_Y * Math.PI * 2;
    for (let v of vertices) {
        let dx = v.x - cx;
        let dz = v.z - cz;
        let x = dz * Math.sin(angle) + dx * Math.cos(angle);
        let z = dz * Math.cos(angle) - dx * Math.sin(angle);
        v.x = x + cx;
        v.z = z + cz;
    }

    while(q<10){
        while(k<20){
            for (let edge of edges) {
                ctx.beginPath();
                ctx.moveTo(vertices[edge[0]].x + k*(h/10), vertices[edge[0]].y + q*(h/10));
                ctx.lineTo(vertices[edge[1]].x + k*(h/10), vertices[edge[1]].y + q*(h/10));
                ctx.stroke();
            }
            k += 1

        }
        if(k=20) k=0;
        q += 1
    }

    if(q=10) q=0;

    requestAnimationFrame(loop);
}