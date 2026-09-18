Inductive natprod : Type :=
    | pair (n1 n2 : nat).

Notation "( x , y )" := (pair x y).

Compute (2, 3).

(* Projection *)
Definition fst (p : natprod) : nat :=
    match p with
    | pair x y => x
    end.

Definition snd (p : natprod) : nat :=
    match p with 
    | pair x y => y
    end.

Compute fst (pair 2 3).

(* destruction을 pair에도 적용 가능. 다만, 기존 inductive 타입과는 다르게 적용 (평소 쓰는 tuple destruction 과 같다)*)
Theorem pair_iden : forall p : natprod, p = (fst p, snd p).
Proof.
    intros p.
    destruct p as [n m].
    simpl. reflexivity.
Qed.

(* list는 recursive하게 정의될 수 있다. *)
Inductive natlist :=
    | nil
    | cons (n : nat) (l : natlist).

Notation "x :: l" := (cons x l) (at level 60, right associativity).
Notation "[ ]" := nil.
Notation "[ x ; .. ; y ]" := (cons x .. (cons y nil) ..).

(* 구현해볼 것들 정리*)
(* 
    repeat, length, append (++), head value with default, tail natlist
    count for given element,
    reverse
    list as multiset or sequence (type alias)
*)

Fixpoint append (l1 l2 : natlist) : natlist :=
    match l1 with
    | nil => l2
    | h :: l3 => h :: (append l3 l2)
    end.

Notation "x ++ y" := (app x y) (at level 60, right associativity).

(* Induction on lists *)
Theorem nil_append : forall l : natlist, append nil l = l.
Proof.
    intros l.
    simpl. reflexivity.
Qed.

Theorem nil_append' : forall l : natlist, append l nil = l.
Proof.
    intros l.
    induction l as [| h t IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed.