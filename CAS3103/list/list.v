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

Definition not (b : bool) : bool :=
    match b with
    | true => false
    | false => true
    end.

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

Fixpoint repeat (n count : nat) : natlist :=
    match count with
    | O => nil
    | S k => n :: (repeat n k)
    end.

Compute repeat 4 3.

Fixpoint length (li : natlist) : nat :=
    match li with
    | nil => 0
    | h :: t => 1 + length t
    end.

Compute length [4 ; 2 ; 2 ; 1; 3].

Fixpoint append (l1 l2 : natlist) : natlist :=
    match l1 with
    | nil => l2
    | h :: t => h :: (append t l2)
    end.

Compute append [1; 2; 3] [2; 3; 4].

Notation "a ++ b" := (append a b).

Compute [2; 3; 4] ++ [1; 0; 3].

Definition tail (l : natlist) : natlist :=
    match l with
    | nil => nil
    | h :: t => t
end.

(* Same type, different intuition: A bag is a multiset *)
Definition bag := natlist.
Fixpoint count (v : nat) (b : bag) : nat :=
    match b with
    | nil => 0
    | h :: t =>
        if h =? v then S (count v t)
                  else count v t
    end.

Fixpoint sum (b : bag) : nat :=
    match b with
    | nil => 0
    | h :: t => h + (sum t)
    end.


Compute sum [1; 2; 3].

Compute count 3 [1; 2; 3; 4; 3; 2; 1].

Theorem count_twolist : forall (l1 l2 : natlist) (v : nat), count v l1 + count v l2 = count v (l1 ++ l2).
Proof.
    intros l1 l2 v.
    induction l1 as [|h t IH].
    - simpl. reflexivity.
    - simpl.
      destruct (h =? v) eqn: E.
      + simpl. rewrite IH. reflexivity.
      + rewrite IH. reflexivity. 
Qed.

Fixpoint rev (l : natlist) : natlist :=
    match l with
    | nil => nil
    | h :: t => (rev t) ++ [h]
    end.

Compute rev [1; 2; 3].

Fixpoint nonzeros (l : natlist) : natlist :=
    match l with
    | nil => nil
    | 0 :: t => nonzeros t
    | h :: t => h :: nonzeros t
    end.

Fixpoint oddmembers (l : natlist) : natlist :=
    match l with
    | nil => nil
    | h :: t => if odd h then h :: (oddmembers t) else oddmembers t
    end.

(* These are some theorem proof exercises *)
Theorem nil_app : forall l : natlist, nil ++ l = l.
Proof.
    simpl. reflexivity.
Qed.

Theorem nil_app' : forall l : natlist, l ++ nil = l.
Proof.
    intros l.
    induction l as [| k t IH].
    - reflexivity.
    - Print append.
      simpl. rewrite IH. reflexivity.
Qed.

(* Induction은 append가 실제로 무엇에 대해 fixpoint를 적용하는지를 보면 된다. 이 경우에는 append l1 l2에서 l1에 적용하면 된다. 귀납법 적용! *)
Theorem app_assoc : forall l1 l2 l3 : natlist, (l1 ++ l2) ++ l3 = l1 ++ (l2 ++ l3).
Proof.
    intros l1 l2 l3.
    induction l1 as [|h t IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.  
Qed.

Theorem app_length : forall l1 l2 : natlist, (length l1) + (length l2) = length (l1 ++ l2).
Proof.
    intros l1 l2.
    induction l1 as [|h t IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed.

Theorem plus_S_1 : forall (n : nat), S n = n + 1.
Proof.
    Print Nat.add.
    intros n.
    induction n as [|k IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed. 

Theorem rev_length : forall l1 : natlist, length l1 = length (rev l1).
Proof.
    intros l1.
    induction l1 as [|h t IH].
    - simpl. reflexivity.
    - simpl. rewrite <- app_length.
      simpl. rewrite IH. rewrite plus_S_1. reflexivity. 
Qed.

Theorem rev_dist : forall (l1 l2 : natlist), rev (l1 ++ l2) = rev l2 ++ rev l1.
Proof.
    intros l1 l2.
    induction l1 as [|h t IH].
    - simpl. rewrite nil_app'. reflexivity.
    - simpl. rewrite IH. rewrite app_assoc. reflexivity.
Qed.

Theorem rev_involutive : forall l : natlist, rev (rev l) = l.
Proof.
    intros l.
    induction l as [|h t IH].
    - simpl. reflexivity.
    - simpl. rewrite rev_dist. rewrite IH. simpl. reflexivity.
Qed.