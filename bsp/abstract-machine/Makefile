ARCH ?= native
FILE_MK = files.mk
FILE_TMP = .tmp.$(FILE_MK)
RTCONFIG_H = rtconfig.h

NAME = rtthread
SRCS = $(shell find src -name "*.c")
CFLAGS += -DHAVE_CCONFIG_H -D__RTTHREAD__
CFLAGS += -Wno-nonnull-compare
LDFLAGS += extra.ld
-include $(FILE_MK)
include $(AM_HOME)/Makefile

$(RTCONFIG_H):
	touch $@
	scons --useconfig=.config

$(FILE_MK): $(RTCONFIG_H)
	scons -c
	scons --verbose -n > $(FILE_TMP)
	cat $(FILE_TMP) | grep -o '[^ ]*.c$$' | awk '{print "SRCS += " $$1}' > $@
	cat $(FILE_TMP) | grep 'gcc ' | head -n 1 | grep -o " -I[^ ]*" | awk '{print "CFLAGS += " $$1}' >> $@
	rm $(FILE_TMP)
	if [ "`sed -n '3p' $^`"x = x ]; then sed -i -e '2a#include "extra.h"' $^; fi

menuconfig:
	scons --menuconfig
	scons --genconfig
	$(MAKE) init

init: $(FILE_MK)

.PHONY: init menuconfig
