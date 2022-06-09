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

class Type (ABC):
	def touch (o, i = 0):
		return i

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

	def __contains__ (o, v):
		"""Checks if type variable v occurs in type"""
		return False

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

class Var (ast.Name, Type):
	def __init__ (o):
		super ().__init__ (None)
		o.instance = None

	def touch (o, i = 0):
		if o.instance is not None:
			return o.instance.touch (i)

		if o.name is None:
			o.name = chr (ord ('α') + i)
			return i + 1

		return i

	def __repr__ (o):
		return o.name if o.instance is None else repr (o.instance)

	def prune (o):
		return o if o.instance is None else o.instance.prune ()

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

class Name (ast.Name, Type):
	def fresh (o, env, non_generic):
		return o

	def unify (o, t):
		if type (t) is not Name or o.name != t.name:
			t.touch (o.touch ())
			raise TypeError ("Type mismatch: {} ≠ {}".format (o, t))

class Pair (Type):
	def touch (o, i = 0):
		return o.y.touch (o.x.touch (i))

	def __contains__ (o, v):
		return v in o.x or v in o.y

	def fresh (o, env, ng):
		return type (o) (fresh (o.x, env, ng), fresh (o.y, env, ng))

	def unify (o, t):
		if type (t) is not type (o):
			t.touch (o.touch ())
			raise TypeError ("Type mismatch: {} ≠ {}".format (o, t))

		unify (o.x, t.x)
		unify (o.y, t.y)

class Func (ast.Func, Pair):
	pass

class Apply (ast.Apply, Pair):
	pass

class Prod (ast.Prod, Pair):
	pass

class Sum (ast.Sum, Pair):
	def __init__ (o, x, y):
		super ().__init__ (x, y)
		o.ref = None

	def touch (o, i = 0):
		if o.ref is not None:
			return o.ref.touch (i)

		return o.y.touch (o.x.touch (i))

	def prune (o):
		return o if o.ref is None else o.ref.prune ()

	def __contains__ (o, v):
		return v in o.x or v in o.y if o.ref is None else v in o.ref

	def unify (o, t):
		try:
			unify (o.x, t)
			o.instance = o.x
		except TypeError:
			unify (o.y, t)
			o.instance = o.y
