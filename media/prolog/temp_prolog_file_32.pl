% Bank account facts
bankAccount(laila, current, 500.0).
bankAccount(stefan, savings, 50.0).
bankAccount(paul, current, 45.0).
bankAccount(tasha, savings, 5000.0).

% Interest facts
interest(twoPercent, current, 500.0).
interest(onePercent, current, 0.0).
interest(tenPercent, savings, 5000.0).
interest(fivePercent, savings, 0.0).

% Savings rate rule
savingsRate(Name, Type, Amount) :-
    bankAccount(Name, Type, Balance),
    interest(InterestRate, Type, Base),
    Balance >= Base,
    Amount is Balance * (InterestRate / 100.0).