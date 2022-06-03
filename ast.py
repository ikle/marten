#!/usr/bin/python3
#
# Abstract Syntax Tree
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause
#

class Name ():
	def __init__ (o, name):
		o.name = name

	def __repr__ (o):
		return o.name

class Bool ():
	def __init__ (o, v):
		o.v = v

	def __repr__ (o):
		return str (o.v).lower ()

class Int ():
	def __init__ (o, v):
		o.v = v

	def __repr__ (o):
		return str (o.v)

class Tuple ():
	def __init__ (o, *args):
		o.args = args

	def __repr__ (o):
		return '(' + ', '.join (map (str, o.args)) + ')'

class Cond ():
	def __init__ (o, c, t, f):
		o.c = c
		o.t = t
		o.f = f

	def __repr__ (o):
		return "(if {} then {} else {})".format (o.c, o.t, o.f)

class Func ():
	def __init__ (o, x, body):
		o.x    = x
		o.body = body

	def __repr__ (o):
		return "(fun {} {})".format (o.x, o.body)

class Apply ():
	def __init__ (o, f, arg):
		o.f   = f
		o.arg = arg

	def __repr__ (o):
		return "({} {})".format (o.f, o.arg)

class Let ():
	def __init__ (o, name, defn, body):
		o.name = name.name
		o.defn = defn
		o.body = body

	def __repr__ (o):
		return "(let {} = {} in {})".format (o.name, o.defn, o.body)

class Letrec ():
	def __init__ (o, name, defn, body):
		o.name = name.name
		o.defn = defn
		o.body = body

	def __repr__ (o):
		return "(letrec {} = {} in {})".format (o.name, o.defn, o.body)
