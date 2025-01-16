from types import FunctionType

class LSystem:
    def __init__(self, rules: dict[str, str], constants:list[str], variables:list[str], initState: str, turtleRules: dict[str, FunctionType] = {}) -> None:

        self.rules = rules
        self.turtleRules = turtleRules
        self.constants = constants
        self.variables = variables
        self.initState = initState
    
    def StateGenerator(self):
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
    
    def TurtleGenerator(self):
        """will execute the functions specified in turtleRules on the next recursion of the system"""
        stageGenerator = self.StateGenerator()
        instructions = self.initState
        while True:
            for char in instructions:
                if not(char in self.constants or char in self.variables): raise KeyError(f"'{char}' is not defined in this system")
                if char not in self.turtleRules.keys(): continue
                self.turtleRules[char]()
            instructions = next(stageGenerator)
            yield

    def GetState(self, n:int):
        oldStr = self.initState
        
        for _ in range(n):
            newStr = ""
            for char in oldStr:
                if not(char in self.constants or char in self.variables): raise KeyError(f"'{char}' is not defined in this system")
                if char in self.constants:
                    newStr += char
                    continue
                newStr += self.rules[char]
            oldStr = newStr
        return oldStr
    
    def DrawSystem(self, n:int):
        for char in self.GetState(n):
            if not(char in self.constants or char in self.variables): raise KeyError(f"'{char}' is not defined in this system")
            if char not in self.turtleRules.keys(): continue
            self.turtleRules[char]()