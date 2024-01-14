#!/usr/bin/env python3

import sys, os, shutil, subprocess
from pathlib import Path

AM_HOME = Path(os.environ["AM_HOME"])
AM_KERNELS_HOME = (AM_HOME / ".." / "am-kernels").resolve()
ARCH = "native"
Path("build").mkdir(exist_ok=True)
am_app_mk_fp = open("am-apps.mk", "w")
am_app_c_fp  = open("build/am-apps.c" , "w")
lib_sym = [
  "memset", "memcpy", "memmove", "memcmp",
  "strlen", "strcat", "strcpy", "strncpy", "strcmp", "strncmp",
  "srand", "rand", "malloc", "free", "abs", "atoi",
  "printf", "sprintf", "snprintf", "vsprintf", "vsnprintf",
]
am_init_sym = [ "trm_init", "ioe_init", "cte_init", "vme_init", "mpe_init" ]
app_dir_list = [
  AM_KERNELS_HOME / "kernels" / "hello",
  AM_KERNELS_HOME / "benchmarks" / "microbench",
  AM_KERNELS_HOME / "kernels" / "typing-game",
]

def read_lib_symbols(lib):
    libfile = AM_HOME / lib / "build" / f"{lib}-{ARCH}.a"
    if (not libfile.exists()):
        os.system("make -j ARCH=" + ARCH + " -C " + str(AM_HOME / lib))
    cmd = f"nm -g --defined-only --format=just-symbols {str(libfile)}"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    global lib_sym
    lib_sym += res.stdout.strip().split('\n')

def integrate(app_dir):
    app_name = app_dir.name.replace("-", "_")
    os.system(f"make -j ARCH={ARCH} -C {str(app_dir)}")
    dst = Path("build") / ARCH / "am-apps" / app_name
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copytree(app_dir / "build" / ARCH / "", dst, dirs_exist_ok=True)
    objs = dst.rglob("*.o")
    redefine_sym_file = "redefine_sym.txt"
    redefine_sym_fp = open(redefine_sym_file, "w")
    for f in lib_sym:
        if f in am_init_sym:
            redefine_sym_fp.write(f"__am_{app_name}_{f} __dummy_{f}\n")
        else:
            redefine_sym_fp.write(f"__am_{app_name}_{f} {f}\n")
    redefine_sym_fp.close()
    for obj in objs:
        os.system(f"objcopy --prefix-symbols=__am_{app_name}_ {str(obj)}")
        os.system(f"objcopy --redefine-syms=redefine_sym.txt {str(obj)}")
        am_app_mk_fp.write("SRCS += " + str(obj.relative_to("build/" + ARCH)) + "\n")
    os.remove(redefine_sym_file)
    am_app_c_fp.write(f"""extern int __am_{app_name}_main(const char *);
static void am_{app_name}(int argc, char *argv[]) {{
  heap = am_apps_heap;
  __am_{app_name}_main(argc >= 2 ? argv[1] : "");
}}
MSH_CMD_EXPORT(am_{app_name}, AM {app_name});""")

read_lib_symbols("am")
read_lib_symbols("klib")

am_app_mk_fp.write("SRCS += build/am-apps.c\n")
am_app_c_fp.write("""#include <am.h>
#include <rtthread.h>
extern Area am_apps_heap;
bool __dummy_ioe_init() { return true; }
bool __dummy_cte_init(Context *(*handler)(Event ev, Context *ctx)) { return true; }
bool __dummy_vme_init(void *(*pgalloc)(int), void (*pgfree)(void *)) { return true; }
bool __dummy_mpe_init(void (*entry)()) { return true; }
""")
for app in app_dir_list:
    integrate(app)
am_app_mk_fp.close()
am_app_c_fp.close()
