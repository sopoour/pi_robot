function makeHttpObject() {
    try {return new XMLHttpRequest();}
    catch (error) {}
    try {return new ActiveXObject("Msxml2.XMLHTTP");}
    catch (error) {}
    try {return new ActiveXObject("Microsoft.XMLHTTP");}
    catch (error) {}
    throw new Error("Could not create HTTP request object.");
}
var request = makeHttpObject();
var getSensors = makeHttpObject();
var doubleClickTimer = 300;
var linkCheckTimer = 5000;
var heartbeatTimer = 1000;
var newSpeedL = 0;
var newSpeedR = 0;
var actSpeedL = 0;
var actSpeedR = 0;
var newSpeed = 0;
var doubleClick = false;
var showHUD = true;
var video = false;
var framerate = 0;
var link = true;
var videoimg = '<img src="/video_feed.mjpg" alt="Connecting to Live Video">'
var frameimg = '<img id="sframe" src="/single_frame.jpg" alt="Connecting to Live Video">'
var framesrc = '/single_frame.jpg'
var inactive = "0px";
var active = "10px solid black";
var clickTimer = setTimeout(reset_doubleclick, doubleClickTimer);
var linkCheck = setTimeout(linkLost, linkCheckTimer);
setInterval(heartbeat, heartbeatTimer);
getSensors.onreadystatechange = updateHUD;
setTimeout(checkVideo, 500);
function linkLost() {
	var status = 'Status<br>Link: DOWN!';
	var sensors = 'Sensors<br>No Data!';
	document.getElementById("status").innerHTML = status;
    	document.getElementById("sensors").innerHTML = sensors;
    	document.getElementById("video").innerHTML = '&nbsp';
    	link = false;
}
function checkVideo() {
	if (video) {
		if (framerate > 0) {
			document.getElementById("video").innerHTML = frameimg;
			setInterval(reloadFrame, framerate);
		} else {
			document.getElementById("video").innerHTML = videoimg;
		}
	}
}
function reloadFrame() {
	document.getElementById("sframe").src = framesrc + '?' + new Date().getTime();
}
function heartbeat() {
    var heartbeat_url = "/heartbeat";
    getSensors.open("GET", heartbeat_url, true);
    getSensors.send(null);
}
function updateHUD(e) {
	var status;
	var sensors;
	if (getSensors.readyState == 4 && getSensors.status == 200) {
        var response = JSON.parse(getSensors.responseText);
        video = response.v;
        framerate = response.f;
        status = "STS-PiLot Status<br>Link: online<br>Videolink: ";
	if (framerate > 0) {
		status += (Math.ceil(1000 / framerate) + " FPS");
	} else {
        	status += video;
	}
        status += "<br>Motor L: ";
        status += response.l;
        status += "<br>Motor R: ";
        status += response.r;
        sensors = "Sensors<br>Digital 1: ";
        sensors += response.i1;
        sensors += "<br>Digital 2: ";
        sensors += response.i2;
        sensors += "<br>Digital 3: ";
        sensors += response.i3;
        sensors += "<br>Digital 4: ";
        sensors += response.i4;
        sensors += "<br>Analog 1: ";
        sensors += response.a1;
        sensors += "<br>Analog 2: ";
        sensors += response.a2;
        sensors += "<br>Analog 3: ";
        sensors += response.a3;
        sensors += "<br>Analog 4: ";
        sensors += response.a4;
        document.getElementById("status").innerHTML = status;
        document.getElementById("sensors").innerHTML = sensors;
        button_status('blue', response.b);
        button_status('yellow', response.y);
        button_status('red', response.c);
        button_status('green', response.g);
        clearTimeout(linkCheck);
		linkCheck = setTimeout(linkLost, linkCheckTimer);
		if (!link) {
			location.reload();
		}
		link = true;
	}
}
function toggle_hud() {
	button_status('hud', showHUD);
	showHUD = !showHUD;
	if (showHUD) {
		document.getElementById("overlay").style.display = 'block';
	} else {
		document.getElementById("overlay").style.display = 'none';
	}
}
function button_status(button, status) {
	if (status) {
		document.getElementById(button).style.opacity = '0.5';
	} else {
		document.getElementById(button).style.opacity = '1';
	}
}
function reset_doubleclick() {
    doubleClick = false;
}
function set_doubleclick() {
    clearTimeout(clickTimer);
    clickTimer = setTimeout(reset_doubleclick, doubleClickTimer);
    doubleClick = true;
}

//speed(30) = slow, speed(60) = medium, speed(100) = fast
function speed(value){
    newSpeed = value;
    set_doubleclick();
    if (value == 30){
        document.getElementById('slow').style.opacity = '0.5';
        document.getElementById('medium').style.opacity = '1';
        document.getElementById('fast').style.opacity = '1';
    }
    else if (value == 60){
        document.getElementById('medium').style.opacity = '0.5';
        document.getElementById('slow').style.opacity = '1';
        document.getElementById('fast').style.opacity = '1';
    }
    else if (value == 100){
        document.getElementById('fast').style.opacity = '0.5';
        document.getElementById('medium').style.opacity = '1';
        document.getElementById('slow').style.opacity = '1';
    }
    else {
        document.getElementById('slow').style.opacity = '1';
        document.getElementById('medium').style.opacity = '1';
        document.getElementById('fast').style.opacity = '1';
    }
}

//left(newSpeed)
function left(speed) {
    newSpeedL = 10;
    //only if the right motor speed is higher than the left one we set it to the speed
    if (speed > newSpeedL) {
        newSpeedR = speed;
        set_doubleclick();
        set_motor();
        document.getElementById('left').style.opacity = '0.5';
        document.getElementById('right').style.opacity = '1';
        document.getElementById('forward').style.opacity = '1';
        document.getElementById('backward').style.opacity = '1';
        document.getElementById('stop').style.opacity = '1';
    }
    else {
        //increase the right motor by the amount of left motor so that it def turns left
        newSpeedR += newSpeedL;
        set_doubleclick();
        set_motor();
    }  
}

//right(newSpeed)
function right(speed) {
    newSpeedR = 10;
    if (speed > newSpeedR) {
        newSpeedL = speed;
        set_doubleclick();
        set_motor();
        document.getElementById('right').style.opacity = '0.5';
        document.getElementById('left').style.opacity = '1';
        document.getElementById('forward').style.opacity = '1';
        document.getElementById('backward').style.opacity = '1';
        document.getElementById('stop').style.opacity = '1';
    }
    else {
        newSpeedL += newSpeedR;
        set_doubleclick();
        set_motor();
    }  
}

//forward(newSpeed)
function forward(speed) {
    newSpeedL = speed;
    newSpeedR = speed;
    set_doubleclick();
    set_motor();
    document.getElementById('forward').style.opacity = '0.5';
    document.getElementById('right').style.opacity = '1';
    document.getElementById('left').style.opacity = '1';
    document.getElementById('backward').style.opacity = '1';
    document.getElementById('stop').style.opacity = '1';
}

//backward(newSpeed)
function backward(speed) {
    newSpeedL = -speed;
    newSpeedR = -speed;
    set_doubleclick();
    set_motor();
    document.getElementById('backward').style.opacity = '0.5';
    document.getElementById('right').style.opacity = '1';
    document.getElementById('forward').style.opacity = '1';
    document.getElementById('left').style.opacity = '1';
    document.getElementById('stop').style.opacity = '1';
}

function brake() {
    newSpeedR = 0;
    newSpeedL = 0;
    set_motor();
    document.getElementById('stop').style.opacity = '0.5';
    document.getElementById('right').style.opacity = '1';
    document.getElementById('left').style.opacity = '1';
    document.getElementById('forward').style.opacity = '1';
    document.getElementById('backward').style.opacity = '1';
}

function set_motor() {
    var motor_url = "/motor?l=" + newSpeedL.toString() + '&r=' + newSpeedR.toString();
    request.open("GET", motor_url, true);
    request.send(null);
    //var oldId = "l" + actSpeedL.toString();
    //var newId = "l" + newSpeedL.toString();
    //document.getElementById(oldId).style.outline = inactive;
    //document.getElementById(newId).style.outline = active;
    //oldId = "r" + actSpeedR.toString();
    //newId = "r" + newSpeedR.toString();
    //document.getElementById(oldId).style.outline = inactive;
    //document.getElementById(newId).style.outline = active;
    actSpeedL = newSpeedL;
    actSpeedR = newSpeedR;
}
function touchpad(pad) {
    var touchpad_url = "/touchpad?pad=" + pad.toString();
    request.open("GET", touchpad_url, true);
    request.send(null);
}

heartbeat();




