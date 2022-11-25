from fastapi import FastAPI
from minizinc import Instance, Model, Solver

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/solve")
def solve():
    print("HOla")
    gecode = Solver.lookup("gecode")

    model = Model()
    model.add_string(
        """
        include "all_different.mzn";
        set of int: A;
        set of int: B;
        array[A] of var B: arr;
        var set of B: X;
        var set of B: Y;

        constraint all_different(arr);
        constraint forall (i in index_set(arr)) ( arr[i] in X );
        constraint forall (i in index_set(arr)) ( (arr[i] mod 2 = 0) <-> arr[i] in Y );
        """
    )
    instance = Instance(gecode, model)
    instance["A"] = range(3, 8)  # MiniZinc: 3..8
    instance["B"] = {4, 3, 2, 1, 0}  # MiniZinc: {4, 3, 2, 1, 0}

    result = instance.solve()
    return {'resultado': result["arr"]}
