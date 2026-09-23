Inductive bool : Type :=
    | true
    | false.

Fixpoint nateq (a b : nat) : bool :=
    match a, b with
    | O, O => true
    | O, _ => false
    | _, O => false
    | S m, S n => nateq m n
    end.

Fixpoint le (a b : nat) : bool :=
    match a, b with
    | O, O => false
    | O, _ => true
    | _, O => false
    | S n, S m => le n m
    end.

Fixpoint leq (a b : nat) : bool :=
    match a, b with
    | O, O => true
    | O, _ => true
    | _, O => false
    | S n, S m => leq n m
    end.

Definition not (b : bool) : bool :=
    match b with
    | true => false
    | false => true
    end.

Definition ge (a b : nat) : bool :=
    not (leq a b).

Definition geq (a b : nat) : bool :=
    not (le a b).



Fixpoint even (a : nat) : bool :=
    match a with
    | O => true
    | S O => false
    | S (S k) => even k
    end.

Definition odd (a : nat) : bool :=
    not (even a).

Compute even 2.
Compute even 3.

Notation "a =? b" := (nateq a b) (at level 10, left associativity).
Notation "a <? b" := (le a b) (at level 10, left associativity).
Notation "a >? b" := (ge a b) (at level 10, left associativity).

(* create a list that gets other types *)
Inductive list (T: Type) : Type :=
    | nil
    | cons (t : T) (l : list T).
(* implicit version *)
Arguments nil {T}.
Arguments cons {T}.

Notation "x :: l" := (cons x l) (at level 60, right associativity).
Notation "[ ]" := nil.
Notation "[ x ; .. ; y ]" := (cons x .. (cons y nil) ..).

Check nil.
Check cons.

Fixpoint length {T: Type} (l : list T) : nat :=
    match l with
    | nil => 0
    | cons h t => S (length t)
    end.

Compute length [1;2;3].


Fixpoint append {T: Type} (l1 l2 : list T) : list T :=
    match l1 with
    | nil => l2
    | h :: t => h :: (append t l2)
    end.

Notation "a ++ b" := (append a b).

Fixpoint rev {X: Type} (l : list X) : list X :=
    match l with
    | nil => nil
    | h :: t => (rev t) ++ [h]
    end.

(* higher order functions *)
Definition doit3times {T: Type} (f : T -> T) (n : T) : T :=
    f ( f (f n)).

Fixpoint filter {T: Type} (test : T -> bool) (l : list T) : list T :=
    match l with
    | nil => nil
    | cons h t => if test h then h :: (filter test t)
    else filter test t
    end.

Compute (filter (fun n => 5 <? n) [3; 4; 7; 8; 1; 3]).

Fixpoint map {X Y: Type} (f : X -> Y) (l : list X) : list Y := 
    match l with
    | nil => nil
    | cons h t => f h :: map f t
    end.

Compute (map (fun n => n * n) [1; 2; 3; 4]).

Theorem map_app : forall (X Y : Type) (f : X -> Y) (l1 l2 : list X), map f (l1 ++ l2) = map f l1 ++ map f l2.
Proof.
    intros.
    induction l1 as [|h t IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed.  

Theorem map_rev : forall (X Y : Type) (f : X -> Y) (l : list X), map f (rev l) = rev (map f l).
Proof.
    intros.
    induction l as [|h t IH].
    - simpl. reflexivity.
    - simpl. rewrite map_app. rewrite IH. simpl. reflexivity.
Qed.

(* 두 값을 주어진 함수를 통해 하나로 만들어 가며 리스트를 줄여 나간다. *)
Fixpoint fold {X Y : Type} (f : X -> Y -> Y) (l : list X) (b : Y) : Y :=
    match l with
    | nil => b
    | cons h t => f h (fold f t b)
    end.

Compute (fold Nat.add [1; 2; 3; 4] 0).
Compute (fold Nat.mul [1; 2; 3; 4; 5] 1).

Definition fold_length {X : Type} (l : list X) : nat :=
    fold (fun _ acc => S acc) l 0.

Theorem fold_length_correct : forall (X : Type) (l : list X), fold_length l = length l.
Proof.
    intros X l.
    induction l as [|h t IH].
    - simpl. reflexivity.
    - simpl. rewrite <- IH. reflexivity.
Qed.
(* 사실 모든 함수는 단 하나의 인자만 받는 걸로 볼 수 있다. *)
(* nat -> nat -> nat 는 nat -> nat함수와 nat -> nat 함수로 볼 수 있다 *)
(* partial application이 가능한 이유 *)
Definition plus3 := Nat.add 3.

Compute plus3 4.