from GridDrawer import GridDrawer

my_list = [[False, False, True],
           [False, True, False],
           [True, False, False],
           [True] * 3,
           [False, True] * 4]

MyGrid = GridDrawer(4, 30, my_list)
MyGrid.start()
