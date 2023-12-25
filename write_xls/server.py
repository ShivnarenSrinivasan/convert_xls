import mimetypes
import fastapi
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse

from . import _io

app = fastapi.FastAPI()

mimetypes.add_type('text/csv', '.csv')


@app.get('/')
async def index() -> str:
    return 'hello'


@app.post("/convert")
def upload_file(
    fromType: _io.FileType, toType: _io.FileType, file: UploadFile = File(...)
) -> StreamingResponse:
    contents = file.file.read()
    converted = _io.convert(fromType, toType, contents)

    return StreamingResponse(
        converted,
        media_type=mimetypes.types_map[f'.{toType.value}'],
        headers={"Content-Disposition": f"attachment; filename=data.{toType}"},
    )
