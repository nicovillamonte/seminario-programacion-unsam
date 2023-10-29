from pyskell_types import PyskellFunction, number

# Función print (String -> String)
def log_pyskell(s):
    s = str(s)
    return s
log = PyskellFunction('log', log_pyskell, type=(str, str))

# Función factorial (Number -> Number)
def factorial_pyskell(n: number) -> number:
    n = number(n)
    return n * factorial_pyskell(n-1) if n > 1 else 1
factorial = PyskellFunction('factorial', factorial_pyskell, type=(number, number))

# Función doble (Number -> Number)
def doble_pyskell(n):
    n = number(n)
    return number(n * 2)
doble = PyskellFunction('doble', doble_pyskell, type=(number, number))

# Función suma (Number -> Number -> Number)
def suma_pyskell(n: number) -> PyskellFunction:
    def inner_suma_pyskell (m: number) -> number:
        return number(n) + number(m)
    return PyskellFunction(func=inner_suma_pyskell, type=(number,number))
suma = PyskellFunction('suma', suma_pyskell, type=(number, PyskellFunction(type=(number,number))))

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
    return number(len(s))
length = PyskellFunction('length', length_pyskell, type=(str, number))

def sumOf_pyskell(arr):
    if len(arr) == 0:
        return 0
    else:
        return number(number(arr[0]) + number(sumOf_pyskell(arr[1:])))
sumOf = PyskellFunction('sumOf', sumOf_pyskell, type=(list, number))

def isStrEq_pyskell(s):
    def inner_isStrEq_pyskell(x):
        return s == x
    return PyskellFunction(func=inner_isStrEq_pyskell, type=(str, bool))
isStrEq = PyskellFunction('isStrEq', isStrEq_pyskell, type=(str, PyskellFunction(type=(str, bool))))

def helloWorld_pyskell():
    return "Hello World!"
helloWorld = PyskellFunction('helloWorld', helloWorld_pyskell, type=(str))

def fibonacci_pyskell(n):
    n = number(n)
    return number(fibonacci_pyskell(n-1) + fibonacci_pyskell(n-2) if n > 1 else n)
fibonacci = PyskellFunction('fibonacci', fibonacci_pyskell, type=(number, number))

pyskell_exported_functions = [log, factorial, doble, suma, upperCase, lowerCase, length, sumOf, isStrEq, helloWorld, fibonacci]