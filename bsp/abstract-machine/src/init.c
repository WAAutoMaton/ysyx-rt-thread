#include <am.h>
#include <rtthread.h>

#define RT_HW_HEAP_BEGIN heap.start
#define RT_HW_HEAP_END heap.end

void rt_hw_board_init() {
  int rt_hw_uart_init(void);
  rt_hw_uart_init();

#ifdef RT_USING_HEAP
  /* initialize memory system */
  rt_system_heap_init(RT_HW_HEAP_BEGIN, RT_HW_HEAP_END);
#endif

#ifdef RT_USING_CONSOLE
  /* set console device */
  rt_console_set_device("uart");
#endif /* RT_USING_CONSOLE */

#ifdef RT_USING_COMPONENTS_INIT
  rt_components_board_init();
#endif

#ifdef RT_USING_HEAP
  rt_kprintf("heap: [0x%08x - 0x%08x]\n", (rt_ubase_t) RT_HW_HEAP_BEGIN, (rt_ubase_t) RT_HW_HEAP_END);
#endif
}

int main() {
  extern void __am_cte_init();
  __am_cte_init();
  extern int entry(void);
  entry();
  return 0;
}
