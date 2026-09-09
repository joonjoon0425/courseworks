(* Inductive nat : Type :=
    | O : nat
    | S : nat -> nat. *)

Fixpoint plus (n m : nat) : nat :=
    match n with
    | O => m
    | S k => S (plus k m)
    end.

Compute plus 1 2.