#!/usr/bin/python3
#
# Type Expressions
#
# An implementation of the Hindley-Milner type checking algorithm based
# on the paper "Basic Polymorphic Typechecking" by Cardelli
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause
#

from abc import ABC, abstractmethod

import ast

def gen ():
	for i in range (ord ('α'), ord ('ω')):
		yield chr (i)

class Type (ABC):
	@abstractmethod
	def touch (o, gen):
		pass

	def prune (o):
		"""
		The Prune method is used whenever a type expression has to
		be inspected: it will always return a type expression which
		is either an uninstantiated type variable or a type operator;
		i.e. it will skip instantiated variables, and will actually
		prune them from expressions to remove long chains of
		instantiated variables.

		Returns an uninstantiated node
		"""
		return o

	@abstractmethod
	def __contains__ (o, v):
		"""Checks if type variable v occurs in type"""
		pass

	@abstractmethod
	def fresh (o, env, non_generic):
		"""
		The Fresh method makes a copy of a type expression,
		duplicating the generic variables and sharing the non-generic
		ones.

		Note that a variables in a non-generic list may be
		instantiated to a type term, in which case the variables
		contained in the type term are considered non-generic.
		"""
		pass

	@abstractmethod
	def unify (o, t):
		"""Must be called with o and t pre-pruned"""
		pass

def fresh (o, env, non_generic):
	return o.prune ().fresh (env, non_generic)

def unify (a, b):
	"""Unify the two types a and b"""

	(a, b) = (a.prune (), b.prune ())

	if isinstance (a, Var):
		a.unify (b)
	else:
		b.unify (a)

def emit_mismatch (a, b):
	msg = "Type mismatch: " + str (a) + " ≠ " + str (b)
	raise TypeError (msg)

class Var (Type, ast.Name):
	def __init__ (o):
		o.instance = None
		o.name = None

	def touch (o, gen):
		if o.instance is not None:
			o.instance.touch (gen)
			return

		if o.name is None:
			o.name = next (gen)

	def __repr__ (o):
		return o.name if o.instance is None else repr (o.instance)

	def prune (o):
#		return o if o.instance is None else o.instance.prune ()

		if o.instance is None:
			return o

		# Collapse the list of type instances as an optimisation
		o.instance = o.instance.prune ()
		return o.instance

	def __contains__ (o, v):
		return o == v if o.instance is None else v in o.instance

	def fresh (o, env, non_generic):
		if any (o in t for t in non_generic):
			return o

		if o not in env:
			env[o] = Var ()

		return env[o]

	def unify (o, t):
		if o == t:
			return

		if o in t:
			raise TypeError ("Recursive unification")

		o.instance = t
		o.pri = t.pri

class Name (Type, ast.Name):
	def __init__ (o, name):
		o.name = name

	def touch (o, gen):
		pass

	def __contains__ (o, v):
		return False

	def fresh (o, env, non_generic):
		return o

	def unify (o, t):
		if type (t) is not Name or o.name != t.name:
			emit_mismatch (o, t)

class Func (Type, ast.Func):
	def __init__ (o, domain, codomain):
		o.x    = domain
		o.body = codomain

	def touch (o, gen):
		o.x.touch (gen)
		o.body.touch (gen)
		pass

	def __contains__ (o, v):
		return v in o.x or v in o.body

	def fresh (o, env, ng):
		return Func (fresh (o.x, env, ng), fresh (o.body, env, ng))

	def unify (o, t):
		if type (t) is not Func:
			emit_mismatch (o, t)

		unify (o.x,    t.x)
		unify (o.body, t.body)

class Tuple (Type, ast.Tuple):
	def __init__ (o, *args):
		o.args = args

	def touch (o, gen):
		for v in o.args:
			v.touch (gen)

	def __contains__ (o, v):
		return any (v in t for t in o.args)

	def fresh (o, env, ng):
		return Tuple (*[fresh (t, env, ng) for t in o.args])

	def unify (o, t):
		if type (t) is not Tuple or len (o.args) != len (t.args):
			emit_mismatch (o, t)

		for p, q in zip (o.args, t.args):
			unify (p, q)

class Apply (Type, ast.Apply):
	def __init__ (o, f, arg):
		o.f   = f
		o.arg = arg

	def touch (o, gen):
		o.f.touch (gen)
		o.arg.touch (gen)

	def __contains__ (o, v):
		return v in o.f or v in o.arg

	def fresh (o, env, ng):
		return Apply (fresh (o.f, env, ng), fresh (o.arg, env, ng))

	def unify (o, t):
		if type (t) is not Apply:
			emit_mismatch (o, t)

		unify (o.f,   t.f)
		unify (o.arg, t.arg)
