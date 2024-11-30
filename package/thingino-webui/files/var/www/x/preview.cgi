#!/bin/haserl
<%in _common.cgi %>
<%
page_title="Camera preview"
icon_gear="<img src=\"/a/gear.svg\" alt=\"Image: Settings\">"
which motors > /dev/null && has_motors="true"
%>
<%in _header.cgi %>

<div class="row preview">
<div class="col-lg-1">

<div class="d-flex flex-nowrap flex-lg-wrap align-content-around gap-1" aria-label="controls">
<input type="checkbox" class="btn-check" name="motionguard" id="motionguard" value="1">
<label class="btn btn-dark border mb-2" for="motionguard" title="Motion Guard"><img src="/a/motion.svg" alt="Motion Guard" class="img-fluid"></label>

<input type="checkbox" class="btn-check" name="r180" id="r180" value="1">
<label class="btn btn-dark border mb-2" for="r180" title="Rotate 180°"><img src="/a/rotate.svg" alt="Rotate 180°" class="img-fluid"></label>

<input type="checkbox" class="btn-check" name="daynight" id="daynight" value="1">
<label class="btn btn-dark border mb-2" for="daynight" title="Night mode"><img src="/a/night.svg" alt="Day/Night Mode" class="img-fluid"></label>

<input type="checkbox" class="btn-check" name="color" id="color" value="1">
<label class="btn btn-dark border mb-2" for="color" title="Color mode"><img src="/a/color.svg" alt="Color mode" class="img-fluid"></label>

<% if get gpio_ircut >/dev/null; then %>
<input type="checkbox" class="btn-check" name="ircut" id="ircut" value="1">
<label class="btn btn-dark border mb-2" for="ircut" title="IR filter"><img src="/a/ircut_filter.svg" alt="IR filter" class="img-fluid"></label>
<% fi %>

<% if get gpio_ir850 >/dev/null; then %>
<input type="checkbox" class="btn-check" name="ir850" id="ir850" value="1">
<label class="btn btn-dark border mb-2" for="ir850" title="IR LED 850 nm"><img src="/a/light_850nm.svg" alt="850nm LED" class="img-fluid"></label>
<% fi %>

<% if get gpio_ir940 >/dev/null; then %>
<input type="checkbox" class="btn-check" name="ir940" id="ir940" value="1">
<label class="btn btn-dark border mb-2" for="ir940" title="IR LED 940 nm"><img src="/a/light_940nm.svg" alt="940nm LED" class="img-fluid"></label>
<% fi %>

<% if get gpio_white >/dev/null; then %>
<input type="checkbox" class="btn-check" name="white" id="white" value="1">
<label class="btn btn-dark border mb-2" for="white" title="White LED"><img src="/a/light_white.svg" alt="White light" class="img-fluid"></label>
<% fi %>

<button type="button" class="btn btn-dark border mb-2" title="Zoom" data-bs-toggle="modal" data-bs-target="#mdPreview">
<img src="/a/zoom.svg" alt="Zoom" class="img-fluid"></button>
</div>

</div>
<div class="col-lg-10">
<div id="frame" class="position-relative mb-2">
<img id="preview" src="/a/nostream.webp" class="img-fluid" alt="Image: Preview">
<% if [ "true" = "$has_motors" ]; then %><%in _motors.cgi %><% fi %>
</div>

<% if [ "true" = "$has_motors" ]; then %>
<p class="small">Move mouse cursor over the center of the preview image to reveal the motor controls.
Use a single click for precise positioning, double click for coarse, larger distance movement.</p>
<% fi %>

<div class="alert alert-secondary">
<p class="mb-0"><img src="/a/mute.svg" alt="Icon: No Audio" class="float-start me-2" style="height:1.75rem" title="No Audio">
Please note, there is no audio on this page. Open the RTSP stream in a player to hear audio.</p>
<b id="playrtsp" class="cb"></b>
</div>
</div>

<div class="col-lg-1">
<div class="d-flex flex-nowrap flex-lg-wrap align-content-around gap-1" aria-label="controls">

<a href="image.cgi" target="_blank" class="btn btn-dark border mb-2" title="Save image"><img
 src="/a/download.svg" alt="Save image" class="img-fluid"></a>

<button type="button" class="btn btn-dark border mb-2" title="Send to email" data-sendto="email"><img
 src="/a/email.svg" alt="Email" class="img-fluid"></button>

<button type="button" class="btn btn-dark border mb-2" title="Send to email" data-sendto="telegram"><img
 src="/a/telegram.svg" alt="Telegram" class="img-fluid"></button>

<button type="button" class="btn btn-dark border mb-2" title="Send to FTP" data-sendto="ftp"><img
 src="/a/ftp.svg" alt="FTP" class="img-fluid"></button>

<button type="button" class="btn btn-dark border mb-2" title="Send to MQTT" data-sendto="mqtt"><img
 src="/a/mqtt.svg" alt="MQTT" class="img-fluid"></button>

<button type="button" class="btn btn-dark border mb-2" title="Send to Webhook" data-sendto="webhook"><img
 src="/a/webhook.svg" alt="Webhook" class="img-fluid"></button>

<button type="button" class="btn btn-bark border mb-2" title="Yandex Disk" data-sendto="yadisk"><img
 src="/a/yadisk.svg" alt="Yandex Disk" class="img-fluid"></button>

</div>
</div>

</div>

<%in _preview.cgi %>

<script>
<%
for i in email ftp mqtt telegram webhook yadisk; do
	[ "true" = $(eval echo \$${i}_enabled) ] && continue
%>
{
	let a = document.createElement('a')
	a.href = 'plugin-send2<%= $i %>.cgi'
	a.classList.add('btn','btn-outline-danger','mb-2')
	a.title = 'Configure sent2<%= $i%> plugin'
	a.append($('button[data-sendto=<%= $i %>] img'))
	$('button[data-sendto=<%= $i %>]').replaceWith(a);
}
<% done %>

$$("button[data-sendto]").forEach(el => {
	el.onclick = (ev) => {
		ev.preventDefault();
		if (!confirm("Are you sure?")) return false;
		fetch("/x/send.cgi?" + new URLSearchParams({'to': el.dataset.sendto}).toString())
		.then(res => res.json())
		.then(data => console.log(data))
	}
});

const preview = $("#preview");
preview.onload = function() { URL.revokeObjectURL(this.src) }

function updatePreview(data) {
	const blob = new Blob([data], {type: 'image/jpeg'});
	const url = URL.createObjectURL(blob);
	preview.src = url;
	$("#preview_fullsize").src = url;
	ws.send('{"action":{"capture":null}}');
}

const ImageBlackMode = 1
const ImageColorMode = 0

let ws = new WebSocket(`//${document.location.hostname}:8089?token=<%= $ws_token %>`);
ws.onopen = () => {
	console.log('WebSocket connection opened');
	ws.binaryType = 'arraybuffer';
	const payload = '{'+
		'"image":{"hflip":null,"vflip":null,"running_mode":null},'+
		'"motion":{"enabled":null},'+
		'"rtsp":{"username":null,"password":null,"port":null},'+
		'"stream0":{"rtsp_endpoint":null},'+
		'"action":{"capture":null}'+
		'}'
	console.log(ts(), '===>', payload);
	ws.send(payload);
}
ws.onclose = () => { console.log('WebSocket connection closed'); }
ws.onerror = (err) => { console.error('WebSocket error', err); }
ws.onmessage = (ev) => {
	if (typeof ev.data == 'string') {
		if (ev.data == '') {
			console.log('Empty response')
			return
		}
		if (ev.data == '{"action":{"capture":"initiated"}}') {
			return;
		}
		console.log(ts(), '<===', ev.data);
		const msg = JSON.parse(ev.data);

		if (msg.image) {
			if (msg.image.running_mode) {
				$("#color").checked = msg.image.running_mode;
			}
			if (msg.image.hflip) {
				$('#r180').checked = msg.image.hflip;
			}
			if (msg.image.vflip) {
				$('#r180').checked = msg.image.vflip;
			}
		}
		if (msg.motion) {
			if (msg.motion.enabled) $('#motionguard').checked = msg.motion.enabled;
		}
		if (msg.rtsp) {
			const r = msg.rtsp;
			if (r.username && r.password && r.port)
				$('#playrtsp').innerHTML = 'mpv --profile=fast ' +
					`rtsp://${r.username}:${r.password}@${document.location.hostname}:${r.port}/${msg.stream0.rtsp_endpoint}`;
		}
	} else if (ev.data instanceof ArrayBuffer) {
		updatePreview(ev.data);
	}
}

function sendToWs(payload) {
	payload = payload.replace(/}$/, ',"action":{"save_config":null}}')
	console.log(ts(), '===>', payload);
	ws.send(payload);
}

function toggleColor() {
	const mode = $("#color").checked ? ImageBlackMode : ImageColorMode
	const payload = '{"image":{"running_mode":' + mode + '}}'
	sendToWs(payload)
}

async function toggleIRcut() {
	const el = $('#ircut')
	const url = '/x/json-imp.cgi?' + new URLSearchParams({'cmd': 'ircut', 'val': (el.checked ? 0 : 1)}).toString()
	console.log(url)
	await fetch(url)
		.then(res => res.json())
		.then(data => el.checked = data.message.ircut == 1)
}

async function toggleLED(el) {
	if (!el) return;
	const url = '/x/json-gpio.cgi?' + new URLSearchParams({'n': 'gpio_' + el.id, "s": (el.checked ? 0 : 1)}).toString();
	console.log(url)
	await fetch(url)
		.then(res => res.json())
		.then(data => el.checked = data.message.status == 1)
}

async function toggleDayNight(mode) {
	url = '/x/json-imp.cgi?' + new URLSearchParams({'cmd': 'daynight', 'val': mode}).toString()
	console.log(url)
	await fetch(url)
		.then(res => res.json())
		.then(data => {
			 console.log(data.message)
			 $('#daynight').checked = (data.message.daynight == 'day')
			 if ($('#ir850')) $('#ir850').checked = (data.message.ir850 == 1)
			 if ($('#ir940')) $('#ir940').checked = (data.message.ir940 == 1)
			 if ($('#ircut')) $('#ircut').checked = (data.message.ircut == 1)
			 if ($('#color')) $('#color').checked = (data.message.color == 1)
		})
}

$("#ircut")?.addEventListener('change', ev => {
	toggleIRcut()
}, true);

$("#ir850")?.addEventListener('change', ev => {
	toggleLED(ev.target)
}, true);

$("#ir940")?.addEventListener('change', ev => {
	toggleLED(ev.target)
}, true);

$("#white")?.addEventListener('change', ev => {
	toggleLED(ev.target)
}, true);

$("#color").addEventListener('change', ev => {
	toggleColor()
});

$("#motionguard").addEventListener('change', ev => {
	sendToWs('{"motion":{"enabled":' + ev.target.checked + '}}');
});

$('#r180').addEventListener('change', ev => {
	sendToWs('{"image":{"hflip":' + ev.target.checked + ',"vflip":' + ev.target.checked + '}}')
});

$("#daynight").addEventListener('change', ev => {
	ev.target.checked ? toggleDayNight('day') : toggleDayNight('night')
});

toggleDayNight();
</script>

<%in _footer.cgi %>
