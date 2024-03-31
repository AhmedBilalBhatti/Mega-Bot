Male(Ali).
Male(Ahmed). 
Female(Alia).
Female(Nadia).

Parent(Ahmed, Ali).
Parent(Ali, Alia).
Parent(Nadia, Alia).

Child(Ali, Ahmed).
Child(Alia, Ali).
Child(Alia, Nadia).

Father(X,Y) :- Male(X), Parent(X,Z), Child(Z,Y).
Mother(X,Y) :- Female(X), Parent(X,Z), Child(Z,Y).
Grandparent(X, Z) :- Parent(X, Y), Parent(Y, Z).
Sibling(X, Y) :- Parent(Z, X), Parent(Z, Y), X \= Y.