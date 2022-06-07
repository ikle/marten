#!/usr/bin/python3
#
# AST with type inference and type checking
#
# An implementation of the Hindley-Milner type checking algorithm based
# on the paper "Basic Polymorphic Typechecking" by Cardelli
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause
#

import ast, te

from abc import ABC, abstractmethod

class Expr (ABC):
	def get_names (o, env, non_generic):
		pass

	def get_env (o, rec, env, non_generic, new_env, new_non_generic):
		pass

	@abstractmethod
	def get_type (o, env, non_generic):
		pass

# basic types

class Name (ast.Name, Expr):
	def get_names (o, env, ng):
		if not o.name in env:
			env[o.name] = v = te.Var ()
			ng.add (v)

	def get_type (o, env, ng):
		if not o.name in env:
			raise SyntaxError ("Undefined symbol " + o.name)

		return te.fresh (env[o.name], {}, ng)

class Bool (ast.Bool, Expr):
	T = te.Name ("bool")

	def get_type (o, env, ng):
		return o.T

class Int (ast.Int, Expr):
	T = te.Name ("int")

	def get_type (o, env, ng):
		return o.T

# core compound nodes

class Pair (Expr):
	def get_names (o, env, ng):
		o.x.get_names (env, ng)
		o.y.get_names (env, ng)

	def get_env (o, rec, env, ng, new_env, new_ng):
		o.x.get_env (rec, env, ng, new_env, new_ng)
		o.y.get_env (rec, env, ng, new_env, new_ng)

class Func (ast.Func, Pair):
	def get_type (o, env, ng):
		new_env = env.copy ()
		new_ng  = ng.copy ()

		o.x.get_names (new_env, new_ng)

		dom = o.x.get_type (new_env, new_ng)
		cod = o.y.get_type (new_env, new_ng)
		return te.Func (dom, cod)

class Apply (ast.Apply, Pair):
	def get_type (o, env, ng):
		f_type = o.x.get_type (env, ng)
		dom = o.y.get_type (env, ng)
		cod = te.Var ()
		te.unify (f_type, te.Func (dom, cod))
		return cod

class Prod (ast.Prod, Pair):
	def get_type (o, env, ng):
		return te.Prod (o.x.get_type (env, ng), o.y.get_type (env, ng))

class Sum (ast.Sum, Pair):
	def get_type (o, env, ng):
		return te.Sum (o.x.get_type (env, ng), o.y.get_type (env, ng))

# core helper nodes

class Assign (ast.Assign, Pair):
	def get_env (o, rec, env, ng, new_env, new_ng):
		o.x.get_names (new_env, new_ng)

		y_type = o.y.get_type (new_env, new_ng) if rec else \
			 o.y.get_type (env, ng)

		te.unify (o.x.get_type (new_env, new_ng), y_type)

	def get_type (o, env, ng):
		raise SyntaxError ('No context to assign to ' + str (o.x))

class Cond (ast.Cond, Expr):
	def get_type (o, env, ng):
		c_type = o.c.get_type (env, ng)
		te.unify (c_type, Bool.T)
		t_type = o.t.get_type (env, ng)
		f_type = o.f.get_type (env, ng)
		te.unify (t_type, f_type)
		return t_type

class Let (ast.Let, Pair):
	def get_type (o, env, ng):
		new_env = env.copy ()
		new_ng  = ng.copy ()

		o.x.get_env (False, env, ng, new_env, new_ng)

		return o.y.get_type (new_env, ng)

class Letrec (ast.Letrec, Pair):
	def get_type (o, env, ng):
		new_env = env.copy ()
		new_ng  = ng.copy ()

		o.x.get_env (True, env, ng, new_env, new_ng)

		return o.y.get_type (new_env, ng)
