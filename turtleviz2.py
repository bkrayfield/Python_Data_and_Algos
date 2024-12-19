from turtle import *
import random

class Block(Turtle):
    def __init__(self, size):
        self.size = size
        Turtle.__init__(self, shape="square", visible=False)
        self.pu()
        self.shapesize(size * 1.5, 1.5, 2)  # square --> rectangle
        self.fillcolor("black")
        self.speed(.5)  # Set turtle speed to maximum
        self.st()

    def glow(self):
        self.fillcolor("red")

    def unglow(self):
        self.fillcolor("black")

    def __repr__(self):
        return f"Block size: {self.size}"


class Shelf(list):
    def __init__(self, y):
        "create a shelf. y is y-position of first block"
        self.y = y
        self.x = -150

    def push(self, d):
        width, _, _ = d.shapesize()
        # align blocks by the bottom edge
        y_offset = width / 2 * 20
        d.sety(self.y + y_offset)
        d.setx(self.x + 34 * len(self))
        self.append(d)

    def _close_gap_from_i(self, i):
        for b in self[i:]:
            xpos, _ = b.pos()
            b.setx(xpos - 34)

    def _open_gap_from_i(self, i):
        for b in self[i:]:
            xpos, _ = b.pos()
            b.setx(xpos + 34)

    def pop(self, key):
        b = list.pop(self, key)
        b.glow()
        b.sety(200)
        self._close_gap_from_i(key)
        return b

    def insert(self, key, b):
        self._open_gap_from_i(key)
        list.insert(self, key, b)
        b.setx(self.x + 34 * key)
        width, _, _ = b.shapesize()
        # align blocks by the bottom edge
        y_offset = width / 2 * 20
        b.sety(self.y + y_offset)
        b.unglow()

def partition(shelf, left, right, pivot_index):
    pivot = shelf[pivot_index]
    shelf.insert(right, shelf.pop(pivot_index))
    store_index = left
    for i in range(left, right): # range is non-inclusive of ending value
        if shelf[i].size < pivot.size:
            shelf.insert(store_index, shelf.pop(i))
            store_index = store_index + 1
    shelf.insert(store_index, shelf.pop(right)) # move pivot to correct position
    return store_index

def isort(shelf):
    length = len(shelf)
    for i in range(1, length):
        hole = i
        while hole > 0 and shelf[i].size < shelf[hole - 1].size:
            hole -= 1
        shelf.insert(hole, shelf.pop(i))
    return


def qsort(shelf, left, right):
    if left < right:
        pivot_index = left
        pivot_new_index = partition(shelf, left, right, pivot_index)
        qsort(shelf, left, pivot_new_index - 1)
        qsort(shelf, pivot_new_index + 1, right)

def ssort(shelf):
    length = len(shelf)
    for j in range(length - 1):
        imin = j
        for i in range(j + 1, length):
            if shelf[i].size < shelf[imin].size:
                imin = i
        if imin != j:
            shelf.insert(j, shelf.pop(imin))


def bsort(shelf):
    length = len(shelf)
    for i in range(length - 1):
        for j in range(length - i - 1):
            # Highlight the two elements being compared
            shelf[j].glow()
            shelf[j + 1].glow()
            ontimer(None, 100)  # Reduce delay to 100ms

            if shelf[j].size > shelf[j + 1].size:
                shelf.insert(j, shelf.pop(j + 1))

            # Remove the highlight after comparison
            shelf[j].unglow()
            shelf[j + 1].unglow()


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


def randomize():
    disable_keys()
    clear()
    target = list(range(10))
    random.shuffle(target)
    for i, t in enumerate(target):
        for j in range(i, len(s)):
            if s[j].size == t + 1:
                s.insert(i, s.pop(j))
    show_text(instructions1)
    show_text(instructions2, line=1)
    enable_keys()


def show_text(text, line=0):
    line = 20 * line
    goto(0, -250 - line)
    write(text, align="center", font=("Courier", 16, "bold"))

def start_qsort():
    disable_keys()
    clear()
    show_text("Quicksort")
    qsort(s, 0, len(s) - 1)
    clear()
    show_text(instructions1)
    show_text(instructions2, line=1)
    enable_keys()

def start_ssort():
    disable_keys()
    clear()
    show_text("Selection Sort")
    ssort(s)
    clear()
    show_text(instructions1)
    show_text(instructions2, line=1)
    enable_keys()


def start_isort():
    disable_keys()
    clear()
    show_text("Insertion Sort")
    isort(s)
    clear()
    show_text(instructions1)
    show_text(instructions2, line=1)
    enable_keys()


def start_bsort():
    disable_keys()
    clear()
    show_text("Bubble Sort")
    bsort(s)
    clear()
    show_text(instructions1)
    show_text(instructions2, line=1)
    enable_keys()


def start_msort():
    disable_keys()
    clear()
    show_text("Merge Sort")
    msort(s)
    clear()
    show_text(instructions1)
    show_text(instructions2, line=1)
    enable_keys()


def init_shelf():
    global s
    s = Shelf(-200)
    vals = (4, 2, 8, 9, 1, 5, 10, 3, 7, 6)
    for i in vals:
        s.push(Block(i))


def disable_keys():
    onkey(None, "s")
    onkey(None, "i")
    onkey(None, "b")
    onkey(None, "q")
    onkey(None, "m")
    onkey(None, "r")


def enable_keys():
    onkey(start_isort, "i")
    onkey(start_ssort, "s")
    onkey(start_bsort, "b")
    onkey(start_qsort, "q")
    onkey(start_msort, "m")
    onkey(randomize, "r")
    onkey(bye, "space")


def main():
    getscreen().clearscreen()
    ht()
    penup()
    init_shelf()
    show_text(instructions1)
    show_text(instructions2, line=1)
    enable_keys()
    listen()
    return "EVENTLOOP"


instructions1 = "press i for insertion sort, s for selection sort, b for bubble sort, q for quicksort, m for merge sort"
instructions2 = "spacebar to quit, r to randomize"

if __name__ == "__main__":
    msg = main()
    mainloop()
