#!/usr/bin/python3
#
# Generic Tree Module
#
# Copyright (c) 2020-2022 Alexei A. Smekalkine <ikle@ikle.ru>
#
# SPDX-License-Identifier: BSD-2-Clause

class Tree:
	pass

class Unit (Tree):
	def __init__ (o, x):
		o.x = x

	def __hash__ (o):
		return hash (type (o)) + hash (o.x)

	def __eq__ (a, b):
		return type (a) == type (b) and a.x == b.x

class Pair (Tree):
	def __init__ (o, x, y):
		o.x = x
		o.y = y

	def __hash__ (o):
		return hash (type (o)) + hash (o.x) + hash (o.y)

	def __eq__ (a, b):
		return type (a) is type (b) and a.x == b.x and a.y == b.y
