import io
import fastapi
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd


app = fastapi.FastAPI()


@app.get('/')
async def index() -> str:
    return 'hello'


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
