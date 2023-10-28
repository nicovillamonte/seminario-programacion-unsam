# Pyskell - Documentation

## Table of Contents

...

## Introduction

Pyskell is ...

# Documentation

## Files types

Pyskell was designed to be a compiler for .pll files and a runner for .rpll files.

## REPL

Pyskell has a REPL (Read-Eval-Print-Loop) that can be used to test your code, it can be accessed by running the command `pyskell` in your terminal.

## Builder

Pyskell has a builder that can be used to compile your .pll files into .rpll files, it can be accessed by running the command `pyskell <file>.pll` in your terminal.

## Runner

Pyskell has a runner that can be used to run your .rpll files, it can be accessed by running the command `pyskell <file>.rpll` in your terminal.

## Syntax

### Comments

Comments are used to explain your code, they are ignored by the compiler and the runner.

```
-- This is a comment
```

## Function call

You can call a function by using the function name followed by the arguments.

```
functionName arg1 arg2 arg3
```

For example

```
> add 1 2
3
```

if you call a function with no arguments or less arguments than the function requires, the function will return the type of a function that will wait for the remaining arguments.

```
> add 1
(add 1) :: number -> number
```

## Loop

For now, the only loop is the `for` loop.

```
for i 3
    add i 1
```

This will be transformed to this code by the compiler.

```
add 0
add 1
add 2
```

## Arithmetic Operations

You can do arithmetic operations by using the operators `+`, `-`, `*`, `/`, `%`, `^`.

```
for i 3
    add i+1 i-2
```

It's important to mention that the operations can't have spaces between the operator and the operands.


## Variables (funciones)

You can define a variable (that are functions in pyskell) by using the `=` operator.

```
aVariable = 3
factorial aVariable
```

## Incognits

You can define incognits by using the `?` operator.

```
factorial ?
```

The incognits can have a name to difference each one.

```
factorial ?num
```

When run the code, it will ask for the value of the incognit.

```bash
num: 
```

So you can define the name as it was the text that will be shown when the code is run.

```
sum ?"Input for the first number: " ?num2
```

```bash
Input for the first number: 3
num2: 3
6.0
```

You can define one incognit and use it in several functions.

```
sum ?num ?num
```

This will only ask the user for one incognit and will use it in the whole program.