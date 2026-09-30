# Inf rule
- implication
- hypothesis는 local variable, premise의 gamma는 global variable로 볼 수 있다?

- Implication (-> I)
    - premise: R, P |- Q
    - conclusion: R |- P -> Q
    - intros: assume P, prove Q
- Modus Ponens (-> E)
    - premise: R |- P -> Q, R |- P
    - conclusion: R |- Q
    - apply: modus ponens

- Prove Conjuction (/\ I)
    - premise: R |- P R |- Q
    - conclusion: R |- P /\ Q
    - split: one goal for P, one goal for Q
- Use Conjuction (/\ E1, /\ E2)
    - premise1: R |- P /\ Q
    - conclusion1: R |- P
    - conclusion2: R |- Q

- Prove Disjunction (\/ I1, I2)
    - p1: R |- P
    - p2: R |- Q
    - c: R |- P \/ Q
-  slept

- Quantifiers and Curry-Howard isomorphism
