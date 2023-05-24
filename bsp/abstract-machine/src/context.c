#include <klib.h>
#include <rtthread.h>

void rt_hw_context_switch_to(rt_ubase_t to) {
  assert(0);
}

void rt_hw_context_switch(rt_ubase_t from, rt_ubase_t to) {
  assert(0);
}

void rt_hw_context_switch_interrupt(void *context, rt_ubase_t from, rt_ubase_t to, struct rt_thread *to_thread) {
  assert(0);
}

rt_uint8_t *rt_hw_stack_init(void *tentry, void *parameter, rt_uint8_t *stack_addr, void *texit) {
  assert(0);
  return NULL;
}
