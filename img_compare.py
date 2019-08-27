from skimage import io
import sys
first = io.imread(sys.argv[1])
second = io.imread(sys.argv[2])
if(len(first) != len(second) or len(first[0]) != len(second[0])):
    print("Not the same size.")
    sys.exit()
for i in range(len(first)):
    for j in range(len(first[i])):
        print(first[i][j])
        if(first[i][j] != second[i][j]):
            print("Not the same image.")
            sys.exit()
print("Same picture!")
