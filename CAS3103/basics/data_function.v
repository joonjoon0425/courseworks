(* Data type definition *)
Inductive day : Type :=
    | monday
    | tuesday
    | wednesday
    | thursday
    | friday
    | saturday
    | sunday.

(* Function definition *)
Definition next_working_day (d : day) : day :=
    match d with
    | monday => tuesday
    | tuesday => wednesday
    | wednesday => thursday
    | thursday => friday
    | friday => monday
    | saturday => monday
    | sunday => monday
    end.

(* Function computation *)
Compute (next_working_day friday).
Compute (next_working_day (next_working_day saturday)).

(* Record what I expect about the result *)
(* Makes an assertion *)
Example test_working_day: (next_working_day (next_working_day saturday)) = tuesday.
(* Verification *)
Proof.
    simpl.
    reflexivity.
Qed.

(* Boolean *)
Inductive bool : Type :=
    | true
    | false.

Definition negb (b : bool) : bool :=
    match b with
    | true => false
    | false => true
    end.

(* No boolean types are built-in, so the Rocq supports conditonal expressions over any inductively defined type with exactly two clauses it its definition *)
Definition negb' (b: bool) : bool :=
    if b then false
    else true.
(* I guess the first enumeration value is marked as true *)

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

Example test_negb: (negb true) = false.
Proof.
    simpl.
    reflexivity.
Qed.

Example test_andb: (andb true false) = false.
Proof.
    simpl.
    reflexivity.
Qed.

Notation "x && y" := (andb x y).
Notation "x || y" := (orb x y).

Compute true && false.
Compute false || true.

Compute negb' true.

(* checks the type of input *)
Check true.

(* new types from old *)
Inductive rgb : Type :=
    | red
    | green
    | blue.
Inductive color : Type :=
    | black
    | white
    | primary (p : rgb).

Definition monochrome (c : color) : bool :=
    match c with
    | black => true
    | white => true
    | primary _ => false
    end.

Compute monochrome black.