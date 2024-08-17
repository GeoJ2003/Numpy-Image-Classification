import imageutils as img
import matrixclass as mc

# Matrices 1 and 7 selected
def test1():
    matrix_classes = mc.MC_list('imgs/mnist', 200, ['0', '2', '3', '4', '5', '6', '8', '9'], 0.01, 28, 28)
    matrix_classes.classify_dirs('imgs/mnist', 100)

# Matrices 0 and 8 selected
def test2():
    matrix_classes = mc.MC_list('imgs/mnist', 200, ['1', '2', '3', '4', '5', '6', '7', '9'], 0.01, 28, 28)
    matrix_classes.classify_dirs('imgs/mnist', 100)

# Matrices 2 and 6 selected
def test3():
    matrix_classes = mc.MC_list('imgs/mnist', 200, ['0', '1', '3', '4', '5', '7', '8', '9'], 0.01, 28, 28)
    matrix_classes.classify_dirs('imgs/mnist', 100)

# Matrices 3 and 5 selected
def test4():
    matrix_classes = mc.MC_list('imgs/mnist', 200, ['0', '1', '2', '4', '6', '7', '8', '9'], 0.01, 28, 28)
    matrix_classes.classify_dirs('imgs/mnist', 100)

# test1()
test2()
# test3()
# test4()

# {0: 5923, 1: 6742, 2: 5958, 3: 6131, 4: 5842, 5: 5421, 6: 5918, 7: 6265, 8: 5851, 9: 5949}

