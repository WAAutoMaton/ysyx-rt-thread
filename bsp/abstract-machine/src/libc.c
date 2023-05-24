#include <klib.h>
#include <rtthread.h>

char *strchr(const char *s, int c) {
  assert(0);
}

char *strstr(const char *haystack, const char *needle) {
  return rt_strstr(haystack, needle);
}
