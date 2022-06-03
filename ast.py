#!/usr/bin/python3
#
# Abstract Syntax Tree
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause
#

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

class Name (Node):
	def __init__ (o, name):
		o.name = name

	def __repr__ (o):
		return o.name

class Bool (Node):
	def __init__ (o, v):
		o.v = v

	def __repr__ (o):
		return str (o.v).lower ()

class Int (Node):
	def __init__ (o, v):
		o.v = v

	def __repr__ (o):
		return str (o.v)

class Tuple (Node):
	def __init__ (o, *args):
		o.args = args

	def __repr__ (o):
		return '(' + ', '.join (map (str, o.args)) + ')'

class Cond (Node):
	pri = 13

	def __init__ (o, c, t, f):
		o.c = c
		o.t = t
		o.f = f

	def __repr__ (o):
		return "{} ? {} : {}".format (o.gh (o.c), o.gt (o.t), o.gt (o.f))

class Func (Node):
	pri = 1

	def __init__ (o, x, body):
		o.x    = x
		o.body = body

	def __repr__ (o):
		return "{} → {}".format (o.gh (o.x), o.gt (o.body))

class Apply (Node):
	pri = 1

	def __init__ (o, f, arg):
		o.f   = f
		o.arg = arg

	def __repr__ (o):
		return "{} {}".format (o.gt (o.f), o.gh (o.arg))

class Let (Node):
	pri = 14

	def __init__ (o, name, defn, body):
		o.name = name.name
		o.defn = defn
		o.body = body

	def __repr__ (o):
		return "let {} = {} in {}".format (o.name, o.defn, o.body)

class Letrec (Node):
	pri = 14

	def __init__ (o, name, defn, body):
		o.name = name.name
		o.defn = defn
		o.body = body

	def __repr__ (o):
		return "let rec {} = {} in {}".format (o.name, o.defn, o.body)
