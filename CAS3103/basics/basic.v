(* Inductive nat : Type :=
    | O
    | S (n : nat). *)

Fixpoint plus (n m : nat) : nat :=
    match n with
    | O => m
    | S k => S (plus k m)
    end.

Fixpoint mult (n m : nat) : nat :=
    match n with
    | O => O
    | S k => plus m (mult k m)
    end.

Fixpoint factorial (n : nat) : nat :=
    match n with
    | O => S O
    | S k => mult n (factorial k)
    end.

(* Notation "x + y" := (plus x y) (at level 50, left associativity).
Notation "x * y" := (mult x y) (at level 40, left associativity). *)

Compute 2 * 3.

Compute factorial (S (S (S (S O)))).

Inductive bin : Type :=
    | Z
    | B0 (n : bin)
    | B1 (n : bin).

Theorem plus_0_n : forall n : nat, 0 + n = n.
Proof.
    intros n.
    simpl.
    reflexivity.
Qed.

Theorem plus_n_0 : forall n : nat, n + 0 = n.
Proof.
    intros n.
    induction n as [ |k IH].
    - reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed.

Theorem plus_0_comm : forall n : nat, n + 0 = 0 + n.
Proof.
    intros n.
    simpl.
    (* How do I use my plus_n_0 here? *)
Qed.