from datetime import date
from datetime import timedelta

from CleanEmonCore.Events import Observer
from CleanEmonCore.Events.builtins import DateChange

from ..lib.DBConnector import fetch_data
from ..lib.DBConnector import send_data

from ..Disaggregator import energy_data_to_dataframe
from ..Disaggregator import dataframe_to_energy_data
from ..Disaggregator import disaggregate


def update(yesterday: str):
    energy_data = fetch_data(yesterday)
    df = energy_data_to_dataframe(energy_data)

    df = disaggregate(df)
    dis_energy_data = dataframe_to_energy_data(df)
    send_data(yesterday, dis_energy_data)


def run():
    class Updater(Observer):
        def on_notify(self, *args, **kwargs):
            if "date" in kwargs:
                yesterday = kwargs["date"]
            else:  # By default, get the previous date
                yesterday = date.today() - timedelta(days=1)
            update(str(yesterday))

    event = DateChange(3, initial_date=date.today())  # todo: increase interval to reduce execution time?
    Updater(event)

    event.run()
