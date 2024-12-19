from turtle import *
import random
import threading
import time

class Block(Turtle):
    def __init__(self, size):
        self.size = size
        Turtle.__init__(self, shape="square", visible=False)
        self.pu()
        self.shapesize(size * 1.5, 1.5, 2)
        self.fillcolor("black")
        self.speed(0)
        self.st()

    def glow(self):
        self.fillcolor("red")

    def unglow(self):
        self.fillcolor("black")

class Shelf(list):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def push(self, block):
        block.setx(self.x + 34 * len(self))
        block.sety(self.y + block.size * 15)
        self.append(block)

    def _rearrange(self):
        for i, block in enumerate(self):
            block.setx(self.x + 34 * i)

    def pop(self, index):
        block = super().pop(index)
        block.glow()
        self._rearrange()
        return block

    def insert(self, index, block):
        super().insert(index, block)
        self._rearrange()
        block.unglow()

def isort(shelf):
    for i in range(1, len(shelf)):
        j = i
        while j > 0 and shelf[j].size < shelf[j - 1].size:
            shelf.insert(j - 1, shelf.pop(j))
            j -= 1

def bsort(shelf):
    for i in range(len(shelf) - 1):
        for j in range(len(shelf) - i - 1):
            if shelf[j].size > shelf[j + 1].size:
                shelf.insert(j, shelf.pop(j + 1))

def msort(shelf):
    def merge(left, right):
        sorted_list = []
        while left and right:
            if left[0].size <= right[0].size:
                sorted_list.append(left.pop(0))
            else:
                sorted_list.append(right.pop(0))
        sorted_list.extend(left + right)
        return sorted_list

    def merge_sort(shelf):
        if len(shelf) <= 1:
            return shelf

        # Highlight the current shelf being divided
        for block in shelf:
            block.glow()
        ontimer(None, 100)  # Reduce delay to 100ms

        mid = len(shelf) // 2
        left = merge_sort(shelf[:mid])
        right = merge_sort(shelf[mid:])

        # Unglow after merging
        for block in shelf:
            block.unglow()

        return merge(left, right)

    # Perform the sort and reinsert sorted elements into the shelf
    sorted_shelf = merge_sort(list(shelf))
    for i, block in enumerate(sorted_shelf):
        shelf.insert(i, shelf.pop(shelf.index(block)))

def threaded_sort(algo, shelf):
    def sort_and_print_time():
        start_time = time.time()
        algo(shelf)
        end_time = time.time()
        print(f"{algo.__name__} took {end_time - start_time:.2f} seconds")
    threading.Thread(target=sort_and_print_time).start()

def start_sorting():
    disable_keys()
    sorting_algos = [isort, bsort, msort]
    for algo, shelf in zip(sorting_algos, shelves):
        threaded_sort(algo, shelf)
    enable_keys()

def create_shelves():
    global shelves
    shelves = []
    algos = ["Insertion Sort", "Bubble Sort", "Merge Sort"]
    positions = [(-500, 0), (-50, 0), (400, 0)]
    for name, (x, y) in zip(algos, positions):
        shelf = Shelf(x, y)
        for size in random.sample(range(1, 11), 10):
            shelf.push(Block(size))
        shelves.append(shelf)
        display_name(name, x, y - 40)

def display_name(name, x, y):
    up()
    goto(x, y)
    write(name, align="center", font=("Courier", 12, "bold"))

def disable_keys():
    onkey(None, "s")
    onkey(None, "q")

def enable_keys():
    onkey(start_sorting, "s")
    onkey(bye, "q")

def main():
    clearscreen()
    print("Results!:",)
    setup(width=1000, height=800)
    hideturtle()
    speed(0)
    create_shelves()
    enable_keys()
    listen()
    return "EVENTLOOP"

if __name__ == "__main__":
    main()
    mainloop()
