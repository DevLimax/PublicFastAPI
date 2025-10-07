import json
import asyncio
from colorama import init, Fore
from publicapi.core.db import Session
from publicapi.models import IesModel

init(autoreset=True)
BATCHSIZE = 100

async def add_ies_to_db():
    async with Session() as session:    
        with open("src/Scripts/json/universidades.json", "r", encoding="utf-8") as file:
            list_ies = json.load(file)       
            
            for ies in list_ies:
                ies_instance = IesModel(
                        id = int(ies.get('id')),
                        name = str(ies.get('name')),
                        abbreviation = str(ies.get('abbreviation')),
                        type = str(ies.get('type')),
                        city_id = int(ies.get('city_id')) if ies.get('city_id') != '' else None,
                        state_id = int(ies.get('state_id')),
                        site = str(ies.get('site'))
                )
                try:
                    ies_instance.validate_data()
                    session.add(ies_instance)
                    await session.commit()
                    await session.refresh(ies_instance)
                    print(f"{Fore.GREEN}Added successfully - Data: {ies_instance.__dict__}{Fore.RESET}")
                    
                except Exception as e:
                    print(f"{Fore.RED}Error: {str(e)}{Fore.RESET}")
                    await session.rollback()
                    continue
       
if __name__ == "__main__":
    asyncio.run(add_ies_to_db())
    
    