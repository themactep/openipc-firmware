#!/bin/haserl
<%in _common.cgi %>
<%
page_title="File Manager"

if [ -n "$GET_dl" ]; then
	file=$GET_dl
	check_file_exist $file
	echo -en "HTTP/1.0 200 OK\r\n\
Date: $(time_http)\r\n\
Server: $SERVER_SOFTWARE\r\n\
Content-type: application/octet-stream\r\n\
Content-Disposition: attachment; filename=$(basename $file)\r\n\
Content-Length: $(stat -c%s $file)\r\n\
Cache-Control: no-store\r\n\
Pragma: no-cache\r\n\
\r\n"
	cat $file
	redirect_to $SCRIPT_NAME
fi
%>
<%in _header.cgi %>
<%
path2links() {
	echo -n "<a href=\"?cd=/\">⌂</a>"
	for d in ${1//\// }; do
		d2="$d2/$d"
		echo -n "/<a href=\"?cd=$d2\">$d</a>"
	done
}
# expand traversed path to a real directory name
dir=$(cd ${GET_cd:-/}; pwd)
# no need for POSIX awkward double root
dir=$(echo $dir | sed s#^//#/#)
%>
<h4><% path2links "$dir" %></h4>
<table class="table files">
<thead>
<tr>
<th>Name</th>
<th>Size</th>
<th>Permissions</th>
<th>Date</th>
</tr>
</thead>
<tbody>
<%
lsfiles=$(ls -ALlp --group-directories-first $dir)
IFS=$'\n'
for line in $lsfiles; do
	echo "<tr>"
	name=${line##* }; line=${line% *}
	path=$(echo "$dir/$name" | sed s#^//#/#)
	echo "<td>"
	if [ -d "$path" ]; then
		echo "<a href=\"?cd=$path\" class=\"fw-bold\">$name</a>"
	else
		echo "<a href=\"?dl=$path\">$name</a>"
	fi
	echo "</td>"
	echo "<td>$(echo $line | awk '{print $5}')</td>"
	echo "<td>$(echo $line | awk '{print $1}')</td>"
	echo "<td>$(echo $line | awk '{print $6,$7,$8}')</td>"
	echo "</tr>"
done
IFS=$IFS_ORIG
%>
</tbody>
</table>
<%in _footer.cgi %>