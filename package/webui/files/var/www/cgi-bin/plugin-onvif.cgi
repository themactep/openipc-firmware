#!/usr/bin/haserl
<%in p/common.cgi %>
<%
plugin="onvif"
plugin_name="ONVIF Server"
page_title="ONVIF Server"
params="enabled"

tmp_file=/tmp/$plugin

config_file="${ui_config_dir}/${plugin}.conf"
[ ! -f "$config_file" ] && touch $config_file

onvif_control=/etc/init.d/S96onvif

if [ "POST" = "$REQUEST_METHOD" ]; then
	# parse values from parameters
	for p in $params; do
		eval ${plugin}_${p}=\$POST_${plugin}_${p}
		sanitize "${plugin}_${p}"
	done; unset p

	# validation

	if [ -z "$error" ]; then
		:>$tmp_file
		for p in $params; do
			echo "${plugin}_${p}=\"$(eval echo \$${plugin}_${p})\"" >>$tmp_file
		done; unset p
		mv $tmp_file $config_file

		if [ -f "$onvif_control" ]; then
			$onvif_control restart >> /tmp/webui.log
		else
			echo "$onvif_control not found" >> /tmp/webui.log
		fi

		update_caminfo
		redirect_to "$SCRIPT_NAME"
	fi
else
	include $config_file

	# default values
	[ -z "$onvid_enabled" ] && onvid_enabled=false
fi
%>
<%in p/header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
<div class="row g-4 mb-4">
<div class="col col-12 col-xl-4">
<% field_switch "onvif_enabled" "Enable ONVIF Server" %>
</div>
<div class="col col-12 col-xl-4">
</div>
<div class="col col-12 col-xl-4">
<% [ -f $config_file ] && ex "cat $config_file" %>
</div>
</div>

<% button_submit %>
</form>

<%in p/footer.cgi %>
