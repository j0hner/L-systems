from types import FunctionType
import json
from typing import Any, Generator, Literal, NoReturn, Self
import turtle, time

position_stack = []
stopDrawingFlag = False

class LSystem:
    def __init__(self, rules: dict[str, str], constants:list[str], variables:list[str], initState: str, turtleRules: dict[str, Literal["forward", "backward", "leaf", "left", "right", "start branch","end branch", "none"]], t:turtle.Turtle, angle:int, length:int) -> None:
        self.turtle = t
        t.speed(0)
        self.rules = rules
        constSyntax = {"[": "start branch", "]": "end branch", "-": "left", "+": "right"}
        self.turtleRules = {**turtleRules, **constSyntax}
        self.constants = constants
        self.variables = variables
        self.initState = initState
        self.angle = angle
        self.length = length

    def StateGenerator(self) -> Generator[str, None, NoReturn]:
        """will yield the next recursion of the system"""
        oldStr = self.initState
        
        while True:
            newStr = ""
            yield oldStr
            for char in oldStr:
                if not(char in self.constants or char in self.variables): raise KeyError(f"'{char}' is not defined in this system")
                if char in self.constants:
                    newStr += char
                    continue
                newStr += self.rules[char]
            oldStr = newStr
    
    def TurtleGenerator(self) -> Generator[None, None, NoReturn]:
        """will execute the functions specified in turtleRules on the next recursion of the system"""
        stageGenerator = self.StateGenerator()
        instructions = self.initState
        while True:
            for char in instructions:
                if char not in self.turtleRules.keys(): continue
                getattr(self, f"_{self.turtleRules[char].replace(" ", "_")}", None)()
            instructions = next(stageGenerator)
            yield

    def GetState(self, n:int) -> str:
        oldStr = self.initState
        
        for _ in range(n):
            newStr = ""
            for char in oldStr:
                if not(char in self.constants or char in self.variables): raise KeyError(f"'{char}' is not defined in this system")
                # if char not in self.rules.keys(): continue
                if char in self.constants:
                    newStr += char
                    continue
                newStr += self.rules[char]
            oldStr = newStr
        return oldStr

    def DrawEvolution(self, sleepTime:int, toState:int, suppressAnimation:bool = False, origin:tuple[int:int] = (0,0), originAngle:int = 90):
        turtle_generator = self.TurtleGenerator()
        
        if suppressAnimation: self.turtle.screen.tracer(0)
        
        for _ in range(toState):  
            self.turtle.clear()
            RestorePos(self.turtle, origin, originAngle)
            next(turtle_generator)
            self.turtle.screen.update()
            time.sleep(sleepTime)
        self.turtle.screen.tracer(0)
    
    def DrawState(self, state: int, suppressAnimation:bool = False, origin:tuple[int:int] = (0,0), originAngle:int = 90):
        global stopDrawingFlag
        
        if suppressAnimation: self.turtle.screen.tracer(0)
        
        self.turtle.clear()
        
        RestorePos(self.turtle, origin, originAngle)
        
        for char in self.GetState(state):
            if stopDrawingFlag: stopDrawingFlag=False ; return
            if char not in self.turtleRules.keys(): continue
            getattr(self, f"_{self.turtleRules[char].replace(" ", "_")}", Any)()
        
        self.turtle.screen.update()
        self.turtle.screen.tracer(1)
    
    def __str__(self) -> str:return f" system = LSystem(\n{self.rules},\n{self.constants},\n{self.variables},\n'{self.initState}',\n{"{\n" + {"".join(f"{key}:{func},\n") for key, func in self.turtleRules.items()} + "}"},\n{self.turtle},\n{self.angle},\n{self.length}\n)"
    
    def serialize(self) -> str:
        """Serializes the class attributes (excluding the turtle) to a JSON string."""
        data = {
            "rules": self.rules,
            "constants": self.constants,
            "variables": self.variables,
            "initState": self.initState,
            "turtleRules": self.turtleRules,
            "angle": self.angle,
            "length": self.length,
        }
        return json.dumps(data, indent=4)

    @classmethod
    def deserialize(cls, t:turtle.Turtle, json_str: str) -> Self:
        """Overloaded constructor to create an instance from a serialized string."""
        data = json.loads(json_str)
        return cls(
            rules=data["rules"],
            constants=data["constants"],
            variables=data["variables"],
            initState=data["initState"],
            turtleRules=data["turtleRules"],
            t=t,
            angle=data["angle"],
            length=data["length"]
        )

    #region turtle movement functions

    def _leaf(self):
        self.turtle.color("green")
        self.turtle.forward(self.length)
        self.turtle.color("black")
    
    def _left(self) -> None:
        self.turtle.left(self.angle)

    def _right(self) -> None:
        self.turtle.right(self.angle)

    def _forward(self) -> None:
        self.turtle.forward(self.length)

    def _back(self) -> None:
        self.turtle.back(self.length)

    def _start_branch(self) -> None:
        position_stack.append((self.turtle.pos(), self.turtle.heading()))  

    def _end_branch(self) -> None:
        if position_stack: RestorePos(self.turtle, *position_stack.pop())

    def _none() -> None: return

    #endregion

def can_deserialze(t:turtle.Turtle, json_str:str):
        try:
            LSystem.deserialize(t, json_str)
            return True
        except: return False    

def RestorePos(t:turtle.Turtle|turtle.RawTurtle, pos:turtle.Vec2D, heading:float):
    t.penup()
    t.goto(pos)
    t.setheading(heading) 
    t.pendown()