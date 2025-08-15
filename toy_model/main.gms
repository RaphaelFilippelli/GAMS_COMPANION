$ontext
Toy GAMS model for CI/integration tests.
Maximize net benefit subject to a capacity constraint.
Supports patching via `patch.gdx` and optional equation includes.
$offtext

$if exist patch.gdx $gdxin patch.gdx
$if exist patch.gdx $load CapacityLimit, CostByCatchment, Benefit, ActiveCatchments
$if exist patch.gdx $gdxin

Sets
    i   "catchments" / A, B /;

Alias (i,ip);

Scalar
    CapacityLimit "capacity limit" / 10 /;

Set
    ActiveCatchments(i) / A, B /;

Parameters
    CostByCatchment(i)  "unit cost by catchment" / A 10, B 20 /
    Benefit(i)          "unit benefit by catchment" / A 15, B 18 /;

Variables
    z   "objective (profit)"
    x(i) "activity level in catchment i";

Positive Variable x;

Equations
    obj "objective function"
    cap "capacity constraint";

obj.. z =e= sum(i, Benefit(i)*x(i)) - sum(i, CostByCatchment(i)*x(i));

cap.. sum(i$ActiveCatchments(i), x(i)) =l= CapacityLimit;

$if exist "equation_patches/new_constraint.inc" $include equation_patches/new_constraint.inc

Model toy /all/;
Solve toy using lp maximizing z;

* Export to GDX
execute_unload 'results.gdx', i, ActiveCatchments, CostByCatchment, Benefit, x, z, obj.m, cap.m, CapacityLimit;
