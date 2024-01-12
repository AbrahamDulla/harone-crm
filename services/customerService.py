from fastapi import FastAPI, HTTPException, status, Query, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None
