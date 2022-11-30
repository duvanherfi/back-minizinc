from minizinc import Instance, Model, Solver, error
from fastapi import Body, FastAPI
from pydantic import BaseModel
from ast import literal_eval
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/solve")
def solve(body=Body()):
    print("HOla")
    print(body)
    if isinstance(body, bytes):
        body = literal_eval(body.decode('utf-8'))
    
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

    instance["n"] = body["n"]
    instance["paginas"] = body["paginas"]
    instance["pagMin"] = body["pag_min"]
    instance["pagMax"] = body["pag_max"]
    instance["lectores"] = body["lectores"]

    print(instance["paginas"])
    result = instance.solve()
    print(result)
    return {'cantidad': result["cantidad"], 'lectores': result["objective"]}

