#!/usr/bin/env python3

import sys, os, shutil
from pathlib import Path

AM_HOME = Path(os.environ["AM_HOME"])
AM_KERNELS_HOME = (AM_HOME / ".." / "am-kernels").resolve()
app_dir_list = AM_KERNELS_HOME / "kernels" / "hello"
ARCH = "native"
Path("build").mkdir(exist_ok=True)
am_app_mk_fp = open("am-apps.mk", "w")
am_app_c_fp  = open("build/am-apps.c" , "w")

def integrate(app_dir):
    app_name = app_dir.name
    os.system("make -j ARCH=" + ARCH + " -C " + str(app_dir))
    dst = Path("build") / ARCH / "am-apps" / app_name
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copytree(app_dir / "build" / ARCH / "", dst, dirs_exist_ok=True)
    objs = dst.rglob("*.o")
    for obj in objs:
        os.system("objcopy --prefix-symbols=__am_" + app_name + "_ " + str(obj))
        am_app_mk_fp.write("SRCS += " + str(obj.relative_to("build/" + ARCH)) + "\n")
    am_app_c_fp.write(f"""extern int __am_{app_name}_main(const char *);
static void am_{app_name}(int argc, char *argv[]) {{
  __am_{app_name}_main(argc >= 2 ? argv[1] : "");
}}
MSH_CMD_EXPORT(am_{app_name}, AM {app_name});""")

am_app_mk_fp.write("SRCS += build/am-apps.c\n")
am_app_c_fp.write("#include <rtthread.h>\n")
integrate(app_dir_list)
am_app_mk_fp.close()
am_app_c_fp.close()
