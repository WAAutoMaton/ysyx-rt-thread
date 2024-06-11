#include <am.h>
#include <klib.h>
#include <rtthread.h>

static Context* ev_handler(Event e, Context *c) {
  switch (e.event) {
    case EVENT_YIELD: {
      rt_thread_t self= rt_thread_self();
      rt_ubase_t *args = (void*)self->user_data;
      Context** from = (Context**)args[0], **to = (Context**)args[1];
      if (from!=NULL)
        *from = c;
      c = *to;
      break;
    }
    case EVENT_IRQ_TIMER: {
      break;
    }
    case EVENT_IRQ_IODEV: break;
    default: printf("Unhandled event ID = %d\n", e.event); assert(0);
  }
  return c;
}

void __am_cte_init() {
  cte_init(ev_handler);
}


void rt_hw_context_switch(rt_ubase_t from, rt_ubase_t to) {
  rt_thread_t self= rt_thread_self();
  rt_ubase_t prev_user_data = self->user_data;
  rt_ubase_t user_data[2] = {from, to};
  self->user_data = (rt_ubase_t)user_data;
  yield();
  self->user_data = prev_user_data;
}

void rt_hw_context_switch_to(rt_ubase_t to) {
  rt_hw_context_switch(0, to);
}

void rt_hw_context_switch_interrupt(void *context, rt_ubase_t from, rt_ubase_t to, struct rt_thread *to_thread) {
  assert(0);
}


static void tentry_entry(void *parameter) {
  uintptr_t *args = parameter;
  void (*tentry)() = (void*)args[1];
  tentry(args[0]);
  void (*texit)() = (void*)args[2];
  texit(); 
}
rt_uint8_t *rt_hw_stack_init(void *tentry, void *parameter, rt_uint8_t *stack_addr, void *texit) {
  stack_addr = (rt_uint8_t*)((rt_ubase_t)stack_addr & ~0xf);
  uintptr_t *args = (void*)(stack_addr-32);
  stack_addr-=32;
  args[0]=(uintptr_t)parameter;
  args[1]=(uintptr_t)tentry;
  args[2]=(uintptr_t)texit;
  Context* c = kcontext((Area){0, stack_addr}, tentry_entry, args);
  return (rt_uint8_t*)c;
}
