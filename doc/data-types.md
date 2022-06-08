# Reflections on the definition of data types

In this note, we will look at what types are, try to operate with expressions
on them, and consider ways to define them.

## Equivalence of ADT and GADT

Consider the classic definition of an abstract list type in the form of ADT:

	∀ α . List α = Nil + Cons α (List α)

Let's try to define the parts of the sum:

	∀ α, β + γ = List α . Nil = β, Cons α (List α) = γ

There is not much to look at in the definition of Nil, but Cons is noticeably
more interesting. Let's derive the type of Cons:

	∀ α, β + γ = List α        . Nil = β, Cons α (List α) = γ
	∀ α, β + γ = ε, ε = List α . Nil = β, Cons α ε        = γ
	∀ α, β + γ = ε, ε = List α . Nil = β, Cons α          = ε → γ
	∀ α, β + γ = ε, ε = List α . Nil = β, Cons            = α → ε → γ
	∀ α, β + γ = List α        . Nil = β, Cons            = α → List α → γ

Specify the upper bound for Nil and Cons:

	∀ α, β + γ = List α . Nil < List α, Cons < α → List α → List α

... next will be rewritten

This output shows that Nil and Cons are types (expressions over types are
types).

Nil and Cons are dualistic: they define both a type (a subtype of List α) and
a data constructor function at the same time. Let's remove the naming
ambiguity and write constructors with a lowercase letter:

	nil  : List α
	cons : α → List α → List α

We got the GADT form from the ADT form.

To summarize: the ADT and GADT forms are equivalent and can be derived one from
the another automatically. If the GADT form can be represented as an ADT form.
The ADT form, as we can see, is always representable as a GADT form.
