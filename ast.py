#!/usr/bin/python3
#
# Abstract Syntax Tree
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause
#

import tree

class Node ():
	pri = 0

	def gh (o, n):
		if n.pri < o.pri:
			return str (n)

		return "({})".format (str (n))

	def gt (o, n):
		if n.pri <= o.pri:
			return str (n)

		return "({})".format (str (n))

class Name (Node, tree.Unit):
	def __repr__ (o):
		return o.x

class Bool (Node, tree.Unit):
	def __repr__ (o):
		return str (o.x).lower ()

class Int (Node, tree.Unit):
	def __repr__ (o):
		return str (o.x)

# core compound nodes

class Pair (Node, tree.Pair):
	pass

class Func (Pair):
	pri = 2

	def __repr__ (o):
		return "{} → {}".format (o.gh (o.x), o.gt (o.y))

class Apply (Pair):
	pri = 1

	def __repr__ (o):
		return "{} {}".format (o.gt (o.x), o.gh (o.y))

class Case (Pair):
	pri = 12

	def __repr__ (o):
		return "{} | {}".format (o.gh (o.x), o.gt (o.y))

class Prod (Pair):
	pri = 15

	def __repr__ (o):
		return "{}, {}".format (o.gh (o.x), o.gt (o.y))

class Sum (Pair):
	pri = 16

	def __repr__ (o):
		return "{}; {}".format (o.gh (o.x), o.gt (o.y))

# core helper nodes

class Assign (Pair):
	pri = 14

	def __repr__ (o):
		return "{} = {}".format (o.gh (o.x), o.gt (o.y))

class Cond (Node):
	pri = 13

	def __init__ (o, c, t, f):
		o.c = c
		o.t = t
		o.f = f

	def __repr__ (o):
		return "{} ? {} : {}".format (o.gh (o.c), o.gt (o.t), o.gt (o.f))

class Let (Pair):
	def __repr__ (o):
		return "let {} in {}".format (o.x, o.y)

class Letrec (Pair):
	def __repr__ (o):
		return "let rec {} in {}".format (o.x, o.y)

# arithmetic nodes, left associative

class Mul (Pair):
	pri = 3

	def __repr__ (o):
		return "{} × {}".format (o.gt (o.x), o.gh (o.y))

class Div (Pair):
	pri = 3

	def __repr__ (o):
		return "{} ÷ {}".format (o.gt (o.x), o.gh (o.y))

class Add (Pair):
	pri = 4

	def __repr__ (o):
		return "{} + {}".format (o.gt (o.x), o.gh (o.y))

class Sub (Pair):
	pri = 4

	def __repr__ (o):
		return "{} - {}".format (o.gt (o.x), o.gh (o.y))

# relation nodes, left associative

class Lt (Pair):
	pri = 6

	def __repr__ (o):
		return "{} < {}".format (o.gt (o.x), o.gh (o.y))

class Le (Pair):
	pri = 6

	def __repr__ (o):
		return "{} ≤ {}".format (o.gt (o.x), o.gh (o.y))

class Gt (Pair):
	pri = 6

	def __repr__ (o):
		return "{} > {}".format (o.gt (o.x), o.gh (o.y))

class Ge (Pair):
	pri = 6

	def __repr__ (o):
		return "{} ≥ {}".format (o.gt (o.x), o.gh (o.y))

class Eq (Pair):
	pri = 7

	def __repr__ (o):
		return "{} = {}".format (o.gt (o.x), o.gh (o.y))

class Ne (Pair):
	pri = 7

	def __repr__ (o):
		return "{} ≠ {}".format (o.gt (o.x), o.gh (o.y))
