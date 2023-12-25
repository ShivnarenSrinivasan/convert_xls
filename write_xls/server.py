import io
import fastapi
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd


app = fastapi.FastAPI()


@app.get("/_xlsx")
def get_excel_data():
    df = pd.DataFrame([["Canada", 10], ["USA", 20]], columns=["team", "points"])
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)
    return StreamingResponse(
        io.BytesIO(buffer.getvalue()),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment; filename=data.xlsx"},
    )


@app.post("/xlsx")
def upload_file(file: UploadFile = File(...)) -> StreamingResponse:
    contents = file.file.read()
    df = pd.read_csv(io.BytesIO(contents))
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlwt') as writer:
        df.to_excel(writer, index=False)

    return StreamingResponse(
        io.BytesIO(buffer.getvalue()),
        media_type='application/vnd.ms-excel',
        headers={"Content-Disposition": "attachment; filename=data.xls"},
    )
