#!/usr/bin/python3
#
# Generic Expression Optimization Module
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause

import tree

class Expr:
	def __lt__ (a, b):
		return str (a) < str (b)

	def rotate_left (o):
		return o

	def remap (o, M):
		return M.get (o, o)

	def prune (o):
		return o

class Unit (Expr, tree.Unit):
	pass

class Op (Expr):
	zero = None	# identity value
	a    = False	# is associative?
	c    = False	# is commutative?
	ld   = set ()	# set of ops this one left-distributive over
	rd   = set ()	# set of ops this one right-distributive over

class Pair (Op, tree.Pair):
	def rotate_left (o):
		while o.a and type (o.y) is type (o):
			to = type (o)
			o = to (to (o.x, o.y.x).rotate_left (), o.y.y)

		return o

	def get_args (o):
		if o.c and type (o.x) is type (o):
			A = o.x.get_args ()
		else:
			A = [o.x]

		if o.c and type (o.y) is type (o):
			A.extend (o.y.get_args ())
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

		A = o.get_args ()
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
