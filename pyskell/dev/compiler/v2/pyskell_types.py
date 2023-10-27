from typing import Any

##############################################################
# Pyskell Types - number
##############################################################
class number:
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            self.value = float(value)
        else:
            self.value = value

    @classmethod
    def type_name(cls):
        return "Number"

    def __repr__(self):
        return f"{self.value}"

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)
    
    def __add__(self, other):
        if isinstance(other, number):
            return number(self.value + other.value)
        elif isinstance(other, (int, float)):
            return number(self.value + other)
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'number' and {type(other).__name__}")
        
    def __sub__(self, other):
        if isinstance(other, number):
            return number(self.value - other.value)
        elif isinstance(other, (int, float)):
            return number(self.value - other)
        else:
            raise TypeError(f"unsupported operand type(s) for -: 'number' and {type(other).__name__}")
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return number(self.value * other)
        elif isinstance(other, number):
            return number(self.value * other.value)
        else:
            raise TypeError("Unsupported operand type")

    def __truediv__(self, other):
        if isinstance(other, number):
            if other.value == 0:
                raise ZeroDivisionError("division by zero")
            return number(self.value / other.value)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return number(self.value / other)
        else:
            raise TypeError(f"unsupported operand type(s) for /: 'number' and {type(other).__name__}")
    
    def __floordiv__(self, other):
        if isinstance(other, number):
            if other.value == 0:
                raise ZeroDivisionError("division by zero")
            return number(self.value // other.value)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return number(self.value // other)
        else:
            raise TypeError(f"unsupported operand type(s) for //: 'number' and {type(other).__name__}")
    
    def __mod__(self, other):
        if isinstance(other, number):
            if other.value == 0:
                raise ZeroDivisionError("division by zero")
            return number(self.value % other.value)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return number(self.value % other)
        else:
            raise TypeError(f"unsupported operand type(s) for %: 'number' and {type(other).__name__}")
    
    def __pow__(self, other):
        if isinstance(other, number):
            return number(self.value ** other.value)
        elif isinstance(other, (int, float)):
            return number(self.value ** other)
        else:
            raise TypeError(f"unsupported operand type(s) for **: 'number' and {type(other).__name__}")
    
    # Métodos mágicos para operaciones de comparación
    def __eq__(self, other):
        if isinstance(other, number):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == other
        else:
            return NotImplemented
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if isinstance(other, number):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        else:
            return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, number):
            return self.value <= other.value
        elif isinstance(other, (int, float)):
            return self.value <= other
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, number):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > other
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, number):
            return self.value >= other.value
        elif isinstance(other, (int, float)):
            return self.value >= other
        else:
            return NotImplemented

##############################################################
# Pyskell Types - PyskellFunction
##############################################################
class PyskellFunction:
    def __init__(self, name="_", func=lambda x: x, type=(None, None)):
        self.name = name
        self.func = func
        self.type = type
        self.command = ""

    def __call__(self, *args: Any) -> Any:
        # transform result into type of second argument if it is not the same type
        value_returned = self.func(args[0]) if len(args) > 0 else self.func()
        if not type(value_returned) is self.type[1] and not isinstance(value_returned, PyskellFunction):
            value_returned = self.type[1](value_returned)
        return value_returned
    
    # def __call__(self, *args: Any) -> Any:
    #     value_returned = self.func(args[0]) if len(args) > 0 else self.func()
    #     print("VALUE RETURNED IN CALL:", value_returned, type(value_returned), self.type[1])
    #     if not isinstance(value_returned, self.type[1]):
    #         value_returned = self.type[1](value_returned)
    #         print("VALUE CONVERTED IN CALL:", value_returned, type(value_returned))
    #     return value_returned
    
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