import requests

equipment_type = {
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

class EquipmentItem:
    def __init__(self, type=-1, name='', customed=-1, amplificationName='', reinforce=-1, enchant=[], refine=-1, fusioned=-1, fusionId='', options=[]):
        self.type = type # 장비 타입
        self.name = name # 장비 이름
        self.customed = customed # 커스텀 옵션 여부
        self.amplificationName = amplificationName # 증폭 종류
        self.reinforce = reinforce # 강화 수치
        self.enchant = enchant # 마부
        self.refine = refine # 제련 수치
        self.fusioned = fusioned # 융합 여부
        self.fusionId = fusionId # 융합 아이템 ID
        self.options = options # 아이템 옵션


def fetch_equipment_info(characterId: str, serverId: str, API_KEY: str):
    url = f"https://api.neople.co.kr/df/servers/{serverId}/characters/{characterId}/equip/equipment?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()


    items = []

    for equipment in data['equipment']:
        item = EquipmentItem()
        item.type = equipment['slotId']
        item.name = equipment['itemName']
        item.customed = 'customOption' in equipment
        item.amplificationName = equipment['amplificationName']
        item.reinforce = equipment['reinforce']
        item.enchant = equipment['enchant']['status']
        item.refine = equipment['refine']
        item.fusioned = 'fusionOption' in equipment

        if item.fusioned:
            item.fusionId = equipment['upgradeInfo']['itemId']
        
        if item.customed:
            item.options = equipment['customOption']['options']

        
        items.append(item)

    return data

def printOptions(options):
    for i, option in enumerate(options):
        print(f"{i+1}옵션\n\n{option['explain']}\n")


# items = fetch_equipment_info("95641d222fed92c8b80813904ccde5d7", "cain", "PZ2F29nXBUBg0LlJPTtRnw76C4r43x82")
# printOptions(items[3].options)