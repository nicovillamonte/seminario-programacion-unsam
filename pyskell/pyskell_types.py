from typing import Any

class PyskellFunction:
    def __init__(self, name="_", func=lambda x: x, type=(None, None)):
        self.name = name
        self.func = func
        self.type = type
        self.command = ""

    def __call__(self, *args: Any) -> Any:
        return self.func(args[0]) if len(args) > 0 else self.func()
    
    def calleable(self):
        return callable(self.func)
    
    def set_command(self, command):
        self.command = command
    
    def destruct_type(self, _obj):
        self_type, inner_type = _obj.type
        
        if (type(_obj.type[0]) is type and type(_obj.type[1]) is PyskellFunction):
            return f"{self_type.__name__} -> {self.destruct_type(inner_type)}"
        else:
            return _obj.type[0].__name__ + " -> " + _obj.type[1].__name__
    
    def __str__(self):
        return f"{self.name if self.name != '_' else f'({self.command})'} :: {self.destruct_type(self)}"

    def __repr__(self):
        return f"<PyskellFunction: {self.name}>"