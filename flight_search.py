from dotenv import dotenv_values
import requests
from flight_data import FlightData

ENV = dotenv_values(".env")
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"

class FlightSearch:
    def get_destination_code(self, city):
        location_end_point = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {
            "apikey": ENV["API_KEY"]
        }
        query = {
            "term": city,
            "locaiton_type": "city"
        }
        
        response = requests.get(url=location_end_point,
                                headers=headers,
                                params=query)
        
        result = response.json()['locations']
        code = result[0]["code"]
        print(f"Flight Searching: {response}")
        return code
        
      
    def check_flight(self, origin_city_code, destination_city_code, from_time, to_time):
        location_end_point = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {
            "apikey": ENV["API_KEY"]
        }
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search",
                                headers=headers,
                                params=query)
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None
        
        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data