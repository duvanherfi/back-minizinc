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
        int: n;
        int: paginas;
        
        array[1..n] of int: pagMin;
        array[1..n] of int: pagMax;
        array[1..n] of int: lectores;
        
        array[1..n] of var int: cantidad;
        
        constraint forall(i in 1..n) (cantidad[i] >= 0 \/ cantidad[i] >= pagMin[i]);
        constraint forall(j in 1..n) (cantidad[j] <= pagMax[j]);
        constraint sum(k in 1..n) (cantidad[k]) = paginas;
        solve maximize sum(l in 1..n) (cantidad[l] * lectores[l]);
        
        output [\"datos:\", show(cantidad), \"\nlectores:\", show(sum(l in 1..n) (cantidad[l] * lectores[l]))]
        """
    )
    n = 5;
    paginas = 10;

    pagMin = [5, 4, 2, 2, 1];
    pagMax = [9, 7, 5, 4, 3];
    lectores = [1500, 2000, 1000, 1500, 750];

    instance = Instance(gecode, model)
    instance["n"] = n
    instance["paginas"] = paginas
    instance["pagMin"] = pagMin
    instance["pagMax"] = pagMax
    instance["lectores"] = lectores


    result = instance.solve()
    print(result)
    return {'datos': result["datos"]}
