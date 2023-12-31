from sqlalchemy import Column, Float, String, Date, Enum, UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as pgUUID

from sqlalchemy.orm import validates

import uuid

from datetime import datetime

Base = declarative_base()

class StockData(Base):
    __tablename__ = 'stock_data'

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    ticker = Column(String)
    stock_interval = Column(Enum("daily", "hourly", name="interval_options"))
    stock_datetime = Column(Date)
    stock_adj_volume = Column(Float)
    stock_adj_open = Column(Float)
    stock_adj_close = Column(Float)
    stock_adj_high = Column(Float)
    stock_adj_low = Column(Float)

class StockDomains(Base):
    __tablename__ = 'stock_domains'

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    ticker = Column(String)
    stock_interval = Column(String)
    start_datetime = Column(Date)
    end_datetime = Column(Date)
    sparsity_mapping = Column(String)
    __table_args__ = (UniqueConstraint(ticker, stock_interval),)

    @validates("sparsity_mapping")
    def validate_sparsity_mapping(self, key, mapstr):
        try:
            running_date = None

            assert mapstr[0] == '/'
            mapstr = mapstr[1:]
            continuous_intervals = mapstr.split('/')

            for continuous_interval_string in continuous_intervals:
                continuous_interval = continuous_interval_string.split("|")
                assert len(continuous_interval) == 2

                start_date = datetime.strptime(continuous_interval[0])
                stop_date = datetime.strptime(continuous_interval[1])

                assert running_date == None or start_date > running_date
                assert stop_date > start_date
                
                running_date = stop_date


        except Exception:
            raise ValueError(f"Improperly formatted sparsity mapping string {mapstr}")

        """
        1. Remove first character
        2. Track a running date
        3. split strings into stretches by `/`
            4. for each domain stretch, split it into 2 by '|'
                5. check that there are exactly 2 elements in the list
                6. check that the value is greater than the running date, then update the running date `/`
        """

        return mapstr