Sets
    i   "catchments" / A, B /;

Scalar
    CapacityLimit "capacity limit" / 10 /;

Parameters
    CostByCatchment(i)  "unit cost by catchment" / A 10, B 20 /
    Benefit(i)          "unit benefit by catchment" / A 15, B 18 /;

Variables
    z   "objective (profit)"
    x(i) "activity level in catchment i";

Positive Variable x;

Equations
    obj "objective function"
    limitA
    cap "capacity constraint";

obj.. z =e= sum(i, Benefit(i)*x(i)) - sum(i, CostByCatchment(i)*x(i));

cap.. sum(i, x(i)) =l= CapacityLimit;

limitA.. x('A') =l= 3;

Model toy /all/;