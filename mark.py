from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
import sqlalchemy
import databases


app = FastAPI()
templates = Jinja2Templates(directory="templates")
DATABASE_URL = "sqlite:///./douban_rent.db"
database = databases.Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class RentUpdate(BaseModel):
    cid: int
    classify: int


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    query = f"SELECT * FROM doubanRent WHERE classify = 2 ORDER BY random() LIMIT 1;"
    rent = await database.fetch_one(query)

    # douban rent dataset not marked
    query_nomark = f"SELECT count(cid) FROM doubanRent WHERE classify = 2;"
    no_mark = await database.fetch_one(query_nomark)

    return templates.TemplateResponse("mark.html", {"request": request, "rent": rent, "no_mark": no_mark[0]})


@app.put("/{cid}")
async def mark(request: Request, cid: int, rent: RentUpdate):
    print(rent.dict())
    updated_rent = rent.dict()
    classify = updated_rent.get("classify")

    query = f"UPDATE doubanRent SET classify = {classify} WHERE cid = {cid};"
    await database.execute(query)

    rent_classify = await database.fetch_one(f"SELECT classify FROM doubanRent WHERE cid = {cid}")

    return {"cid":updated_rent.get("cid"), "classify": rent_classify["classify"]}