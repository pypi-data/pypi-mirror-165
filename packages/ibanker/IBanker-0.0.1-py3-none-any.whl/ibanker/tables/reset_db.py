from os import path

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from tinydb import TinyDB

from ..tables.tables import *


def load_zipped():
    """
    > It takes a JSON file, loads it into a TinyDB database, and returns a list of tuples containing the
    ticker and cik for each company
    :return: A list of tuples.
    """
    abspath = path.abspath("ibanker/tables/data/ticks_and_ciks_db.json")
    info = TinyDB(abspath).all()

    tickers = [ticker["ticker"] for ticker in info]
    ciks = [cik["cik"] for cik in info]

    return list(zip(tickers, ciks))


def reset():
    """
    It drops all the tables in the database, creates them again, and then loads the ticker-cik pairs
    into the database
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    zipped = load_zipped()

    objects = [Ticker(ticker=ticker, cik=cik) for ticker, cik in zipped]

    with Session(engine) as session:
        session.add_all(objects)
        session.commit()
