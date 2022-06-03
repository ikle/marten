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

class Type (ABC):
	@abstractmethod
	def show (o, gen, guard):
		pass

	def __str__ (o):
		def gen ():
			for i in range (ord ('α'), ord ('ω')):
				yield chr (i)

		return o.show (gen ())

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

	a.prune ().unify (b.prune ())

class Var (Type):
	def __init__ (o):
		o.instance = None
		o.name = None

	def show (o, gen):
		if o.instance is not None:
			return o.instance.show (gen)

		if o.name is None:
			o.name = next (gen)

		return o.name

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

def guard (o, gen, name = None):
	o = o.prune ()

	if isinstance (o, Var) or len (o.types) < 2 or o.name == name:
		return o.show (gen)

	return '(' + o.show (gen) + ')'

class Op (Type):
	def __init__ (o, name, types):
		o.name  = name
		o.types = types

	def show (o, gen):
		if len (o.types) == 0:
			return o.name

		def f (o):
			return guard (o, gen)

		return "{} {}".format (o.name, ' '.join (map (f, o.types)))

	def __contains__ (o, v):
		return any (v in t for t in o.types)

	def fresh (o, env, non_generic):
		kind  = type (o)
		types = [fresh (t, env, non_generic) for t in o.types]

		return Op (o.name, types) if kind is Op else kind (*types)

	def unify (o, t):
		if isinstance (t, Var):
			t.unify (o)
			return

		if o.name != t.name or len (o.types) != len (t.types):
			msg = "Type mismatch: " + str (o) + " ≠ " + str (t)
			raise TypeError (msg)

		for p, q in zip (o.types, t.types):
			unify (p, q)

class Name (Op):
	def __init__ (o, name):
		super ().__init__ (name, [])

	def show (o, gen):
		return o.name

	def fresh (o, env, non_generic):
		return o

class Func (Op):
	def __init__ (o, domain, codomain):
		super ().__init__ ("→", [domain, codomain])

	def show (o, gen):
		dom = guard (o.types[0], gen)
		cod = guard (o.types[1], gen, o.name)
		return "{} → {}".format (dom, cod)

class Tuple (Op):
	def __init__ (o, *args):
		super ().__init__ ("×", args)

	def show (o, gen):
		def f (o):
			return guard (o, gen)

		return ", ".join (map (f, o.types))
