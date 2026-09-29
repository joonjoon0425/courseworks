(* apply: use hypothesis directly *)
(* apply with: fill in universial variables explicitly*)

Theorem mp : forall P Q : Prop, (P -> Q) -> P -> Q.
Proof.
    intros P Q HPQ HP.
    apply HPQ.
    exact HP.
Qed.

(* rewrite는 goal을 바꾸고 apply는 goal을 sub-problem으로 바꿔주는 것이라고 한다. *)

Theorem trans_eq : forall (X : Type) (n m o : X),
    n = m -> m = o -> n = o.
Proof.
    intros X n m o eq1 eq2.
    rewrite eq1. rewrite eq2. reflexivity.
Qed.

Example a_eq_c : forall a b c : nat,
    a = b -> b = c -> a = c.
Proof.
    intros a b c H1 H2.
    rewrite H1.
    rewrite H2.
    reflexivity.
Qed.

Example a_eq_c' : forall a b c : nat,
    a = b -> b = c -> a = c.
    intros a b c H1 H2.
    apply trans_eq with (m := b).
    - apply H1.
    - apply H2.
Qed.

(* injection uses the constructor *)
(* C n = C m -> n = m *)

Theorem injection_nat : forall (n m : nat),
    S n = S m -> n = m.
Proof.
    intros n m H.
    injection H as H1.
    exact H1.
Qed.

(* If the hypothesis has different Constructors, the hypothesis is false and the result is always true *)
Theorem discriminate_ex : forall (n : nat),
    0 = S n -> 2 + 2 = 5.
Proof.
    intros n H.
    discriminate H. (* 0 != S n; assumption is absurd *)
Qed.

Theorem add_assoc: forall n m p : nat, n + (m + p) = (n + m) + p.
Proof.
    intros n m p.
    induction n as [|k IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed. 

(* rewrite in H, symmetry in H --> 전부 H에 적용 *)
Definition square (n : nat) := n * n.

Theorem distributive : forall (n m p : nat), (n + m) * p = n * p + m * p.
Proof.
    intros n m p.
    induction n as [| k IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. apply add_assoc.
Qed.

Theorem assoc_mult : forall (n m p : nat), n * (m * p) = (n * m) * p.
Proof.
    intros n m p.
    induction n as [| k IH].
    - simpl. reflexivity.
    - simpl. rewrite distributive. rewrite IH. reflexivity.
Qed.

Theorem mult_0_r: forall n : nat, n * 0 = 0.
Proof.
    intros n.
    induction n as [|k IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed.

Theorem comm_mult : forall (n m : nat), n * m = m * n.
Proof.
    intros n m.
    induction n as [| k IH].
    - simpl. rewrite mult_0_r. reflexivity.
    - simpl. 

Theorem square_mult : forall n m , square (n * m) = square n * square m.
Proof.
    intros n m.
    unfold square.
    rewrite assoc_mult.
    rewrite assoc_mult.
    
Qed.

(* f_equal: reverse of injection. changes the goal. *)
Theorem eq_implies_succ_equal : forall (n m : nat), n = m -> S n = S m.
Proof.
    intros n m H.
    f_equal.
    apply H.
Qed.

(*
apply L in H 는 일반 apply와는 다르게 forward reasoning을 한다 
즉, L이 X->Y고 H가 X면 H를 Y로 교체한다
*)