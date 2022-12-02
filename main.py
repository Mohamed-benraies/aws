#  Copyright (c) 2021.
#  __author__ = "Walid YAICH"
#  __copyright__ = "Copyright (c) 2021., AWS Module"
#  __license__ = "GPL"
#  __maintainer__ = "Yosra ABASSI, Chayma BEN HAHA"
#  __email__ = "abassi.yosra@tek-up.de, Chayma.BENHAHA@tek-up.de, walid.yaich@tek-up.de"
#  __status__ = "Education"
#
#
import logging
import os
from typing import Optional

import boto3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pydantic import BaseSettings

# logging configuration
logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World !"}


class File(BaseModel):
    path: str
    file_name: str
    content: Optional[str] = None


@app.post("/file/", status_code=status.HTTP_201_CREATED)
def write_text_file_to_disk(file: File) -> str:
    full_path = file.path + "/" + file.file_name
    try:
        file_handler = open(full_path, 'w')
        file_handler.write(file.content)
        logging.info("The file was stored successfully to : " + full_path)
        file_handler.close()
    except Exception:
        logging.error("Cannot write to disk !", exc_info=True)
        raise HTTPException(status_code=500, detail="Cannot write this file to disk : " + full_path)
    return "The file was stored successfully :" + full_path


@app.get("/file/")
def read_text_file_from_disk(full_path: str) -> str:
    if os.path.isfile(full_path):
        return open(full_path).read()
    else:
        raise HTTPException(status_code=404, detail="File does not exists : " + full_path)