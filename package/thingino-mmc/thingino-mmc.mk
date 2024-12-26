define THINGINO_MMC_INSTALL_TARGET_CMDS
	$(INSTALL) -m 755 -d $(TARGET_DIR)/etc/init.d
	$(INSTALL) -m 755 -t $(TARGET_DIR)/etc/init.d $(THINGINO_MMC_PKGDIR)/files/S09mmc
	$(INSTALL) -m 755 -d $(TARGET_DIR)/usr/sbin
	$(INSTALL) -m 755 -t $(TARGET_DIR)/usr/sbin $(THINGINO_MMC_PKGDIR)/files/mmc
endef

$(eval $(generic-package))
