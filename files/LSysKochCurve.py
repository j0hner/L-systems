import time
from LSystem import LSystem
import turtle

t = turtle.Turtle()
t.speed(0)
angle = 120
distance = 5

def fwd(): t.forward(distance)
def left(): t.left(angle)
def right(): t.right(angle)


lSys = LSystem({"F":"F+F-F-F+F"}, 
               ["+","-"], 
               ["F"], 
               "F",
               {"F":fwd, "+":left, "-":right}
               )

turtle_generator = lSys.TurtleGenerator()
turtle.tracer(0)
for _ in range(10):  
    t.clear()
    t.teleport(0,0)
    next(turtle_generator)
    turtle.update()
    time.sleep(0.5)

turtle.exitonclick()