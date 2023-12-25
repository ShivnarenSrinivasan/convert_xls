import uvicorn
from convert_xls import server


if __name__ == '__main__':
    uvicorn.run(server.app, port=8001)
