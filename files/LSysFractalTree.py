import time
from LSystem import LSystem
import turtle

t = turtle.Turtle()
position_stack = []  
size = 10  
angle = 45  

def RestorePos(pos:turtle.Vec2D, heading:float):
    t.penup()
    t.goto(pos)
    t.setheading(heading) 
    t.pendown()

def draw_leaf():
    t.forward(size)
    

def draw_branch():
    t.forward(size)

def push_position_and_turn_left():
    position_stack.append((t.pos(), t.heading()))  
    t.left(angle)

def pop_position_and_turn_right():
    if position_stack: RestorePos(*position_stack.pop())
    t.right(angle)


tree_sys = LSystem(
    {"1": "11", "0": "1[0]0"},  
    ["[", "]"],  
    ["0", "1"],  
    "0",  
    {
        "0": draw_leaf,  
        "1": draw_branch,  
        "[": push_position_and_turn_left,  
        "]": pop_position_and_turn_right,  
    },
)


turtle.tracer(0)  
t.speed(0)  


state_generator = tree_sys.StateGenerator()
turtle_generator = tree_sys.TurtleGenerator()

for _ in range(10):  
    t.clear()
    RestorePos((0,0), 90)
    next(turtle_generator)  
    turtle.update()  
    time.sleep(0.5)

turtle.exitonclick()
