from LSystem import LSystem
import turtle, time

class TurtleFuncContainer:
    def __init__(self, t:turtle.Turtle|turtle.RawTurtle, segmentSize:int, angle:int) -> None:
        self.position_stack = []
        self.t = t
        t.speed(0)
        self.size = segmentSize
        self.angle = angle
        self.constTurtleRules = {"[": self.startBranch, "]": self.endBranch, "-": self.left, "+": self.right}
    
    def leaf(self):
        self.t.color("green")
        self.t.forward(self.size)
        self.t.color("black")
    
    def left(self):
        self.t.left(self.angle)

    def right(self):
        self.t.right(self.angle)

    def fwd(self):
        self.t.forward(self.size)

    def back(self):
        self.t.back(self.size)

    def startBranch(self):
        self.position_stack.append((self.t.pos(), self.t.heading()))  

    def endBranch(self):
        if self.position_stack: RestorePos(self.t, *self.position_stack.pop())

    def __repr__(self) -> str:
        return f"tfc = TurtleFuncContainer(t,{self.size},{self.angle})"

def RestorePos(t:turtle.Turtle|turtle.RawTurtle, pos:turtle.Vec2D, heading:float):
    t.penup()
    t.goto(pos)
    t.setheading(heading) 
    t.pendown()

def RunSystem(lSys:LSystem,t:turtle.Turtle|turtle.RawTurtle, sleepTime:int, toState:int, suppressAnimation:bool = False, origin:tuple[int:int] = (0,0), originAngle:int = 90):
    turtle_generator = lSys.TurtleGenerator()
    if suppressAnimation: turtle.tracer(0)
    for _ in range(toState):  
        t.clear()
        RestorePos(t, origin, originAngle)
        next(turtle_generator)
        turtle.update()
        time.sleep(sleepTime)
    turtle.tracer(1)

def DrawSystemState(lSys:LSystem, t:turtle.Turtle|turtle.RawTurtle, state: int, suppressAnimation:bool = False, origin:tuple[int:int] = (0,0), originAngle:int = 90):
    if suppressAnimation: t.screen.tracer(0)
    t.clear()
    RestorePos(t, origin, originAngle)
    lSys.DrawSystem(state)
    t.screen.update()
    t.screen.tracer(1)

