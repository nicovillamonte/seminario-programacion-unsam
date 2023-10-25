from pyskell_types import PyskellFunction

# Función factorial (Number -> Number)
def factorial_pyskell(n: int) -> int:
    n = int(n)
    return n * factorial_pyskell(n-1) if n > 1 else 1
factorial = PyskellFunction('factorial', factorial_pyskell, type=(int, int))

# Función doble (Number -> Number)
def doble_pyskell(n):
    n = float(n)
    return n * 2
doble = PyskellFunction('doble', doble_pyskell, type=(float, float))

# Función suma (Number -> Number -> Number)
def suma_pyskell(n: float) -> PyskellFunction:
    def inner_suma_pyskell (m: float) -> float:
        return float(n) + float(m)
    return PyskellFunction(func=inner_suma_pyskell, type=(float,float))
suma = PyskellFunction('suma', suma_pyskell, type=(float, PyskellFunction(type=(float,float))))

# Función upperCase (String -> String)
def upperCase_pyskell(s):
    s = str(s)
    return s.upper()
upperCase = PyskellFunction('upperCase', upperCase_pyskell, type=(str, str))

# Función lowerCase (String -> String)
def lowerCase_pyskell(s):
    s = str(s)
    return s.lower()
lowerCase = PyskellFunction('lowerCase', lowerCase_pyskell, type=(str, str))

# Función length (String -> Number)
def length_pyskell(s):
    s = str(s)
    return len(s)
length = PyskellFunction('length', length_pyskell, type=(str, int))

def sumOf_pyskell(arr):
    if len(arr) == 0:
        return 0
    else:
        return int(arr[0]) + sumOf_pyskell(arr[1:])
sumOf = PyskellFunction('sumOf', sumOf_pyskell, type=(list, int))

def isStrEq_pyskell(s):
    def inner_isStrEq_pyskell(x):
        return s == x
    return PyskellFunction(func=inner_isStrEq_pyskell, type=(str, bool))
isStrEq = PyskellFunction('isStrEq', isStrEq_pyskell, type=(str, PyskellFunction(type=(str, bool))))

def helloWorld_pyskell():
    return "Hello World!"
helloWorld = PyskellFunction('helloWorld', helloWorld_pyskell, type=(str))

def fibonacci_pyskell(n):
    n = int(n)
    return fibonacci_pyskell(n-1) + fibonacci_pyskell(n-2) if n > 1 else n
fibonacci = PyskellFunction('fibonacci', fibonacci_pyskell, type=(int, int))

pyskell_exported_functions = [factorial, doble, suma, upperCase, lowerCase, length, sumOf, isStrEq, helloWorld, fibonacci]