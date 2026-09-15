(* Constructor with multiple parameters *)
Inductive bit : Type :=
    | B1
    | B0.

Inductive bit4 : Type :=
    | bits (b0 b1 b2 b3 : bit).

Check (bits B0 B1 B1 B0).