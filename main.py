from fastapi import FastAPI, Path, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
import requests
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# dictionary to stare server information
server_dict = {}

API_KEY = "PZ2F29nXBUBg0LlJPTtRnw76C4r43x82" # Need to hide this key



server_dict =   {"cain": "카인",
        "diregie": "디레지에",
        "siroco": "시로코",
        "prey": "프레이",
        "casillas": "카시야스",
        "hilder": "힐더",
        "anton": "안톤",
        "bakal": "바칼"
    }

equipment_dict = {
    'WEAPON': 0,
    'TITLE': 1,
    'JACKET': 2,
    'SHOULDER': 3,
    'PANTS': 4,
    'SHOES': 5,
    'WAIST': 6,
    'AMULET': 7,
    'WRIST': 8,
    'RING': 9,
    'SUPPORT': 10,
    'MAGIC_STONE': 11,
    'EARRING': 12
}




@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/server")
def read_server():
    url = f"https://api.neople.co.kr/df/servers?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data


@app.get("/searchCharacter", response_class=HTMLResponse, response_model=Dict[str, str])
def search_character(request: Request, characterName: str = Query(...)):
    url = f"https://api.neople.co.kr/df/servers/all/characters?characterName={characterName}&apikey={API_KEY}"
    reponse = requests.get(url)
    data = reponse.json()
    return templates.TemplateResponse("search.html", {"request": request, "data": data , "servers" : server_dict })


@app.get("/info",  response_class=HTMLResponse)
def info(request: Request, characterId: str, serverId: str):
    url = f"https://api.neople.co.kr/df/servers/{serverId}/characters/{characterId}/equip/equipment?apikey={API_KEY}"   
    response = requests.get(url)
    data = response.json() 

    if data:
        return templates.TemplateResponse("info.html", { "request": request, "info": data, "equipment_dict": equipment_dict})
    else:
        return "No data found"

