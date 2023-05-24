SECTIONS {
  . = ALIGN(8);

  .myextra : {
    /* section information for initial. */
    . = ALIGN(8);
    __rt_init_start = .;
    KEEP(*(SORT(.rti_fn*)))
    __rt_init_end = .;
    . = ALIGN(8);

    __rt_utest_tc_tab_start = .;
    KEEP(*(UtestTcTab))
    __rt_utest_tc_tab_end = .;
  }
  end = .;
  _end = .;
  _heap_start = ALIGN(0x1000);
}
