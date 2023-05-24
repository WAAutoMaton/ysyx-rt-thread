#include <am.h>
#include <klib.h>

void rt_hw_interrupt_enable() {
  assert(0);
}

void rt_hw_interrupt_disable() {
  iset(0);
}
