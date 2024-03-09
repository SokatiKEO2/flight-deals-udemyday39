import requests
from dotenv import dotenv_values

ENV = dotenv_values(".env")

class DataManager:
    def __init__(self):
        self.destination_data = {}
        
    
    def get_destination_data(self):
        response = requests.get(ENV["GOOGLE_SHEET_END_POINT"])
        data = response.json()
        
        self.destination_data = data["prices"]
        return self.destination_data
        

    def update_destination_code(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{ENV['GOOGLE_SHEET_END_POINT']}/{city['id']}",
                json=new_data
            )
            print(f"Updating Data: {response}")