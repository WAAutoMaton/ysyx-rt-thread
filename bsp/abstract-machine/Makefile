ARCH ?= native
RTCONFIG_H = rtconfig.h

NAME = rtthread
SRCS = 
include $(AM_HOME)/Makefile

$(RTCONFIG_H):
	touch $@
	scons --useconfig=.config

init: $(RTCONFIG_H)

.PHONY: init
