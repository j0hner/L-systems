import time
from LSystem import LSystem
import turtle

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
angle = 90
distance = 10

def fwd(): t.forward(distance)
def left(): t.left(angle)
def right(): t.right(angle)


lSys = LSystem({"F":"F+G", "G":"F-G"}, 
               ["+","-"], 
               ["F", "G"], 
               "F",
               {"F":fwd, "G":fwd, "+":left, "-":right}
               )


# turtle.tracer(0)
lSys.DrawSystem(10)
# turtle.update()

turtle.exitonclick()