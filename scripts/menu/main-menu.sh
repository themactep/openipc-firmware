#!/bin/bash

source ./scripts/menu/menu-common.sh

function main_menu() {
	check_and_install_dialog
	while true; do
		CHOICE=$("${DIALOG_COMMON[@]}" --help-button --menu "Select an option:" 18 110 30 \
			"bootstrap" "Install prerequisite software necessary for the compilation process" \
			"menuconfig" "Proceed to the buildroot menu (toolchain, kernel, and rootfs)" \
			"nconfig" "Proceed to the buildroot menu (toolchain, kernel, and rootfs)" \
			"br-linux-menuconfig" "Proceed to the Linux Kernel menu configuration" \
			"br-linux-nconfig" "Proceed to the Linux Kernel menu configuration" \
			"br-busybox-menuconfig" "Proceed to the Busybox menu configuration" \
			"defconfig" "(Re)create config file" \
			"clean" "Clean before reassembly"  \
			"cleanbuild" "Build everything from scratch" \
			"distclean" "Remove all cached build files from current profile"  \
			"make" "Generate firmware" \
			"upgrade_ota" "Upload the full firmware file to the camera over network, and flash it"  \
			"update_ota" "Upload the update firmware file to the camera over network, and flash it"  \
			3>&1 1>&2 2>&3)

			exit_status
	done
}

function show_help() {
	local item=$1
	case "$item" in
		"HELP bootstrap")
			show_help_msgbox "The 'Bootstrap' option initiates the installation of all necessary prerequisite software required for the compilation of the firmware.\n\nThis includes tools and libraries that are essential for building the firmware from source. Selecting this will ensure your environment is correctly set up to proceed with building Thingino without encountering missing dependencies.\n\nRequires super-user privileges." 13 80;;
		"HELP menuconfig")
			show_help_msgbox "Launches a graphical interface for configuring the toolchain, kernel options, and the packages that will be included in your root filesystem. It's a crucial step for customizing your build according to your needs." 8;;
		"HELP nconfig")
			show_help_msgbox "Launches a graphical interface for configuring the toolchain, kernel options, and the packages that will be included in your root filesystem. It's a crucial step for customizing your build according to your needs." 8;;
		"HELP br-linux-menuconfig")
			show_help_msgbox "Launches a graphical interface for configuring the Linux Kernel." 5;;
		"HELP br-linux-nconfig")
			show_help_msgbox "Launches a graphical interface for configuring the Linux Kernel." 5;;
		"HELP clean")
			show_help_msgbox "The 'clean' command removes most of the files generated during the build process but preserves your configuration settings. This allows you to rebuild your firmware quickly without starting from scratch." 8;;
		"HELP distclean")
			show_help_msgbox "Choosing 'distclean' will clean your build environment more thoroughly than 'clean'. It removes all generated files, including your configuration and all cached build files. Use this to completely restart the build process." 8;;
		"HELP make")
			show_help_msgbox "This option starts the compilation process for the entire firmware project based on your current configuration settings. It's a key step in creating the custom thingino firmware for your device." 7;;
		"HELP upgrade_ota")
			show_help_msgbox "This function initiates an Over-the-Air (OTA) upgrade using the full firmware image. You'll need to specify the target device's IP address. It's used for comprehensive updates that include the bootloader, kernel, and filesystem." 8;;
		"HELP update_ota")
			show_help_msgbox "This option performs an OTA update with just the firmware update image, excluding the bootloader. You'll need to provide the target device's IP address. It's ideal for routine software updates after the initial full installation." 8;;
		"HELP defconfig")
			show_help_msgbox "The 'defconfig' option recreates the default configuration file. It's used to reset your configuration settings to the default state, which can be helpful if you want to start the configuration process anew." 8;;
		"HELP br-busybox-menuconfig")
			show_help_msgbox "Proceed to the Busybox menu configuration. This allows you to customize the Busybox settings." 7;;
		"HELP cleanbuild")
			show_help_msgbox "The 'cleanbuild' option builds everything from scratch. It removes all previously built files and starts the build process from the beginning, ensuring a clean build environment." 7;;
		*)
			show_help_msgbox "No help information is available for the selected item. Please choose another option or consult the thingino wiki for more details.";;
	esac
}

execute_choice() {
	case $1 in
		bootstrap)
			sudo make $1
			sleep 2
			;;
		make)
			make $1
			exit
			;;
		menuconfig | br-linux-menuconfig | nconfig| br-linux-nconfig)
			make $1
			#savedefconfig future user box
			#exit
			;;
		clean | distclean)
			make $1
			;;
		upgrade_ota | update_ota)
			local action="upgrade"
			local warning="You are about to start a full upgrade, which includes upgrading the device's bootloader. This operation is critical and may disrupt the device's functionality if it fails. Proceed with caution. Are you sure you want to continue with the flashing process?"
			[ "$1" = "update_ota" ] && {
				action="update"
				warning="Flashing will begin. Be careful, as this might disrupt the device's operation if it fails. Are you sure you want to continue?"
			}

			# Fix for containers, or environments with broken privs

			"${DIALOG_COMMON[@]}" --title "Input IP" --inputbox "Enter the IP address for OTA $action" 8 78 2>"$temp_ip"
			exit_status=$?

			if [ $exit_status -ne 0 ]; then
				echo "User canceled the operation."
				rm -f "$temp_ip"
				return
			fi

			IP=$(<"$temp_ip")

			if [ -z "$IP" ]; then
				DIALOGRC=$temp_rc "${DIALOG_COMMON[@]}" --title "Warning" --msgbox "No IP address entered, returning to main menu." 5 78
				rm -f "$temp_ip"
				return
			fi

			if DIALOGRC=$temp_rc "${DIALOG_COMMON[@]}" --title "Warning" --yesno "$warning" 12 78; then
				echo "Proceeding with OTA $action to $IP..."
				make $1 IP=$IP
				exit
			else
				echo "OTA $action canceled by user."
			fi

			rm -f $temp_ip
			rm -f $temp_rc
			;;
		*)
			echo "Invalid choice."
			;;
	esac
}

# Start the main menu
main_menu
