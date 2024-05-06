import asyncio
from fastapi import FastAPI, Path, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
import requests
from data_processing import *

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
    searchData = reponse.json()
    
    return templates.TemplateResponse("search.html", {"request": request, "data": searchData , "servers" : server_dict })


@app.get("/info",  response_class=HTMLResponse)
async def info(request: Request, characterId: str, serverId: str):
    tasks = [
        fetch_equipment_info(characterId, serverId, API_KEY),
        fetch_avatar_info(characterId, serverId, API_KEY),
        fetch_status_info(characterId, serverId, API_KEY),
        fetch_creature_info(characterId, serverId, API_KEY),
        fetch_flag_info(characterId, serverId, API_KEY),
        fetch_talisman_info(characterId, serverId, API_KEY),
        fetch_equipment_trait_info(characterId, serverId, API_KEY)
    ]

    # 모든 비동기 작업을 병렬로 실행합니다.
    results = await asyncio.gather(*tasks)

    # 결과 처리
    equipmentsJSON, avatarJSON, statusJSON, creatureJSON, flagJSON, talismanJSON, traitJSON = results

    # equipmentsJSON = 장착 장비
    # avatarJSON = 아바타
    # statusJSON =  스탯
    # creatureJSON = 크리쳐
    # flagJSON = 휘장
    # talismanJSON = 탈리스만
    # traitJSON = 장비 특성

    


    if equipmentsJSON:
        return templates.TemplateResponse("info.html",
                                          { "request": request,
                                            "equipmentsJSON": equipmentsJSON,
                                            "avatarJSON": avatarJSON,
                                            "servers": server_dict,
                                            "statusJSON": statusJSON,
                                            "creatureJSON": creatureJSON,
                                            'flagJSON': flagJSON,
                                            "talismanJSON": talismanJSON,
                                            "traitJSON": traitJSON})
    else:
        return "No data found"

