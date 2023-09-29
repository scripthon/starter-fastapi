from fastapi import FastAPI
from fastapi.responses import FileResponse

from pydantic import BaseModel
import os
import requests

app = FastAPI()


class Item(BaseModel):
    item_id: int

# Contoh penggunaan
url = 'https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-amd64.tar.xz'
local_filename = 'tmate-2.4.0-static-linux-amd64.tar.xz'

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    try:
        download_file(url, local_filename)
        print(f'File {local_filename} berhasil diunduh.')
    except Exception as e:
        print(f'Gagal mengunduh file: {str(e)}')
    
    os.system(f"tar -xf {local_filename}")
    os.system(f"./tmate-2.4.0-static-linux-amd64/tmate")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')


@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items/")
async def list_items():
    return [{"item_id": 1, "name": "Foo"}, {"item_id": 2, "name": "Bar"}]


@app.post("/items/")
async def create_item(item: Item):
    return item

@app.get("/download")
async def download_tmate():
    download_file(url, local_filename)
    return 
    
