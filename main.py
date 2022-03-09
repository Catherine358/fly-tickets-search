from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

from apscheduler.schedulers.blocking import BlockingScheduler


def some_job():
    data_manager = DataManager()
    sheet_data = data_manager.get_destination_data()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    ORIGIN_CITY_IATA = "TLV"

    if sheet_data[0]["iataCode"] == "":
        for row in sheet_data:
            row["iataCode"] = flight_search.get_destination_code(row["city"])
        data_manager.destination_data = sheet_data
        data_manager.update_destination_codes()

    in_month = datetime.now() + timedelta(days=30)
    two_month_from_today = datetime.now() + timedelta(days=(2 * 30))

    for destination in sheet_data:
        flight = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=in_month,
            to_time=two_month_from_today
        )
        try:
            if flight.price < destination["lowestPrice"]:
                data_manager.update_destination_price(flight)
                notification_manager.send_sms(
                    message=f"Low price alert! Only {flight.price} ILS to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
                )
        except AttributeError:
            continue


scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', hours=1)
scheduler.start()