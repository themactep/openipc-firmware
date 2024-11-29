#!/bin/haserl
<%in _common.cgi %>
<%
plugin="users"
plugin_name="Users"
page_title="Users"

conf_file=/tmp/passwd

if [ -n "$POST_action" ] && [ "$POST_action" = "create" ]; then
	user_name="$POST_user_name"
	user_name_new="$POST_user_name_new"
	user_password="$POST_user_password"
	user_full_name="$POST_user_full_name"
	user_home="$POST_user_home"
	user_shell="$POST_user_shell"
	user_group="$POST_user_group"

	[ -n "$user_name_new" ] && user_name=$user_name_new

	error_if_empty "$user_name" "User name cannot be empty."
	error_if_empty "$user_password" "User password cannot be empty."

	if [ -z "$error" ]; then
		if grep -q "^$user_name:" /etc/passwd; then
			alert_append "warning" "User $user_name found."
		else
			adduser $user_name -h ${user_home:-/dev/null} -s ${user_shell:-/bin/false} -G ${user_group:-users} -D -g "$user_full_name"
			if [ $? -eq 0 ]; then
				alert_append "success" "User $user_name created."
			else
				set_error_flag "Failed to create user $user_name."
			fi
		fi

		if [ -z "$error" ]; then
			result=$(echo "$user_name:$user_password" | chpasswd -c sha512 2>&1)
			if [ $? -eq 0 ]; then
				alert_append "success" "Password for ${user_name} set."
				redirect_back
			else
				alert_append "danger" "$result"
			fi
		fi
	fi
fi

users=$(awk 'BEGIN { FS = ":" } ; { if ($3 > 1000) print $1 }' /etc/passwd)

default_for user_home "/dev/null"
default_for user_shell "/bin/false"
default_for user_group "users"
%>

<%in _header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post" class="mb-4">
<div class="row row-cols-1 row-cols-md-2 row-cols-xl-3">
<div class="col">
<% field_hidden "action" "create" %>
<% field_select "user_name" "Username" "$users" %>
<% field_text "user_name_new" "Username" "<a href=\"#\" id=\"hide_new_user\">Select an existing user</a>" %>
<% field_password "user_password" "Password" %>
</div>
<div class="col">
<% field_text "user_full_name" "Full name" %>
<% field_text "user_home" "Home directory" %>
</div>
<div class="col">
<% field_text "user_shell" "Shell" %>
<% field_text "user_group" "Group" %>
</div>
</div>
<% button_submit %>
</form>
<p><a href="#" id="show_new_user">Create a new user</a></p>

<div class="alert alert-dark ui-debug">
<h4 class="mb-3">Debug info</h4>
<% ex "cat /etc/passwd" %>
<% ex "cat /etc/shadow" %>
<% ex "cat /etc/group" %>
</div>

<script>
function showNewUser() {
	$('#user_full_name').disabled = false;
	$('#user_name_new_wrap').classList.remove('d-none');
	$('#user_name_wrap').classList.add('d-none');
	$('#user_name').value = '';
}

function hideNewUser() {
	$('#user_full_name').disabled = true;
	$('#user_name_wrap').classList.remove('d-none');
	$('#user_name_new_wrap').classList.add('d-none');
	$('#user_name_new').value = '';
}

$('#show_new_user').onclick = (ev) => {
	ev.preventDefault();
	showNewUser();
}

$('#hide_new_user').onclick = (ev) => {
	ev.preventDefault();
	hideNewUser();
}

if ($('#user_name_new').value == "") {
	hideNewUser();
} else {
	showNewUser();
}

$('#user_home').disabled = true;
$('#user_shell').disabled = true;
$('#user_group').disabled = true;
</script>

<%in _footer.cgi %>
