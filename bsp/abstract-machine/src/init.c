#include <klib.h>

void rt_hw_board_init() {
  assert(0);
}

int main() {
  extern int entry(void);
  entry();
  return 0;
}
