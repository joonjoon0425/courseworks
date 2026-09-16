(* induction <VAR> as <PATTERN WITH NAMES> *)
(* induction n as [|k IH]. *)
(* O은 변수가 안에 없어서 새로 받을 이유가 없다. Hypothesis도 안 받음 *)

Theorem add_0_r : forall n : nat, n + 0 = n.
Proof.
    intros n.
    induction n as [|n' IHn'].
    - simpl. reflexivity.
    - simpl. rewrite -> IHn'. reflexivity.
Qed.
(* simpl.을 사용하면 정의를 이용한다 *)
Print Nat.add.

Theorem mult_0_r: forall n : nat, n * 0 = 0.
Proof.
    intros n.
    induction n as [|k IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed.
Print Nat.mul.

(* reduction이 일어나는 변수에 대해 귀납법을 적용한다 *)
Theorem add_n_Sm: forall n m : nat, S (n + m) = n + S m.
Proof.
    intros n m.
    induction n as [|k IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed.

(* 화살표로 어느 방향으로 rewrite할지 정할 수 있는 듯? *)
Theorem add_comm: forall n m : nat, n + m = m + n.
Proof.
    intros n m.
    induction n as [|k IH].
    - simpl. rewrite add_0_r. reflexivity.
    - simpl. rewrite IH. rewrite plus_n_Sm. reflexivity.
Qed. 

Theorem add_assoc: forall n m p : nat, n + (m + p) = (n + m) + p.
Proof.
    intros n m p.
    induction n as [|k IH].
    - simpl. reflexivity.
    - simpl. rewrite IH. reflexivity.
Qed. 

(* Generalize the theorem *)
Fixpoint go (acc n : nat) : nat :=
    match n with
    | O => acc
    | S k => go (S acc) k
    end.


(* rewrite applies to outermost one, basically *)
Theorem plus_rearrange : forall n m p q : nat, (n + m) + (p + q) = (m + n) + (p + q).
Proof.
    intros n m p q.
    (* rewrite add_comm -> switches the parantheses *)
    (* how do we apply rewrite to our desired part? *)
    (* new tatic: assert *)
    assert (H: n + m = m + n).
    {
        rewrite add_comm.
        reflexivity.
    }
    rewrite H.
    reflexivity.

(* Theorem plus_rearrange' : forall n m p q : nat, (n + m) + p + q = (m + n) + p + q.
Proof.
    intros n m p q.
    replace (n + m) with (m + n).
    - rewrite add_comm.
    - reflexivity.
Qed. *)

Theorem add_swap : forall n m p : nat, n + (m + p) = m + (n + p).
Proof.
    intros n m p.
    rewrite add_assoc.
    rewrite add_assoc.
    rewrite (add_comm n m). (* can apply lemma to specific variables *)
    reflexivity.
Qed.

(* study the proofs with hand for midterm exam *)