#!/usr/bin/python3
#
# Generic Expression Optimization Module
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause

import ast, expr

class Name (expr.Unit, ast.Name):
	pass

class Int (expr.Unit, ast.Int):
	pass

class Add (expr.Pair, ast.Add):
	lu   = Int (0)
	ru   = Int (0)
	a    = True
	c    = True

class Mul (expr.Pair, ast.Mul):
	lu   = Int (1)
	ru   = Int (1)
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

print ('parsed =', o)
print ('pruned =', o.prune ())
