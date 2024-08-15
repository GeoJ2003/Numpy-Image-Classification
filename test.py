import matrixclass as mc

def test1():
    matrix_classes = mc.MC_list('imgs/mnist', 2, ['zero', 'two', 'three', 'four', 'five', 'six', 'eight', 'nine'])
    matrix_classes.classify_dirs('imgs/mnist', 1)

def test2():
    matrix_classes = mc.MC_list('imgs/mnist', 2, ['seven'])
    matrix_classes.classify_dirs('imgs/mnist', 3)

def test3():
    matrix_classes = mc.MC_list('imgs/mnist', 2, ['one'])
    matrix_classes.classify_dirs('imgs/mnist', 3)

def test4():
    matrix_classes = mc.MC_list('imgs/mnist', 2, ['two'])
    matrix_classes.classify_dirs('imgs/mnist', 3)

test1()
# test2()
# test3()

