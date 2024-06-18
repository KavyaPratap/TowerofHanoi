import turtle
import tkinter as tk
from tkinter import simpledialog, ttk

# Initialize the pegs with rings
def initialize_pegs(num_rings):
    pegs = {1: list(range(num_rings, 0, -1)), 2: [], 3: []}
    return pegs

# Draw a single peg
def draw_peg(x):
    tower.penup()
    tower.goto(x, -295)
    tower.pendown()
    tower.pensize(5)
    tower.color("white")
    tower.forward(peg_height)

# Draw a single ring
def draw_ring(x, y, width, height, color):
    tower.penup()
    tower.goto(x - width / 2, y)
    tower.pendown()
    tower.color("black", color)
    tower.begin_fill()
    for _ in range(2):
        tower.forward(width)
        tower.left(90)
        tower.forward(height)
        tower.left(90)
    tower.end_fill()
    tower.penup()

# Draw all pegs
def draw_pillars():
    for x in peg_positions.values():
        draw_peg(x)

# Draw the entire scene including pegs and rings
def draw_scene(pegs, step):
    tower.clear()
    draw_pillars()
    for peg, rings in pegs.items():
        x = peg_positions[peg]
        y = -250 + len(rings) * 20
        for ring in rings:
            color = ring_colors[ring % len(ring_colors)]
            draw_ring(x, y, 20 + ring * 20, 20, color)
            y += 20
    draw_step(step)

# Draw the step counter
def draw_step(step):
    tower.penup()
    tower.goto(0, -395)
    tower.pendown()
    tower.color("white")
    tower.write(f"Step: {step}", align="center", font=("Arial", 16, "normal"))

# Colors for the rings
ring_colors = [
    "orange",
    "red",
    "green",
    "blue",
    "purple",
    "pink",
    "cyan",
    "yellow",
    "brown",
    "gray"
]

# Move a ring from source peg to destination peg
def move_ring(pegs, source, destination, step):
    if not pegs[source]:
        print("Source peg is empty. Try again.")
    elif not pegs[destination] or pegs[source][-1] < pegs[destination][-1]:
        ring = pegs[source].pop()
        pegs[destination].append(ring)
        step += 1
        draw_scene(pegs, step)
        print(f"Moved ring {ring} from {source} to {destination}")
        move_list.insert("", "end", text=f"Move {step}", values=(ring, source, destination))
    else:
        print("Invalid move. The ring cannot be placed on top of a smaller ring.")

# Recursive Tower of Hanoi solution
def tower_of_hanoi(n, source, auxiliary, target, step):
    draw_scene(pegs, step)
    if n == 1:
        source = simpledialog.askinteger("Input", "Enter source peg (1, 2, 3):")
        destination = simpledialog.askinteger("Input", "Enter destination peg (1, 2, 3):")
        if source in pegs and destination in pegs:
            move_ring(pegs, source, destination, step)
        else:
            print("Invalid source or destination.")
        return
    tower_of_hanoi(n - 1, source, target, auxiliary, step)
    source = simpledialog.askinteger("Input", "Enter source peg (1, 2, 3):")
    destination = simpledialog.askinteger("Input", "Enter destination peg (1, 2, 3):")
    if source in pegs and destination in pegs:
        move_ring(pegs, source, destination, step)
    else:
        print("Invalid source or destination.")
    tower_of_hanoi(n - 1, auxiliary, source, destination, step)

# Initialize the main screen and turtle graphics
screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
tower = turtle.Turtle()
tower.hideturtle()
tower.speed(0)

peg_positions = {1: -300, 2: 0, 3: 300}
peg_height = 300

num_rings = simpledialog.askinteger("Input", "Enter the number of rings:")
pegs = initialize_pegs(num_rings)

screen.bgcolor("black")

step = 0

draw_scene(pegs, step)

# Create Tkinter root window
root = tk.Tk()
root.title("Tower of Hanoi Moves")

# Create a treeview to display moves
move_list = ttk.Treeview(root, columns=("Ring", "From Peg", "To Peg"), show="headings")
move_list.heading("Ring", text="Ring")
move_list.heading("From Peg", text="From Peg")
move_list.heading("To Peg", text="To Peg")
move_list.pack()

# Run the Tower of Hanoi algorithm
while len(pegs[3]) != num_rings:
    tower_of_hanoi(1, 1, 3, 2, step)

print("Congratulations! You have solved the Tower of Hanoi puzzle.")
input("")

# Start Tkinter event loop
root.mainloop()
