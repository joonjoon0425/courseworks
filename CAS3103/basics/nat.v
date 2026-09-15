Module NatPlayground.
Inductive nat : Type :=
    | O
    | S (n : nat).
End NatPlayground.
(* The standard library uses same definition, I guess. *)
Check S (S (S O)).

(* Boolean *)
Inductive bool : Type :=
    | true
    | false.

Definition negb (b : bool) : bool :=
    match b with
    | true => false
    | false => true
    end.

Definition andb (b_1: bool) (b_2: bool) : bool :=
    match b_1 with
    | true => b_2
    | false => false
    end.

Definition orb (b_1: bool) (b_2: bool) : bool :=
    match b_1 with
    | true => true
    | false => b_2
    end.

Fixpoint even (n : nat) : bool :=
    match n with
    | O => true
    | S O => false
    | S (S k) => even k
    end.

Compute even 2.
Compute even 3.

Definition odd(n : nat) : bool :=
    negb (even n).

Compute odd 3.
Compute odd 1233.

Fixpoint plus (n : nat) (m : nat) : nat :=
    match n with
    | O => m
    | S k => S (plus k m)
    end.

Fixpoint mult (n : nat) (m : nat) : nat :=
    match n with
    | O => O
    | S k => plus m (mult k m)
    end.

Fixpoint exp (base power : nat) : nat :=
    match power with
    | O => S O
    | S k => mult base (exp base k)
    end.

Fixpoint factorial (n : nat) : nat :=
    match n with
    | O => S O
    | S k => mult n (factorial k)
    end.

Fixpoint eq (n m : nat) : bool :=
    match n, m with
    | O, O => true
    | O, _ => false
    | _, O => false
    | S n', S m' => eq n' m'
    end.
Fixpoint le (n m : nat) : bool :=
    match n, m with
    | O, O => false
    | O, _ => true
    | _, O => false
    | S n', S m' => le n' m'
    end.
Fixpoint ge (n m : nat) : bool :=
    match n, m with
    | O, O => false
    | O, _ => false
    | _, O => true
    | S n', S m' => ge n' m'
    end.
Definition leq (n m : nat) : bool :=
    negb (ge n m).
Definition geq (n m : nat) : bool :=
    negb (le n m).

Example test_factorial: (factorial 5) = 120.
Proof.
    simpl.
    reflexivity.
Qed.

Notation "x + y" := (plus x y) (at level 50, left associativity).
Notation "x * y" := (mult x y) (at level 40, left associativity).
Notation "x ^ y" := (exp x y) (at level 30, right associativity).

Compute 4 * 8.
Compute 3 ^ 3.
Compute factorial 5.
Compute eq 4 3.
Compute eq 0 0.
Compute eq 3 5.
Compute eq 4 4.

Compute le 3 4.
Compute le 4 4.
Compute ge 1 5.
Compute ge 5 2.
Compute le 3 4.
Compute leq 4 4.