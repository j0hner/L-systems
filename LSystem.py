from types import FunctionType

class LSystem:
    def __init__(self, rules: dict[str, str], consants:list[str], variables:list[str], initState: str, turtleRules: dict[str, FunctionType] = {}) -> None:

        self.rules = rules
        self.turtleRules = turtleRules
        self.consts = consants
        self.vars = variables
        self.initState = initState
    def StateGenerator(self, log:bool = False):
        """will yield the next recursion of the system"""
        oldStr = self.initState
        newStr = ""
        
        while True:
            yield oldStr
            for char in oldStr:
                if char not in self.rules.keys() and not char in self.consts and not char in self.vars: raise KeyError(f"there is no rule, constant or variable defining the behavior of '{char}' in this system")
                if char in self.consts:
                    newStr += char
                    continue
                newStr += self.rules[char]
            oldStr = newStr
            newStr = ""
    
    def TurtleGenerator(self):
        """will execute the functions specified in turtleRules on the next recursion of the system"""
        stageGenerator = self.StateGenerator()
        instructions = self.initState
        while True:
            for instruction in instructions:
                if instruction not in self.turtleRules.keys(): raise KeyError(f"there is no turtle rule defining the behavior of '{instruction}' in this system")
                self.turtleRules[instruction]()
            instructions = next(stageGenerator)
            yield

    def GetState(self, n:int):
        oldStr = self.initState
        newStr = ""
        
        for _ in range(n):
            for char in oldStr:
                if char not in self.rules.keys() and not char in self.consts and not char in self.vars: raise KeyError(f"there is no rule, constant or variable defining the behavior of '{char}' in this system")
                if char in self.consts:
                    newStr += char
                    continue
                newStr += self.rules[char]
            oldStr = newStr
            newStr = ""
        
        return oldStr
    
    def DrawSystem(self, n:int):
        for instruction in self.GetState(n):
            if instruction not in self.turtleRules.keys(): raise KeyError(f"there is no turtle rule defining the behavior of '{instruction}' in this system")
            self.turtleRules[instruction]()