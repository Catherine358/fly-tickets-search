import requests

SHEETY_PRICES_ENDPOINT = "Google sheet link"


class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )

    def update_destination_price(self, flight):
        for city in self.destination_data:
            if city["city"] == flight.destination_city:
                new_data = {
                    "price": {
                        "lowestPrice": flight.price,
                        "date": f"from {flight.out_date} to {flight.return_date}"
                    }
                }
                response = requests.put(
                    url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                    json=new_data
                )
