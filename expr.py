#!/usr/bin/python3
#
# Generic Expression Optimization Module
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause

import tree

class Node:
	pass

class Unit (Node, tree.Unit):
	def __lt__ (a, b):
		if type (b) is not type (a):
			return type (a).__name__ < type (b).__name__

		return a.x < b.x

	def remap (o, M):
		return M.get (o, o)

	def prune (o):
		return o

class Pair (Node, tree.Pair):
	lu   = None	# left unit (identity) value
	ru   = None	# right unit (identity) value
	a    = False	# is associative?
	c    = False	# is commutative?
	ld   = set ()	# set of ops this one left-distributive over
	rd   = set ()	# set of ops this one right-distributive over

	def __lt__ (a, b):
		if type (b) is not type (a):
			return type (a).__name__ < type (b).__name__

		return a.y < b.y if a.x == b.x else a.x < b.x

	def flatten (o):
		while o.a and type (o.y) is type (o):
			to = type (o)
			o = to (to (o.x, o.y.x).flatten (), o.y.y)

		return o

	def get_args (o):
		X = o.x.get_args () if o.c and type (o.x) is type (o) else [o.x]
		Y = o.y.get_args () if o.c and type (o.y) is type (o) else [o.y]

		return X + Y

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
		if o.x == o.lu:
			return o.y.prune ()

		if o.y == o.ru:
			return o.x.prune ()

		while type (o.y) in o.ld:
			to = type (o)
			o  = type (o.y) (to (o.x, o.y.x), to (o.x, o.y.y))

		while type (o.x) in o.rd:
			to = type (o)
			o  = type (o.x) (to (o.x.x, o.y), to (o.x.y, o.y))

		return type (o) (o.x.prune (), o.y.prune ()).flatten ().sort ()
