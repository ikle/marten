#!/usr/bin/python3
#
# Generic Expression Optimization Module
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause

import ast

class Unit:
	def __init__ (o, x):
		o.x = x

#	def __repr__ (o):
#		return repr (o.x)

	def __hash__ (o):
		return hash (o.x)

	def __eq__ (a, b):
		return type (a) == type (b) and a.x == b.x

	def __lt__ (a, b):
		if isinstance (b, Pair):
			return True

		if type (a) is not type (b):
			return type (a).__name__ < type (b).__name__

		return a.x < b.x

	def lflatten (o, z = None):
		return o

	def rflatten (o, z = None):
		return o

	def rotate_left (o):
		return o

	def remap (o, M):
		return M.get (o, o)

	def prune (o):
		return o

class Op:
	zero = None	# identity value
	a    = False	# is associative?
	c    = False	# is commutative?
	ld   = set ()	# set of ops this one left-distributive over
	rd   = set ()	# set of ops this one right-distributive over

class Pair (Op):
	def __init__ (o, x, y):
		o.x = x
		o.y = y

#	def __repr__ (o):
#		return '({} {})'.format (repr (o.x), repr (o.y))

	def __hash__ (o):
		return hash (type (o)) + hash (o.x) + hash (o.y)

	def __eq__ (a, b):
		if type (a) is not type (b):
			return False

		return a.x == b.x and a.y == b.y

	def __lt__ (a, b):
		if isinstance (b, Unit):
			return False

		if type (a) is not type (b):
			return type (a).__name__ < type (b).__name__

		return a.y < b.y if a.x == b.x else a.x < b.x

	def lflatten (o, z = None):
		to, tx, ty = type (o), type (o.x), type (o.y)

		if tx is to:
			z = o.x.lflatten (z)
		else:
			x = o.x.lflatten ()
			z = x if z is None else to (z, x)

		return o.y.lflatten (z) if ty is to else to (z, o.y.lflatten ())

	def rflatten (o, z = None):
		to, tx, ty = type (o), type (o.x), type (o.y)

		if ty is to:
			z = o.y.rflatten (z)
		else:
			y = o.y.rflatten ()
			z = y if z is None else to (y, z)

		return o.x.rflatten (z) if tx is to else to (o.x.rflatten (), z)

	def rotate_left (o):
		while o.a and type (o.y) is type (o):
			to = type (o)
			o = to (to (o.x, o.y.x).rotate_left (), o.y.y)

		return o

	def get_args (o, A = []):
		if o.c and type (o.x) is type (o):
			o.x.get_args (A)
		else:
			A.append (o.x)

		if o.c and type (o.y) is type (o):
			o.y.get_args (A)
		else:
			A.append (o.y)

		return A

	def remap (o, M):
		if o in M:
			return M[o]

		return type (o) (o.x.remap (M), o.y.remap (M))

	def sort (o):
		if not o.c:
			return o

		A = o.get_args ([])
		return o.remap ({k: v for (k, v) in zip (A, sorted (A))})

	def prune (o):
		if o.x == o.zero or o.y == o.zero:
			o = o.x if o.y == o.zero else o.y
			return o.prune ()

		while type (o.y) in o.ld:
			to = type (o)
			o  = type (o.y) (to (o.x, o.y.x), to (o.x, o.y.y))

		while type (o.x) in o.rd:
			to = type (o)
			o  = type (o.x) (to (o.x.x, o.y), to (o.x.y, o.y))

		return type (o) (o.x.prune (), o.y.prune ()).rotate_left ().sort ()

class Name (Unit, ast.Name):
	def __init__ (o, x):
		o.x = o.name = x

class Int (Unit, ast.Int):
	def __init__ (o, x):
		o.x = o.v = x

class Add (Pair, ast.Add):
	zero = Int (0)
	a    = True
	c    = True

class Mul (Pair, ast.Mul):
	zero = Int (1)
	a    = True
	c    = True
	ld   = {Add}
	rd   = {Add}

def foldl (fn, zero, seq):
	return foldl (fn, fn (zero, seq[0]), seq[1:]) if seq else zero

def foldr (fn, zero, seq):
	return fn (seq[0], foldr (fn, zero, seq[1:])) if seq else zero

def parse (o):
	if isinstance (o, str):
		return Name (o)

	if isinstance (o, int):
		return Int (o)

	if isinstance (o, list):
		if len (o) == 0:
			return Name ('ε')

		if len (o) == 1:
			return Name (o[0])

		A = [parse (e) for e in o[1:]]

		if len (A) == 1:
			return A[0]

		if o[0] == '+':
			return foldl (Add, A[0], A[1:])

		if o[0] == '×':
			return foldl (Mul, A[0], A[1:])

	raise 'Cannot parse ' + repr (o)

o = [
	'+',
	['×', 1, ['×', 'x', 'z'], 'y'],
	['+', 1],
	['×', 2],
	['×', 'y', 'z', 'b'],
	0,
	['×',
		['+', 'x', 'a'],
		['+', 'x', 'y', 'b']
	]
]

o = parse (o)

print ('parsed          =', o)
print ('left  flatten   =', o.lflatten ())
print ('right flatten   =', o.rflatten ())
print ('left from right =', o.rflatten ().lflatten ())

print ('prune           =', o.prune ())

# print ('pruned =', prune (o))

#	def __iter__ (o):
#		return iter (o.dict)
