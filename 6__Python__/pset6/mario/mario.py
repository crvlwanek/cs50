height = 0
options = set(str(i) for i in range(1, 9))
while height not in options:
    height = input("Height: ")
height = int(height)
for i in range(1, height + 1):
    print((" " * (int(height) - i)) +  ("#" * i) + "  " +  ("#" * i))