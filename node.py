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
	@abstractmethod
	def get_type (o, env, non_generic):
		pass

# basic types

class Name (ast.Name, Expr):
	def get_type (o, env, non_generic):
		if not o.name in env:
			raise SyntaxError ("Undefined symbol " + o.name)

		return te.fresh (env[o.name], {}, non_generic)

class Bool (ast.Bool, Expr):
	T = te.Name ("bool")

	def get_type (o, env, non_generic):
		return o.T

class Int (ast.Int, Expr):
	T = te.Name ("int")

	def get_type (o, env, non_generic):
		return o.T

class Prod (ast.Prod, Expr):
	def get_type (o, env, ng):
		return te.Prod (o.x.get_type (env, ng), o.y.get_type (env, ng))

# core expressions

class Cond (ast.Cond, Expr):
	def get_type (o, env, non_generic):
		c_type = o.c.get_type (env, non_generic)
		te.unify (c_type, Bool.T)
		t_type = o.t.get_type (env, non_generic)
		f_type = o.f.get_type (env, non_generic)
		te.unify (t_type, f_type)
		return t_type

class Func (ast.Func, Expr):
	def get_type (o, env, non_generic):
		dom = te.Var ()

		new_env = {o.x.name: dom, **env}
		new_non_generic = non_generic | {dom}

		cod = o.y.get_type (new_env, new_non_generic)
		return te.Func (dom, cod)

class Apply (ast.Apply, Expr):
	def get_type (o, env, non_generic):
		f_type = o.x.get_type  (env, non_generic)
		dom = o.y.get_type (env, non_generic)
		cod = te.Var ()
		te.unify (f_type, te.Func (dom, cod))
		return cod

class Let (ast.Let, Expr):
	def get_type (o, env, non_generic):
		defn_type = o.defn.get_type (env, non_generic)

		new_env = {o.name: defn_type, **env}

		return o.body.get_type (new_env, non_generic)

class Letrec (ast.Letrec, Expr):
	def get_type (o, env, non_generic):
		new_type = te.Var ()

		new_env = {o.name: new_type, **env}
		new_non_generic = non_generic | {new_type}

		defn_type = o.defn.get_type (new_env, new_non_generic)
		te.unify (new_type, defn_type)

		return o.body.get_type (new_env, non_generic)
