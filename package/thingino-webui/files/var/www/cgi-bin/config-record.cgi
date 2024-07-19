#!/usr/bin/haserl

<%in p/common.cgi %>

<%
	plugin="record"
	plugin_name="Local Recording"
	page_title="Local Recording"
	params="enabled prefix path format interval loop led_enabled led_gpio led_interval"

	tmp_file=/tmp/$plugin

	config_file="${ui_config_dir}/${plugin}.conf"
	[ ! -f "$config_file" ] && touch $config_file

	record_control=/etc/init.d/S96record

	if [ "POST" = "$REQUEST_METHOD" ]; then
		# parse values from parameters
		for p in $params; do
			eval ${plugin}_${p}=\$POST_${plugin}_${p}
			sanitize "${plugin}_${p}"
		done; unset p

		# validation

		if [ -z "$record_led_gpio" ]; then
			record_led_enabled=false
			echo "LED GPIO PIN not defined. Disabling blink" >> /tmp/webui.log
		fi

		if [ -z "$error" ]; then
			# Check if record path starts and ends with "/"
			if [ -z $record_path ]; then
			 	echo "Record path cannot be empty. Disabling." >> /tmp/webui.log
				record_enable=false
				record_path="/mnt/mmcblk0p1/"
			else
				if [[ $record_path != "/mnt/*" ]]; then
					echo "Record path does not seem to be in sd card location. Disabling" >> /tmp/webui.log
					record_enable=false
					record_path="/mnt/mmcblk0p1/"
				fi
				if [[ $record_path != "/mnt/*/" ]]; then
					echo "record path does not end with "/". Adding" >> /tmp/webui.log
					record_path="$record_path/"
				fi
			fi

			:>$tmp_file
			for p in $params; do
				echo "${plugin}_${p}=\"$(eval echo \$${plugin}_${p})\"" >>$tmp_file
			done; unset p
			mv $tmp_file $config_file

			# Check if record path exists
			if [ ! -d "$record_path" ]; then
				echo "Record path $record_path does not exist. Creating" >> /tmp/webui.log
				mkdir -p "$record_path" >> /tmp/webui.log
			fi

			if [ -f "$record_control" ]; then
				$record_control restart >> /tmp/webui.log
			else
				echo "$record_control not found" >> /tmp/webui.log
			fi

			update_caminfo
			redirect_to "$SCRIPT_NAME"
		fi
	else
		include $config_file

		# default values
		[ -z "$record_enabled" ] && record_enabled=false
		[ -z "$record_prefix" ] && record_prefix="thingino-"
		[ -z "$record_path" ] && record_path="/mnt/mmcblk0p1/"
		[ -z "$record_format" ] && record_format=".mp4"
		[ -z "$record_interval" ] && record_interval=60
		[ -z "$record_loop" ] && record_loop=true
		[ -z "$record_led_enabled" ] && record_led_enabled=false
		[ -z "$record_led_gpio" ] && record_led_gpio=$(get gpio_led_r)
		[ -z "$record_led_interval" ] && record_led_interval=1
	fi
%>

<%in p/header.cgi %>

<%	if ! ls /dev/mmc* >/dev/null 2>&1; then %>
	<div class="alert alert-danger">
		<h4>Does this camera support SD Card?</h4>
		<p>Your camera does not have an SD Card slot or SD Card is not inserted.</p>
	</div>
<% else %>

<form action="<%= $SCRIPT_NAME %>" method="post">
	<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
		<div class="col">
			<h3>Recording</h3>
			<% field_switch "record_enabled" "Enable Recording" %>
			<% field_text "record_prefix" "Filename Prefix" "e.g. thingino-yyyy-mm-dd_HH-MM-SS.mp4" "thingino-" %>
			<% field_text "record_path" "Record Directory in SD Card" "Directory will be created if non-existent" "/"%>
			<% field_select "record_format" "Output File Format" ".mov, .mp4, .avi" %>
			<% field_number "record_interval" "Recording Interval (seconds)" "" "How long to record in each file" %>
			<% field_checkbox "record_loop" "Loop Recording" "Delete oldest file to make space for newer recordings"%>
			<br>
			<% button_submit %>
		</div>

		<div class="col col-12 col-xl-4">
			<h3>Status LED</h3>
			<% field_switch "record_led_enabled" "Blink LED" "Flash a status LED when recording"%>
			<% field_number "record_led_gpio" "LED GPIO Pin" "" "Default: gpio_led_r" %>
			<% field_range "record_led_interval" "Blink Interval (seconds)" "0,3.0,0.5" "Set to 0 for always on"%>
		</div>
		
		<div class="col">
			<h3>Configuration</h3>
			<% [ -f $config_file ] && ex "cat $config_file" %>
		</div>
	</div>
	
</form>

<% fi %>
<%in p/footer.cgi %>
