import turtle
from LSystem import LSystem
t = turtle.Turtle()

# KochCurveSys = LSystem( 
#         {
#             "F" : "F-G+F+G-F",
#               "G":"GG"}, 
#         ["+","-"], 
#         ["F", "G"], 
#         "F",
#         {
            
#         }
#     )

# fracTreeSys = LSystem(
#     {
#         "1": "11", 
#         "0": "1[0]0"
#     },  
#     ["[", "]"],  
#     ["0", "1"],  
#     "0",  
#     {
        
#     },
# )

dragonSys = LSystem(
    {
        "F":"F+G",
        "G":"F-G"
    }, 
    ["+","-"], 
    ["F", "G"], 
    "F",
    {
        "F":"forward",
        "G":"forward",
    },
    t,
    90,
    10,
)

# ArrowheadSys = LSystem(
#     {
#         "F" : "G-F-G", "G":"F+G+F"
#     }, 
#     ["+","-"], 
#     ["F", "G"], 
#     "F",
#     {
        
#     }
# )

foo = FracPlantSys.serialize()
print(foo)
turtle.exitonclick()