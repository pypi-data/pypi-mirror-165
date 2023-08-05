import os
import time
import pandas as pd
from dotenv import load_dotenv
from dataclasses import make_dataclass
from datetime import date, datetime,timedelta

# # covey libraries - internal test
# from utils import get_data, get_output, get_checks
# from covey_trade import Trade
# import covey_checks as covey_checks 
# from covey_calendar import CoveyCalendar

# covey libraries - packaging
from covey import get_data, get_output, get_checks
from covey.covey_trade import Trade
import covey.covey_checks as covey_checks 
from covey.covey_calendar import CoveyCalendar

class Portfolio(Trade):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # default start cash to 10000
        self.start_cash = kwargs.get('start_cash', 10000)
        # default annual interest to 0.2 %
        self.ann_interest = kwargs.get('ann_interest', 0.02)
        # initialize the portfolio
        self.reset_portfolio()
        # initialize trading_key portfolio derived columns
        self.set_trading_key()
        # generate crypto pricing error report
        self.unpriced_crypto = covey_checks.check_crypto_tickers(self.trading_key)
    
    def get_start_date(self, day_offset : int = 0) -> datetime:
        if len(self.trades.index) > 1:
            start_date = self.trading_key['market_entry_date_time'].min() + timedelta(days= day_offset)
            return start_date.replace(hour=0)
        else:
            return datetime(year=2021,month=12,day=31)

    def set_trading_key(self):
        self.trading_key = self.trading_key[~self.trading_key['vwap'].isnull()]
        self.trading_key[[
            'post_cumulative_share_count',
            'realized_profit',
            'long_realized_profit',
            'short_realized_profit',
            'prior_portfolio_value',
            'current_position',
            'prior_position_value',
            'cash_used',
            'share_count',
            'prior_cumulative_share_count',
            'post_cumulative_share_count',
            'adjusted_entry'
        ]] = 0
        return 0

    def reset_portfolio(self):
        # create the portfolio row entry dataclass 
        portfolio_entry = make_dataclass('portfolio_entry',
        [('date_time',datetime),
        ('cash',float),
        ('usd_value',float), 
        ('positions_usd',float),
        ('long_exposure_usd',float),
        ('short_exposure_usd',float),
        ('gross_traded_usd',float),
        ('gross_traded_percent',float),
        ('net_traded_usd',float),
        ('net_traded_percent',float),
        ('unrealized_long_pnl',float), 
        ('unrealized_short_pnl',float),
        ('realized_long_pnl',float), 
        ('realized_short_pnl',float),
        # derived columns - dollar exposure
        ('gross_exposure_usd',float),
        ('net_exposure_usd',float),
        # derived columns - percent exposure
        ('gross_exposure_percent',float),
        ('long_exposure_percent',float),
        ('short_exposure_percent',float),
        ('net_exposure_percent',float),
        # derived columns - pnl totals
        ('unrealized_pnl',float),
        ('realized_pnl',float),
        ('total_long_pnl',float),
        ('total_short_pnl',float),
        ('total_pnl',float),
        # the main goal - inception to date return
        ('inception_return', float),
        # helper previous portfolio usd
        ('previous_usd_value',float)
        ])
        
        # initialize the first row of the portfolio - start date, start cash, and remanining 9 zeros 
        self.portfolio = pd.DataFrame([portfolio_entry(self.get_start_date(-1), self.start_cash, self.start_cash,
                        0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0, self.start_cash)])
        
        # set the index to be date_time
        self.portfolio.set_index('date_time', inplace=True)

        # fill in the rest of the date index using covey calender market close times
        c = CoveyCalendar(start_date = self.get_start_date().strftime('%Y-%m-%d'))
        calendar_key = c.set_business_dates()
        max_calendar_date = min(self.price_key.reset_index()['timestamp'].max(),calendar_key['next_market_close'].max())
        calendar_mask = calendar_key['next_market_close'] <= max_calendar_date
        calendar_key_df = pd.DataFrame(calendar_key[calendar_mask]['next_market_close'].unique())
        
        # set the calendar index to be datetime so we can concat easily
        calendar_key_df.set_index(0, inplace=True)

        # attach the dates back to the original portfolio row
        self.portfolio = pd.concat([self.portfolio, calendar_key_df])

        return 0

    def get_active_positions(self, portfolio_date):

        columns = ['address','symbol', 'target_percentage','post_cumulative_share_count', 'vwap', 
        'current_position', 'long_post_cumulative_share_count','short_post_cumulative_share_count',
        'realized_profit', 'dividend_cash', 'dividend_cash_long','dividend_cash_short']

        df = self.trading_key.copy()
        
        df = df[(df['market_entry_date_time'] < portfolio_date) ]
        df['symbol_date_rank'] = df.groupby('symbol')['entry_date_time'].rank('dense', ascending=False)

        # realized profit sum partitioned by symbol
        df['realized_profit_symbol_agg'] = df.groupby('symbol')['realized_profit'].transform(sum)
        df['realized_profit_final'] = df['realized_profit_symbol_agg'] - df['realized_profit']
        df = df[(df['symbol_date_rank'] == 1) & (df['post_cumulative_share_count'] != 0)]
        df['current_position'].fillna(0, inplace=True)

        if len(df.index) < 1:
            return pd.DataFrame(columns=columns)

        # export to csv
        self.export_to_csv(key = 'position', df = df)

        # dividend logic 
        dividends_df = pd.read_csv(get_data('dividend_split.csv'))
        dividends_df['payment_date'] = pd.to_datetime(dividends_df['payment_date'])
        dividends_df = dividends_df[(dividends_df['div_or_split'] == 'dividend') & (dividends_df['payment_date'] == portfolio_date)][['symbol','amount']]

        # merge to main df (trading key) and calculate dividends
        df = pd.merge(left=df, right=dividends_df, on = 'symbol', how='left')
        df.rename(columns={'amount':'div_amount'}, inplace=True)
        df['dividend_cash'] = df['div_amount'] * df['post_cumulative_share_count']

        # if we don't have dividends, sad but have to fill with 0
        df['dividend_cash'].fillna(0,inplace=True)

        # split logic
        splits_df = pd.read_csv(get_data('dividend_split.csv'))
        splits_df['payment_date'] = pd.to_datetime(splits_df['payment_date'])
        splits_df = splits_df[(splits_df['div_or_split'] == 'split') & (splits_df['payment_date'] == portfolio_date)][['symbol', 'amount']]
        df = pd.merge(left=df, right=splits_df, on = 'symbol', how='left')
        df.rename(columns={'amount':'split_amount'}, inplace=True)

        # fill NA split amounts as 1 so it won't nullify the new vwap price post multiplication
        df['split_amount'] .fillna(1, inplace=True)
        df['adjusted_entry'] = df['vwap']
        df['vwap'] = df['vwap'] * df['split_amount'] 
        df['post_cumulative_share_count'] = df['post_cumulative_share_count'] / df['split_amount'] 

        # split out long and short share counts - to be multiplied by active prices later
        df['long_post_cumulative_share_count'] = df.apply(lambda x : x['post_cumulative_share_count'] if x['post_cumulative_share_count'] > 0 else 0, axis=1)
        df['short_post_cumulative_share_count'] = df.apply(lambda x : x['post_cumulative_share_count'] if x['post_cumulative_share_count'] < 0 else 0, axis = 1)

        # split out the long vs short dividends
        df['dividend_cash_long'] = df.apply(lambda x : x['dividend_cash'] if x['post_cumulative_share_count'] > 0  else 0, axis=1)
        df['dividend_cash_short'] = df.apply(lambda x : x['dividend_cash'] if x['post_cumulative_share_count'] < 0  else 0, axis=1)

        # final filter for no current positions of 0 value in case they were missed with the post cumulative filter
        df = df[df['current_position'] != 0]

        # # export to csv
        # self.export_to_csv(key = 'position', df = df)

        return df[columns]
    
    def get_previous_positions(self, symbol, latest_index):
        # previous positions mask
        prev_mask = (self.trading_key.symbol == symbol) & (self.trading_key.index < latest_index)

        # isolate the trading key for desired symbol
        df = self.trading_key[prev_mask]

        # return dataframe with latest instance - if there was no history for this ticker it will lookup on -1
        # and return an empty dataframe
        if len(df.index) > 0:
            latest_index = df.index.max()
            return df[df.index == latest_index]
        else:
            return df

    def process_trades(self, row, prior_portfolio_usd):
        
        # there arent any trades dont even bother
        if len(row.index) == 0:
            return 0
        
        # symbol didn't get priced so make all of the numeric columns (except prior port)

        # current index
        current_index = row.index[0]

        # current price
        current_price = row.vwap.unique()[0]

        # previous positions isolation
        previous_positions = self.get_previous_positions(row.symbol.unique()[0], row.index[0])

        if len(previous_positions.index) > 0:
            # previous index
            previous_index = previous_positions.index[0]
            
            # previous price
            prior_price = previous_positions['vwap'].unique()[0]

            # trade key metrics : prior shares
            prior_shares = previous_positions['post_cumulative_share_count'].unique()[0]

            # trade key metrics recording : current index : prior shares
            self.trading_key['prior_cumulative_share_count'].at[current_index] = prior_shares

            # trade key metrics : prior_profit
            prior_profit = (current_price - prior_price) * prior_shares

            # trade key metrics recording : prev index : prior profit (aka realized profit)
            self.trading_key['realized_profit'].at[previous_index] = prior_profit

            # allocate the long short pnl, since in this if block we know there's
            # non zero previous position
            if prior_shares > 0:
                # trade key metrics recording : prev index : long realized profit 
                self.trading_key['long_realized_profit'].at[previous_index] = prior_profit
            else: 
                # trade key metrics recording : prev index : short realized profit
                self.trading_key['short_realized_profit'].at[previous_index] = prior_profit

            # trade key metrics recording : current index : prior position value 
            self.trading_key['prior_position_value'].at[current_index] = current_price * prior_shares
        else:
            # no previous positions means all 0 for these metrics
            prior_shares = 0
            self.trading_key['prior_cumulative_share_count'].at[current_index] = 0
            self.trading_key['prior_position_value'].at[current_index] = 0

        # set the current metrics - now that we took all we need from previous positions (profit + prior shares)
        # prior portfolio value
        self.trading_key['prior_portfolio_value'].at[current_index] = prior_portfolio_usd

        # trade key metrics : current index : current position (0 if current price is 0)
        self.trading_key['current_position'].at[current_index] = 0 if current_price == 0 else float(row['target_percentage']) * prior_portfolio_usd

        # trade key metrics : current index : cash used 
        self.trading_key['cash_used'].at[current_index] = self.trading_key['prior_position_value'].at[current_index] - \
                                                self.trading_key['current_position'].at[current_index]
        
        # trade key metrics : current index : change in shares (0 if current price is 0)
        self.trading_key['share_count'].at[current_index] = 0 if current_price == 0 else -1 * self.trading_key['cash_used'].at[current_index] / current_price

        # trade key metrics : current index : post cumulative share count (0 if current price is 0)
        self.trading_key['post_cumulative_share_count'].at[current_index] = 0 if current_price == 0 else self.trading_key['share_count'].at[current_index] + prior_shares

        return 0
   
    def evaluate_portfolio_row(self, row):
        self.portfolio.sort_index(ascending=True, inplace=True)
        current_loc= self.portfolio.index.get_loc(row.index[0])
        
        # start date is really the previous date
        start_date = self.portfolio.index[current_loc - 1]
        end_date = self.portfolio.index[current_loc]
        
        # daily interest
        daily_interest = self.ann_interest * (end_date - start_date) / timedelta(days=365)

        # get the previous portfolio value
        prior_portfolio_usd = self.portfolio.loc[start_date,'usd_value']

        # get the previous portfolio inception return 
        prior_portfolio_inception_return = self.portfolio.loc[start_date,'inception_return']

        print(end_date, prior_portfolio_usd)

        # get prior cash
        prior_cash = self.portfolio.loc[start_date,'cash']

        # set up a new starting cash balance and calculate any interest cost for leverage
        cash_interest_payment = 0 if prior_cash > 0 else prior_cash * daily_interest

        # set up new cash - will pass it into the trade processing
        new_cash = prior_cash + cash_interest_payment

        # set up in scope trades mask - any trades made up until this point (end_date), as of the last portfolio timestamp (start_date)
        new_trades_mask = (self.trading_key['market_entry_date_time'] <= end_date) & (self.trading_key['market_entry_date_time'] > start_date)
        
        # isolate the new trades 
        new_trades = self.trading_key[new_trades_mask]

        # process the new trades batch
        new_trades.groupby('trade_id').apply(self.process_trades,(prior_portfolio_usd))

        # refresh the new trades now that the trading key changed
        new_trades = self.trading_key[new_trades_mask]

        # all trades mask - will be used for a complete lookback for realized long and short pnl
        all_trades_mask = (self.trading_key['market_entry_date_time'] <= end_date)

        # isolate all trades up to the current portfolio date index
        all_trades = self.trading_key[all_trades_mask]

        # before we add dividends to the cash - update gross_traded_usd 
        self.portfolio.iloc[current_loc,5] = new_trades['cash_used'].abs().sum()

        # before we add dividends to the cash - update net_traded_usd 
        self.portfolio.iloc[current_loc,7] = -1* new_trades['cash_used'].sum()

        # update cash after most recent trades processed/updated
        new_cash += new_trades['cash_used'].sum() + new_trades['cash_used'].abs().sum() * -0.0005
        
        # look through active trades - these are the trades before the 'trades in scope'
        # we are updating their metrics now that we handled the new trades
        active_trade_stats_df = self.get_active_positions(end_date)

        # get the most up to date prices for the tickers we already had trades for
        active_prices_df = self.price_key.loc[self.price_key.timestamp == end_date]

        # merge active trades with active prices to get the up to date values on all the existing positions
        active_df = pd.merge(left=active_trade_stats_df, right=active_prices_df, how='inner', on='symbol')

        # set up price change column for unrealized pnl calc
        active_df['price_change'] = active_df['vwap_y'] - active_df['vwap_x']

        # update portfolio active position(s) value
        self.portfolio.iloc[current_loc,2] = active_df['post_cumulative_share_count'].multiply(active_df['vwap_y']).sum()

        # update portfolio cash amount = prior cash + cash used in trading + dividends
        self.portfolio.iloc[current_loc,0] = new_cash + active_df['dividend_cash'].sum()

        # update portfolio usd value = cash + positions
        self.portfolio['usd_value'] = self.portfolio['cash'] + self.portfolio['positions_usd']

        # update portfolio long exposure usd - coming from active_df -> active trades + active prices
        self.portfolio.iloc[current_loc, 3] = active_df['long_post_cumulative_share_count'].multiply(active_df['vwap_y']).sum()

        # update portfolio short exposure usd - coming from active_df -> active trades + active prices
        self.portfolio.iloc[current_loc, 4] = active_df['short_post_cumulative_share_count'].multiply(active_df['vwap_y']).sum()

        # similar logic for long unrealized pnl - coming from active df -> post cumulative shares * price change
        self.portfolio.iloc[current_loc, 9] = active_df['long_post_cumulative_share_count'].multiply(active_df['price_change']).sum()

        # similar logic for short unrealized pnl - coming from active df -> post cumulative shares * price change
        self.portfolio.iloc[current_loc, 10] = active_df['short_post_cumulative_share_count'].multiply(active_df['price_change']).sum()

        # long realized pnl -> new trades long realized profit + active trades long dividend + cash interest 
        # + previous portfolio long realized pnl
        self.portfolio.iloc[current_loc,11] = all_trades['long_realized_profit'].sum() + active_df['dividend_cash_long'].sum() + cash_interest_payment 

        # short realized pnl -> new trades long realized profit + active trades short dividend 
        # + previous portfolio short realized pnl
        self.portfolio.iloc[current_loc,12] = all_trades['short_realized_profit'].sum() + active_df['dividend_cash_short'].sum() 

         # LE PIECE DE RESISTANCE - INCEPTION TO DATE RETURNS
        # (usd value at current row / usd value at previous row) *  inception return at previous row
        self.portfolio.iloc[current_loc,24] = (self.portfolio.iloc[current_loc,1] / prior_portfolio_usd) * prior_portfolio_inception_return
    
    def calculate_portfolio(self):
        # if its effectively no trading history (DUMMY ticker only)
        if self.trading_key.symbol.unique()[0] == 'DUMMY' and len(self.trading_key.index) == 1:
            self.portfolio.ffill(inplace=True)

            # exit the function
            return 0

        # get the main portfolio calculations
        self.portfolio.iloc[1:,:].groupby(self.portfolio.index[1:]).apply(self.evaluate_portfolio_row)

        # previous portfolio value as a helper
        self.portfolio.iloc[:,25] = self.portfolio.iloc[:,1].shift(fill_value=self.start_cash)

        # caclulate gross_traded   _percent 
        self.portfolio.iloc[1:,6] = self.portfolio.iloc[1:,5]/self.portfolio.iloc[1:,25]

        # caclulate net_traded_percent
        self.portfolio.iloc[1:,8] = self.portfolio.iloc[1:,7]/self.portfolio.iloc[1:,25]

        # derived column : gross exposure usd = long - short
        self.portfolio.iloc[1:,13] = self.portfolio.iloc[1:,3] - self.portfolio.iloc[1:,4]
        
        # derived column : net exposure usd = long + short
        self.portfolio.iloc[1:,14] = self.portfolio.iloc[1:,3] + self.portfolio.iloc[1:,4]
        
        # derived column : gross exposure percent = gross exposure / previous usd value
        self.portfolio.iloc[1:,15] = self.portfolio.iloc[1:,13]/self.portfolio.iloc[1:,25]

        # derived column : long exposure percent = long exposure / previous usd value
        self.portfolio.iloc[1:,16] = self.portfolio.iloc[1:,3]/self.portfolio.iloc[1:,25]

        # derived column : short exposure percent = short exposure / previous usd value
        self.portfolio.iloc[1:,17] = self.portfolio.iloc[1:,4]/self.portfolio.iloc[1:,25]

        # derived column : net exposure percent = net exposure / previous usd value
        self.portfolio.iloc[1:,18] = self.portfolio.iloc[1:,14]/self.portfolio.iloc[1:,25]

        # derived column : unrealized pnl = unrealized long pnl + unrealized short pnl
        self.portfolio.iloc[1:,19] = self.portfolio.iloc[1:,9] + self.portfolio.iloc[1:,10]

        # derived column : realized pnl = realized long pnl + realized short pnl
        self.portfolio.iloc[1:,20] = self.portfolio.iloc[1:,11] + self.portfolio.iloc[1:,12]

        # derived column : total long pnl = unrealized long pnl + realized long pnl
        self.portfolio.iloc[1:,21] = self.portfolio.iloc[1:,9] + self.portfolio.iloc[1:,11]

        # derived column : total short pnl = unrealized short pnl + realized short pnl
        self.portfolio.iloc[1:,22] = self.portfolio.iloc[1:,10] + self.portfolio.iloc[1:,12]

        # derived column : total pnl = unrealized pnl + realized pnl or total long pnl + total short pnl
        self.portfolio.iloc[1:,23] = self.portfolio.iloc[1:,21] + self.portfolio.iloc[1:,22]

        # export portfolio output to csv format
        self.export_to_csv('portfolio')

        # export trading key output to csv format
        self.export_to_csv('trading')

        # export price key output to csv format
        self.export_to_csv('price')

        return 0

    # export to csv
    def export_to_csv(self, key: str = 'trading', df : pd.DataFrame = None):
        if key == 'trading':
            self.trading_key.to_csv(get_output('trading_key.csv'), index=False)
        elif key == 'price':
            self.price_key.to_csv(get_output('price_key.csv'))
        elif key == 'portfolio':
            self.portfolio.to_csv(get_output('portfolio.csv'))
        elif key == 'crypto_check':
            self.unpriced_crypto.to_csv(get_checks('unpriced_crypto_test_{}.csv'.format(self.address)))
        elif key == "position":
            df.to_csv(get_output('latest_positions.csv'), index=False)


if __name__ == '__main__':
     # load environment variables (aplaca private and public keys)
    load_dotenv()

    # start the timer
    start_time = time.time()

    # initialize an example portfolio
    p = Portfolio(address='0x31141854e4C5B732127507654a9D1E83b7b082d2')

    # calculate the portfolio from inception
    p.calculate_portfolio()

    # print statement announcing finish and run time taken
    print("---Portfolio finished in %s seconds ---" % (time.time() - start_time))
