#!/usr/bin/haserl
<% SSH_AUTH_KEYS=/root/.ssh/authorized_keys %>
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
<meta charset="utf-8">
<meta content="width=device-width,initial-scale=1" name="viewport">
<title>Thingino Initial Configuration</title>
<link rel="stylesheet" href="/bootstrap.min.css">
<style>
.container {max-width:28rem}
h1,h2 {font-weight:400}
h1 {font-size:4.5rem}
h1 span {color:#f80}
h2 {font-size:1.8rem}
</style>
<script src="/bootstrap.bundle.min.js"></script>
</head>
<body>
<header class="my-4 text-center">
<div class="container">
<h1>th<span>ing</span>ino</h1>
<h2>Initial Configuration</h2>
</div>
</header>
<main>
<div class="container">
<%
if [ "POST" = "$REQUEST_METHOD" ]; then
	wlanssid="$POST_wlanssid"
	wlanpass="$POST_wlanpass"
	hostname="$POST_hostname"
	rootpass="$POST_rootpass"
	rootpkey="$POST_rootpkey"
fi

if [ "POST" = "$REQUEST_METHOD" ] && [ "save" = "$POST_mode" ]; then
	fw_setenv wlanssid $wlanssid
	fw_setenv wlanpass $wlanpass
	fw_setenv hostname $hostname
	echo "root:${rootpass}" | chpasswd -c sha512
	echo "$rootpkey" > $SSH_AUTH_KEYS
	echo "<h1 class=\"mt-5 text-center display-1\">Done. Rebooting...</h1>"
	reboot -d 5
elif [ "GET" = "$REQUEST_METHOD" ] || [ "edit" = "$POST_mode" ]; then %>
<form action="<%= $SCRIPT_NAME %>" method="post" class="my-3 needs-validation" novalidate style="max-width:26rem">
<div class="mb-3">
<label class="form-label">Wireless Network Name (SSID)</label>
<input class="form-control form-control-lg bg-light text-dark" type="text" name="wlanssid" value="<%= $wlanssid %>" required autocapitalize="none">
<div class="invalid-feedback">Please enter network name</div>
</div>
<div class="mb-3">
<label class="form-label">Wireless Network Password</label>
<input class="form-control form-control-lg bg-light text-dark" type="text" name="wlanpass" id="wlanpass" value="<%= $wlanpass %>" required autocapitalize="none">
<div class="invalid-feedback">Please enter password</div>
</div>
<div class="mb-3">
<label class="form-label">Camera Hostname</label>
<input class="form-control form-control-lg bg-light text-dark" type="text" name="hostname" value="<%= $hostname %>" required autocapitalize="none">
<div class="invalid-feedback">Please enter hostname</div>
</div>
<div class="mb-3">
<label class="form-label">User <b>root</b> Password</label>
<input class="form-control form-control-lg bg-light text-dark" type="text" name="rootpass" id="rootpass" value="<%= $rootpass %>" required autocapitalize="none">
<div class="invalid-feedback">Please enter password</div>
</div>
<div class="mb-3">
<label class="form-label">User <b>root</b> Public SSH Key (optional)</label>
<textarea class="form-control form-control-lg bg-light text-dark text-break" name="rootpkey" id="rootpkey" rows="8"><%= $rootpkey %></textarea>
</div>
<div class="mb-3">
<input type="submit" value="Save Credentials" class="btn btn-primary">
</div>
</form>
<script>
(() => {
	const forms = document.querySelectorAll('.needs-validation');
	Array.from(forms).forEach(form => {
		form.addEventListener('submit', event => {
			if (!form.checkValidity()) {
				event.preventDefault()
				event.stopPropagation()
			}
			form.classList.add('was-validated')
		}, false)
	})
})()
</script>
<% else %>
<div class="alert alert-secondary my-3">
<h3>Ready to connect</h3>
<p>Please double-check the enterred data and correct it if you see an error!</p>

<form action="<%= $SCRIPT_NAME %>" method="POST" class="mb-3">
<input type="hidden" name="mode" value="edit">
<input type="hidden" name="wlanssid" value="<%= $wlanssid %>">
<input type="hidden" name="wlanpass" value="<%= $wlanpass %>">
<input type="hidden" name="hostname" value="<%= $hostname %>">
<input type="hidden" name="rootpass" value="<%= $rootpass %>">
<input type="hidden" name="rootpkey" value="<%= $rootpkey %>">
<input type="submit" class="btn btn-danger" value="Oops, this requires a correction">
</form>

<dl>
<dt>Wireless Network SSID</dt>
<dd class="lead"><%= $wlanssid %></dd>
<dt>Wireless Network Password</dt>
<dd class="lead text-break"><%= $wlanpass %></dd>
<dt>Camera Hostname</dt>
<dd class="lead"><%= $hostname %></dd>
<dt>User <b>root</b> Password</dt>
<dd class="lead"><%= $rootpass %></dd>
<dt>User <b>root</b> Public SSH Key</dt>
<dd class="lead text-break"><%= $rootpkey %></dd>
</dl>

<form action="<%= $SCRIPT_NAME %>" method="POST">
<input type="hidden" name="mode" value="save">
<input type="hidden" name="wlanssid" value="<%= $wlanssid %>">
<input type="hidden" name="wlanpass" value="<%= $wlanpass %>">
<input type="hidden" name="hostname" value="<%= $hostname %>">
<input type="hidden" name="rootpass" value="<%= $rootpass %>">
<input type="hidden" name="rootpkey" value="<%= $rootpkey %>">
<input type="submit" class="btn btn-success" value="Looks good. Proceed with reboot">
</form>

</div>
<% fi %>

</div>
</main>
</body>
</html>
