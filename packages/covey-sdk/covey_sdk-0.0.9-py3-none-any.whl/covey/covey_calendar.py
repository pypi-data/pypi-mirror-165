import pytz
import os
import time
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetCalendarRequest



class CoveyCalendar:
    def __init__(self, **kwargs):
        # load environment variables (aplaca private and public keys)
        load_dotenv()
    
        # get the start date, default to 3 years ago
        self.start_date = kwargs.get('start_date', (datetime.now() - timedelta(days=3*365)).strftime('%Y-%m-%d'))

        # get the end date, default to today
        self.end_date = kwargs.get('end_date', datetime.now().strftime('%Y-%m-%d'))

        # # initialize the alpaca rest api if it is not provided
        # self.alpaca_api = kwargs.get('alpaca_api', REST())
        # create and fill the dates data frame
        # initialize the trading client
        self.trading_client = TradingClient(api_key=os.environ.get('APCA_API_KEY_ID'), 
                                            secret_key=os.environ.get('APCA_API_SECRET_KEY'))

        self.business_dates = self.set_business_dates()

    def set_business_dates(self):
        # alpaca calendar to denote business days
        # the format comes in as date and time so we combine them
        # we are pulling the next available business open and close date time

        delayed_trade_date_time_df = pd.DataFrame(
            {
                'next_market_open': [x.open.astimezone(pytz.utc).replace(tzinfo=None) for x in 
                                        self.trading_client.get_calendar(filters = GetCalendarRequest(start = self.start_date))],
                'next_market_close': [x.close.astimezone(pytz.utc).replace(tzinfo=None) for x in 
                                        self.trading_client.get_calendar(filters = GetCalendarRequest(start = self.start_date))]
            })

        # agnostic date range of all days between min trade key date and max alpaca business date
        date_df = pd.DataFrame({'date': pd.date_range(start=self.start_date,
                                                      end=delayed_trade_date_time_df['next_market_open'].max())})

        # next raw date so that we can get the 'next delayed trade open
        date_df['date_t_plus_1'] = date_df['date'] + timedelta(days=1)

        # conversion for merging
        delayed_trade_date_time_df['next_market_open_date'] = \
            pd.to_datetime(delayed_trade_date_time_df['next_market_open']).dt.date

        # conversion for merging
        delayed_trade_date_time_df['next_market_open_date'] = pd.to_datetime(
            delayed_trade_date_time_df['next_market_open_date'])

        # merging agnostic dates with business dates
        bus_date_key_df = pd.merge(left=date_df, right=delayed_trade_date_time_df,
                                   how='left', left_on='date',
                                   right_on='next_market_open_date')

        # merging agnostic dates with business dates one more time (for next business day)
        bus_date_key_df = pd.merge(left=bus_date_key_df, right=delayed_trade_date_time_df,
                                   how='left', left_on='date_t_plus_1',
                                   right_on='next_market_open_date')

        # drop all the _x and replace _y with _t_plus_1
        bus_date_key_df.rename(columns=lambda s: s.replace('_x', '').replace('_y', '_t_plus_1'), inplace=True)

        # back-filling empty merge results so that the next business day propgates backwards for non business days
        bus_date_key_df.fillna(method='bfill', inplace=True)
        bus_date_key_df.dropna(inplace=True)

        return bus_date_key_df


if __name__ == '__main__':
    start_time = time.time()

    c = CoveyCalendar()

    print(c.business_dates)


    print("---Calendar finished in %s seconds ---" % (time.time() - start_time))