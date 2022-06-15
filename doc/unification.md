# Logic Unification

Logic unification is an algorithmic process of solving equations between
symbolic expressions. If higher-order variables (variables representing
functions) are allowed in an expression, the process is called higher-order
unification, otherwise first-order unification. 

If a solution is required to make both sides of each equation literally
equal, the process is called syntactic or free unification, otherwise
semantic or equational unification.

A solution of a unification problem is denoted as a substitution, that is, a
mapping assigning a symbolic value to each variable of the problem's
expressions.

For first-order syntactical unification, Martelli and Montanari gave an
algorithm that reports unsolvability or computes a complete and minimal
singleton substitution set containing the so-called most general unifier.

## First-Order Unification Algorithm

Definitions:

* Let L is a sequence of arguments of Ψ.
* Let L[i] is a i-th argument of Ψ.
* Read x/y as substitute y with x.

Unify (Ψ₁, Ψ₂) =

1. If Ψ₂ is a variable then return Unify (Ψ₂, Ψ₁).

2. If Ψ₁ is a constant and Ψ₁ and Ψ₂ are identical then return {} else
   return Error (clash).

3. If Ψ₁ is a variable and Ψ₁ and Ψ₂ are identical then return {} else

   a. if Ψ₁ occurs in Ψ₂, then return Error (cycle)
   b. else return {Ψ₂/Ψ₁}.

4. If the initial predicate symbol in Ψ₁ and Ψ₂ are not same then return
   Error (clash).

5. If len (L₁) ≠ len (L₂) then return Error (clash).

6. Set substitution set RS to {}.

7. For i = 0 to len (L₁) - 1:

   a. if RS ≠ {} then apply RS to L₁[i] and to L₂[i].
   b. S = Unify (L₁[i], L₂[i]);
   c. if S = Error then returns Error;
   d. RS := RS + S.

8. Return RS.
