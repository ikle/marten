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

## Compute types of expressions

Consider the function for calculating the length of a list:

	succ : Int → Int
	let rec len = nil → 0 | cons x xs → succ (len xs)

Let's calculate its type:

	1. len : α → β
	2. α → β = (Nil → β) + (Cons γ (List γ) → (Int → Int) (α → β))
	3. β = Int
	4. α → Int = (Nil → Int) + (Cons γ (List γ) → Int)
	5. α → Int = (Nil + Cons γ (List γ)) → Int
	6. α → Int = List γ → Int
	7. α = List γ
	8. len : List γ → Int

And finally, rename the remaining free variable:

	len : List α → Int

Note that to go from point 4 to point 5, we used the fact that “→” is
distributive over “+”.

### Prune sum of expressions

The prune-sum function algorithm:

1. Create a set S from the set of all child nodes of the sum: flatten sum.

2. Create a set U of all unit nodes from S.

3. For each pair node from S of the form (t, x, y), we create a mapping L
   from (t, x) to set of y.

4. Create a set LP from nodes of the form (t, x, prune-sum (L (t, x))) for
   all keys (t, x) from L.

5. For each pair node from S of the form (t, x, y), we create a mapping R
   from (t, y) to set of x.

6. Create a set RP from nodes of the form (t, prune-sum (L (t, y)), y) for
   all keys (t, y) from R.

7. Create a set P from the union of sets U, LP and LR.

8. Return fold of an ordered list of nodes from P with sum.

Possible optimizations:

* Sets U, and mappings L and R can be created in one pass, bypassing the
  creation of set S.

* You can immediately create a union of sets P from U, LP and RP: we do not
  need these subsets separately.
