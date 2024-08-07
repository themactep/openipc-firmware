MOTORS_SITE_METHOD = git
MOTORS_SITE = https://github.com/gtxaspec/ingenic-motor.git
MOTORS_SITE_BRANCH = master
MOTORS_VERSION = $(shell git ls-remote $(MOTORS_SITE) $(MOTORS_SITE_BRANCH) | head -1 | cut -f1)

MOTORS_LICENSE = MIT
MOTORS_LICENSE_FILES = LICENSE

define MOTORS_BUILD_CMDS
	$(TARGET_CC) -Os -s $(@D)/motor.c -o $(@D)/motors
	$(TARGET_CC) -Os -s $(@D)/motor-daemon.c -o $(@D)/motors-daemon
endef

ifeq ($(BR2_MOTORS_INVERT_GPIO_DIR),y)
define MOTORS_INSTALL_TARGET_CMDS
	$(INSTALL) -m 755 -d $(TARGET_DIR)/etc/init.d
	$(INSTALL) -m 755 -t $(TARGET_DIR)/etc/init.d/ $(MOTORS_PKGDIR)/files/S09motor
	$(INSTALL) -m 755 -d $(TARGET_DIR)/etc/modprobe.d
	$(INSTALL) -m 644 -t $(TARGET_DIR)/etc/modprobe.d/ $(MOTORS_PKGDIR)/files/motor.conf

	$(INSTALL) -m 0755 -D $(@D)/motors $(TARGET_DIR)/usr/bin/motors
	$(INSTALL) -m 0755 -D $(@D)/motors-daemon $(TARGET_DIR)/usr/bin/motors-daemon
endef
else
define MOTORS_INSTALL_TARGET_CMDS
	$(INSTALL) -m 755 -d $(TARGET_DIR)/etc/init.d
	$(INSTALL) -m 755 -t $(TARGET_DIR)/etc/init.d/ $(MOTORS_PKGDIR)/files/S09motor

	$(INSTALL) -m 0755 -D $(@D)/motors $(TARGET_DIR)/usr/bin/motors
	$(INSTALL) -m 0755 -D $(@D)/motors-daemon $(TARGET_DIR)/usr/bin/motors-daemon
endef
endif

$(eval $(generic-package))
