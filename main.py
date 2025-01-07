from fastapi import FastAPI
from models import CNCMachine

import joblib

import numpy as np

estimator_toolwear = joblib.load('saved_models/toolwear_RandomForestClassifier.pkl')

app = FastAPI()

def predict_tool_wear(estimator, request):
    
    X1_ACTUALPOSITION=request["X1_ACTUALPOSITION"]
    X1_ACTUALVELOCITY=request["X1_ACTUALVELOCITY"]
    X1_ACTUALACCELERATION=request["X1_ACTUALACCELERATION"]
    X1_COMMANDPOSITION=request["X1_COMMANDPOSITION"]
    X1_COMMANDVELOCITY=request["X1_COMMANDVELOCITY"]
    X1_COMMANDACCELERATION=request["X1_COMMANDACCELERATION"]
    X1_CURRENTFEEDBACK=request["X1_CURRENTFEEDBACK"]
    X1_DCBUSVOLTAGE=request["X1_DCBUSVOLTAGE"]
    X1_OUTPUTCURRENT=request["X1_OUTPUTCURRENT"]
    X1_OUTPUTVOLTAGE=request["X1_OUTPUTVOLTAGE"]
    X1_OUTPUTPOWER=request["X1_OUTPUTPOWER"]
    Y1_ACTUALPOSITION=request["Y1_ACTUALPOSITION"]
    Y1_ACTUALVELOCITY=request["Y1_ACTUALVELOCITY"]
    Y1_ACTUALACCELERATION=request["Y1_ACTUALACCELERATION"]
    Y1_COMMANDPOSITION=request["Y1_COMMANDPOSITION"]
    Y1_COMMANDVELOCITY=request["Y1_COMMANDVELOCITY"]
    Y1_COMMANDACCELERATION=request["Y1_COMMANDACCELERATION"]
    Y1_CURRENTFEEDBACK=request["Y1_CURRENTFEEDBACK"]
    Y1_DCBUSVOLTAGE=request["Y1_DCBUSVOLTAGE"]
    Y1_OUTPUTCURRENT=request["Y1_OUTPUTCURRENT"]
    Y1_OUTPUTVOLTAGE=request["Y1_OUTPUTVOLTAGE"]
    Y1_OUTPUTPOWER=request["Y1_OUTPUTPOWER"]
    Z1_ACTUALPOSITION=request["Z1_ACTUALPOSITION"]
    Z1_ACTUALVELOCITY=request["Z1_ACTUALVELOCITY"]
    Z1_ACTUALACCELERATION=request["Z1_ACTUALACCELERATION"]
    Z1_COMMANDPOSITION=request["Z1_COMMANDPOSITION"]
    Z1_COMMANDVELOCITY=request["Z1_COMMANDVELOCITY"]
    Z1_COMMANDACCELERATION=request["Z1_COMMANDACCELERATION"]
    Z1_CURRENTFEEDBACK=request["Z1_CURRENTFEEDBACK"]
    Z1_DCBUSVOLTAGE=request["Z1_DCBUSVOLTAGE"]
    Z1_OUTPUTCURRENT=request["Z1_OUTPUTCURRENT"]
    Z1_OUTPUTVOLTAGE=request["Z1_OUTPUTVOLTAGE"]
    S1_ACTUALPOSITION=request["S1_ACTUALPOSITION"]
    S1_ACTUALVELOCITY=request["S1_ACTUALVELOCITY"]
    S1_ACTUALACCELERATION=request["S1_ACTUALACCELERATION"]
    S1_COMMANDPOSITION=request["S1_COMMANDPOSITION"]
    S1_COMMANDVELOCITY=request["S1_COMMANDVELOCITY"]
    S1_COMMANDACCELERATION=request["S1_COMMANDACCELERATION"]
    S1_CURRENTFEEDBACK=request["S1_CURRENTFEEDBACK"]
    S1_DCBUSVOLTAGE=request["S1_DCBUSVOLTAGE"]
    S1_OUTPUTCURRENT=request["S1_OUTPUTCURRENT"]
    S1_OUTPUTVOLTAGE=request["S1_OUTPUTVOLTAGE"]
    S1_OUTPUTPOWER=request["S1_OUTPUTPOWER"]
    S1_SYSTEMINERTIA=request["S1_SYSTEMINERTIA"]
    M1_CURRENT_PROGRAM_NUMBER=request["M1_CURRENT_PROGRAM_NUMBER"]
    M1_SEQUENCE_NUMBER=request["M1_SEQUENCE_NUMBER"]
    M1_CURRENT_FEEDRATE=request["M1_CURRENT_FEEDRATE"]

    machine_status = [[X1_ACTUALPOSITION, X1_ACTUALVELOCITY, X1_ACTUALACCELERATION,
                       X1_COMMANDPOSITION, X1_COMMANDVELOCITY, X1_COMMANDACCELERATION,
                       X1_CURRENTFEEDBACK, X1_DCBUSVOLTAGE, X1_OUTPUTCURRENT,
                       X1_OUTPUTVOLTAGE, X1_OUTPUTPOWER, Y1_ACTUALPOSITION,
                       Y1_ACTUALVELOCITY, Y1_ACTUALACCELERATION, Y1_COMMANDPOSITION,
                       Y1_COMMANDVELOCITY, Y1_COMMANDACCELERATION, Y1_CURRENTFEEDBACK,
                       Y1_DCBUSVOLTAGE, Y1_OUTPUTCURRENT, Y1_OUTPUTVOLTAGE,
                       Y1_OUTPUTPOWER, Z1_ACTUALPOSITION, Z1_ACTUALVELOCITY,
                       Z1_ACTUALACCELERATION, Z1_COMMANDPOSITION, Z1_COMMANDVELOCITY,
                       Z1_COMMANDACCELERATION, Z1_CURRENTFEEDBACK, Z1_DCBUSVOLTAGE,
                       Z1_OUTPUTCURRENT, Z1_OUTPUTVOLTAGE, S1_ACTUALPOSITION,
                       S1_ACTUALVELOCITY, S1_ACTUALACCELERATION, S1_COMMANDPOSITION,
                       S1_COMMANDVELOCITY, S1_COMMANDACCELERATION, S1_CURRENTFEEDBACK,
                       S1_DCBUSVOLTAGE, S1_OUTPUTCURRENT, S1_OUTPUTVOLTAGE,
                       S1_OUTPUTPOWER, S1_SYSTEMINERTIA, M1_CURRENT_PROGRAM_NUMBER,
                       M1_SEQUENCE_NUMBER, M1_CURRENT_FEEDRATE]]


    machine_status_array = np.array(machine_status)
    print(machine_status_array)
    print("Machine status shape:", machine_status_array.shape)
    prediction = estimator.predict(machine_status_array)

    return prediction[0] 


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict/toolwear")
async def predict_tool_wear_status(request: CNCMachine):
    prediction = predict_tool_wear(estimator_toolwear, request.dict())
    
    # Convert numpy types to native Python types
    if isinstance(prediction, np.ndarray):
        prediction = prediction.tolist()
    elif isinstance(prediction, np.int64):
        prediction = int(prediction)
    elif isinstance(prediction, np.float64):
        prediction = float(prediction)

    return prediction
