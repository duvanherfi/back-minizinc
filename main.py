from minizinc import Instance, Model, Solver, error


from typing import Union

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Data(BaseModel):
    n:int
    paginas:int
    pag_min:list
    pag_max:list
    lectores:list

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/solve")
def solve(data: Data = Body(embed=True)):
    print("HOla")
    print(data)
    solver = Solver.lookup("gecode")

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
        constraint forall(j in 1..n) (cantidad[j] >= 0 /\ cantidad[j] <= pagMax[j]);
        constraint sum(k in 1..n) (cantidad[k]) = paginas;
        solve maximize sum(l in 1..n) (cantidad[l] * lectores[l]);
        """
    )

    instance = Instance(solver, model)
    instance["n"] = data.n
    instance["paginas"] = data.paginas
    instance["pagMin"] = data.pag_min
    instance["pagMax"] = data.pag_max
    instance["lectores"] = data.lectores

    print(instance["paginas"])
    result = instance.solve()
    print(result)
    return {'cantidad': result["cantidad"], 'lectores': result["objective"]}

