from functools import reduce
import turtle
from LSystem import LSystem
from TurtleFuncContainer import TurtleFuncContainer as TFC, RunSystem

SerpTriTfc = TFC(10, -120)
SerpTriSys = LSystem( 
        {
            "F" : "F-G+F+G-F",
            "G":"GG"
        }, 
        ["+","-"], 
        ["F", "G"], 
        "F",
        {
            "F":SerpTriTfc.fwd,
            "G":SerpTriTfc.fwd, 
            **SerpTriTfc.constTurtleRules
        }
    )

KochCurveTfc = TFC(10, 90)
KochCurveSys = LSystem( 
        {
            "F" : "F-G+F+G-F",
              "G":"GG"}, 
        ["+","-"], 
        ["F", "G"], 
        "F",
        {
            "F":KochCurveTfc.fwd,
            "G":KochCurveTfc.fwd,
            **KochCurveTfc.constTurtleRules
        }
    )

fracTreeTfc = TFC(10, 45)
fracTreeSys = LSystem(
    {
        "1": "11", 
        "0": "1[0]0"
    },  
    ["[", "]"],  
    ["0", "1"],  
    "0",  
    {
        "0": fracTreeTfc.leaf,  
        "1": fracTreeTfc.fwd,
        "[": lambda: reduce(lambda _, f: f(), [fracTreeTfc.startBranch, fracTreeTfc.left], None),
        "]": lambda: reduce(lambda _, f: f(), [fracTreeTfc.endBranch, fracTreeTfc.right], None)
    },
)

dragonTfc = TFC(10, 90)
dragonSys = LSystem(
    {
        "F":"F+G",
        "G":"F-G"
    }, 
    ["+","-"], 
    ["F", "G"], 
    "F",
    {
        "F":dragonTfc.fwd,
        "G":dragonTfc.fwd,
        **dragonTfc.constTurtleRules
    }
)

ArrowheadTfc = TFC(10, 60)
ArrowheadSys = LSystem({"F" : "G-F-G", "G":"F+G+F"}, 
               ["+","-"], 
               ["F", "G"], 
               "F",
               {"F":ArrowheadTfc.fwd, "G":ArrowheadTfc.fwd, "+":ArrowheadTfc.left, "-":ArrowheadTfc.right}
               )

FracPlantTfc = TFC(1, -25)
FracPlantSys = LSystem(
    {
        "X":"F+[[X]-X]-F[-FX]+X",
        "F":"FF"
    },
    ["[","]","+","-"],
    ["F","X"],
    "X",
    {
        "F": FracPlantTfc.fwd,
        **FracPlantTfc.constTurtleRules
    }

)

RunSystem(FracPlantSys, 0, 10, True, originAngle=75)
turtle.exitonclick()