#include <klib.h>

void rt_hw_board_init() {
  assert(0);
}

int main() {
  extern void __am_cte_init();
  __am_cte_init();
  extern int entry(void);
  entry();
  return 0;
}
