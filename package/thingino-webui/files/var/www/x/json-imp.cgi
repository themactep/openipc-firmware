#!/bin/sh
# shellcheck disable=SC2039
. ./_json.sh

bad_request() {
	http_400
	echo
	echo "$1"
	exit 1
}

we_are_good() {
	echo "we are good"
}

unknown_command() {
	bad_request "unknown command"
}

unknown_value() {
	bad_request "unknown value"
}

urldecode() {
	local i="${*//+/ }"
	echo -e "${i//%/\\x}"
}

# parse parameters from query string
[ -n "$QUERY_STRING" ] && eval $(echo "$QUERY_STRING" | sed "s/&/;/g")

# quit if no command sent
[ -z "$cmd" ] && bad_request "missing required parameter cmd"

val="$(urldecode "$val")"

# check lower limit
case "$cmd" in
	aivol | aovol)
		[ "$val" -lt -30 ] && unknown_value
		;;
	ains)
		[ "$val" -lt -1 ] && unknown_value
		;;
	aecomp | aialc | aigain | aogain | brightness | contrast | defogstrength | dpc | drc | flicker | flip | hilight | hue | ispmode | saturation | setosdalpha | sharpness | sinter | temper)
		[ "$val" -lt -0 ] && unknown_value
		;;
	*) ;;
esac

# check upper limit
case "$cmd" in
	ispmode)
		[ "$val" -gt 1 ] && unknown_value
		;;
	flicker)
		[ "$val" -gt 2 ] && unknown_value
		;;
	ains | flip)
		[ "$val" -gt 3 ] && unknown_value
		;;
	aialc)
		[ "$val" -gt 7 ] && unknown_value
		;;
	hilight)
		[ "$val" -gt 10 ] && unknown_value
		;;
	aigain | aogain)
		[ "$val" -gt 31 ] && unknown_value
		;;
	aivol | aovol)
		[ "$val" -gt 120 ] && unknown_value
		;;
	aecomp | brightness | contrast | defogstrength | dpc | drc | hue | saturation | setosdalpha | sharpness | sinter | temper)
		[ "$val" -gt 255 ] && unknown_value
		;;
	*) ;;

esac

# check non-numeric values
case "$cmd" in
	aihpf | aiaec | aiagc)
		case "$val" in
			on | off)
				we_are_good
				;;
			*)
				unknown_value
				;;
		esac
		;;
	*) ;;
esac

case "$cmd" in
	daynight)
		[ "$val" -eq 1 ] && val="night" || val="day"
		daynight $val
		payload="{\"mode\":\"$(daynight status)\"}"
		;;
	ir850 | ir940 | white)
		irled ${val:-read} $cmd
		payload="{\"command\":\"$command\",\"result\":\"$(irled status $cmd)\"}"
		;;
	ircut)
		ircut $val
		payload="{\"ircut\":\"$val\"}"
		;;
	setosd)
		handle=`echo "$val" | cut -d" " -f1`
		# save to temp config
		sed -i "/^$cmd $handle/d" /tmp/imp.conf
		echo "$cmd $val" >> /tmp/imp.conf
		command="imp-control $cmd $val"
		result=$($command)
		payload="{\"command\":\"$command\",\"result\":\"$result\"}"
		;;
	*)
		# save to temp config
		sed -i "/^$cmd/d" /tmp/imp.conf
		echo "$cmd $val" >> /tmp/imp.conf
		command="imp-control $cmd $val"
		result=$($command)
		payload="{\"command\":\"$command\",\"result\":\"$result\"}"
		;;
esac

json_ok "$payload"
