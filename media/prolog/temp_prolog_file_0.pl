Male(ali).
Male(ahmed). 
Female(alia).
Female(nadia).
Female(yasmin).

Parent(ahmed, ali).
Parent(ali, alia).
Parent(alia, nadia).
Parent(ahmed, nadia).

Father(X,Y) :- Male(X), Parent(X,Y).
Mother(X,Y) :- Female(X), Parent(X,Y).
Child(X,Y):- Parent(Y,X).
Brother(X, Y) :- Male(X), Parent(Z, X), Parent(Z, Y).
Sister(X, Y) :- Female(X), Parent(Z, X), Parent(Z, Y).
Grandparent(X, Y) :- Parent(X, Z), Parent(Z,Y).