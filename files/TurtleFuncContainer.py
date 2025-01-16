from LSystem import LSystem
import turtle, time

t = turtle.Turtle()

class TurtleFuncContainer:
    def __init__(self, segmentSize:int, angle:int) -> None:
        self.position_stack = []
        t = turtle.Turtle()
        t.speed(0)
        self.size = segmentSize
        self.angle = angle
        self.constTurtleRules = {"[": self.startBranch, "]": self.endBranch, "-": self.left, "+": self.right}
    def leaf(self):
        t.color("green")
        t.forward(self.size)
        t.color("black")
    
    def left(self):
        t.left(self.angle)

    def right(self):
        t.right(self.angle)

    def fwd(self):
        t.forward(self.size)

    def startBranch(self):
        self.position_stack.append((t.pos(), t.heading()))  

    def endBranch(self):
        if self.position_stack: RestorePos(t, *self.position_stack.pop())

def RestorePos(t:turtle.Turtle, pos:turtle.Vec2D, heading:float):
    t.penup()
    t.goto(pos)
    t.setheading(heading) 
    t.pendown()

def RunSystem(lSys:LSystem, sleepTime:int, toState:int, suppressAnimation:bool = False, origin:tuple[int:int] = (0,0), originAngle:int = 90):
    turtle_generator = lSys.TurtleGenerator()
    if suppressAnimation: turtle.tracer(0)
    for _ in range(toState):  
        t.clear()
        RestorePos(t, origin, originAngle)
        next(turtle_generator)
        turtle.update()
        time.sleep(sleepTime)
    turtle.tracer(1)

def DrawSystemState(lSys:LSystem, state: int, suppressAnimation:bool = False, origin:tuple[int:int] = (0,0), originAngle:int = 90):
    if suppressAnimation: turtle.tracer(0)
    t.clear()
    RestorePos(t, origin, originAngle)
    lSys.DrawSystem(state)
    turtle.update()
    turtle.tracer(1)
