The Game of Arithmetic Hide and Seek
------------------------------------

Implementation of Angel's algorithm (solution of the problem).
See more here: http://dmishin.blogspot.com/2015/05/the-game-of-arithmetic-hide-and-seek.html

The program enumerates all expressions, buit of operations +-/*^ integer numbers and variable *k*, substituting current move number to *k*.

Resulting sequence is guaranteed to intersect with any sequence, generted by a fixed formula.

Requirments
===========

Python 3, pyparsing.

To validate and evaluare expressions, **pyparsing** is used.
The code is in Python 3, bus should work in Python 2 with minor modifications (prints etc).

Implementation
==============

Simply enumerate all strings of characters "0123456789+-*/^()k", and choose those that are valid expressions.