import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import datetime as dt

# Disable pandas warning
pd.options.mode.chained_assignment = None

def compare_annual_performance(ticker_symbol, index_fund="VTSAX"):
    def get_annual_returns(symbol):
        # Get the current date
        end_date = dt.date.today()
        # Get the date from 10 years ago
        start_date = end_date - dt.timedelta(days=10*365.25)
        
        # Fetch data
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)
        
        # Calculate annual returns
        return data['Close'].resample('A').ffill().pct_change().dropna() * 100, data

    def calculate_cagr(data):
        start_value = data['Close'].iloc[0]
        end_value = data['Close'].iloc[-1]
        years = len(data['Close'].resample('A').max())
        cagr = ((end_value / start_value) ** (1/years)) - 1
        return cagr * 100

    # Get annual returns and full data for index_fund and the given ticker symbol
    index_fund_returns, index_fund_data = get_annual_returns(index_fund)
    symbol_returns, symbol_data = get_annual_returns(ticker_symbol)

    # Calculate CAGR for index_fund and the ticker symbol
    index_fund_cagr = calculate_cagr(index_fund_data)
    symbol_cagr = calculate_cagr(symbol_data)

    # Calculate average annual performance
    avg_index_fund_return = index_fund_returns.mean()
    avg_symbol_return = symbol_returns.mean()

    # Display the comparison
    print('#############################')
    for year in range(index_fund_returns.index[0].year, index_fund_returns.index[-1].year + 1):
        index_fund_val = index_fund_returns[index_fund_returns.index.year == year].values
        symbol_val = symbol_returns[symbol_returns.index.year == year].values
        
        if index_fund_val.size > 0 and symbol_val.size > 0:
            print(f"Annual performance in {year}: {index_fund} = {index_fund_val[0]:.2f}% | {ticker_symbol} = {symbol_val[0]:.2f}%")
        elif index_fund_val.size > 0:
            print(f"Annual performance in {year}: {index_fund} = {index_fund_val[0]:.2f}% | {ticker_symbol} data not available")
        elif symbol_val.size > 0:
            print(f"Annual performance in {year}: {index_fund} data not available | {ticker_symbol} = {symbol_val[0]:.2f}%")

    # Print average annual performance
    print("\nAverage Annual Performance over 10 years:")
    print(f"{index_fund}: {avg_index_fund_return:.2f}%")
    print(f"{ticker_symbol}: {avg_symbol_return:.2f}%")

    # Print CAGR
    print("\nCompound Annual Growth Rate (CAGR) over 10 years:")
    print(f"{index_fund}: {index_fund_cagr:.2f}%")
    print(f"{ticker_symbol}: {symbol_cagr:.2f}%")

def roic_growth_rate(ticker_symbol):
    # Fetch data
    stock = yf.Ticker(ticker_symbol)
    financials = stock.financials.transpose()
    balancesheet = stock.balance_sheet.transpose()

    # Calculate NOPAT
    operating_income = financials['Operating Revenue']
    tax_rate = financials['Tax Provision'] / financials['Pretax Income']
    nopat = operating_income * (1 - tax_rate)

    # Calculate Invested Capital
    total_assets = balancesheet['Total Assets']
    current_liabilities = 0
    if 'Current Liabilities' in balancesheet.columns:
        current_liabilities = balancesheet['Current Liabilities']
    long_term_debt = balancesheet.get('Long Term Debt', 0)
    # If short-term debt info is available, fetch it, else set to 0
    short_term_debt = balancesheet.get('Short Term Debt', 0)
    invested_capital = total_assets - current_liabilities + (long_term_debt - short_term_debt)

    # Calculate ROIC
    roic = (nopat * 100 ) / invested_capital

    # Display ROIC for the last ten years (or as much data as available)
    print('#############################')
    for date, roic_value in roic.head(10).iloc[::-1].items():
        year = date.year
        print(f"ROIC for {ticker_symbol} in {year}: {roic_value:.2f}%")

def equity_growth_rates(ticker_symbol):
    # Fetch data
    stock = yf.Ticker(ticker_symbol)
    balancesheet = stock.balance_sheet.transpose()

    # Extract Total Equity for the available years
    total_equity = balancesheet['Stockholders Equity']

    growth_rates = {}

    # Calculate the Equity Growth Rate for each year based on the previous year's equity
    # Start from the last entry and iterate to the first
    for i in range(len(total_equity) - 1, 0, -1):
        year = str(total_equity.index[i-1].year)
        prev_year = str(total_equity.index[i].year)
        
        start_equity = total_equity.iloc[i]
        end_equity = total_equity.iloc[i-1]
        
        if start_equity == 0:  # Avoid division by zero
            growth_rate = float('inf')  # Infinite growth if the starting equity was 0
        else:
            growth_rate = ((end_equity/start_equity) - 1) * 100  # As a percentage
            
        growth_rates[f"{prev_year} to {year}"] = growth_rate
        
    return growth_rates


def eps_growth_rate(ticker_symbol):
    # Fetch data
    stock = yf.Ticker(ticker_symbol)
    print(stock.info)
    earnings_data =  stock.earnings_growth
    print(earnings_data)
    
    # Check if sufficient data is available
    if len(earnings_data) < 2:
        print("Insufficient data available.")
        return None
    
    growth_rates = {}
    
    for i in range(len(earnings_data)-1):
        start_year = earnings_data.index[i]
        end_year = earnings_data.index[i+1]
        start_eps = earnings_data["Earnings Per Share"].iloc[i]
        end_eps = earnings_data["Earnings Per Share"].iloc[i+1]
        
        growth = ((end_eps/start_eps) - 1) * 100
        growth_rates[f"{start_year} to {end_year}"] = growth
    
    return growth_rates


def sales_growth_rate(ticker_symbol):
    """
    Calculate the sales growth rate for a given ticker symbol for each available year.
    
    Parameters:
    - ticker_symbol (str): The stock ticker symbol.
    
    Returns:
    - dict: A dictionary with years as keys and growth rates as values.
    """
    stock = yf.Ticker(ticker_symbol)
    financials = stock.financials

    # Fetching the revenues (sales) data
    revenues = financials.loc["Total Revenue"]

    growth_rates = {}
    
    # Start from the second last data point and iterate backwards
    for i in range(len(revenues) - 1, 0, -1):
        initial_value = revenues.iloc[i]   # The previous year's revenue
        final_value = revenues.iloc[i - 1] # The current year's revenue
        
        growth_rate = ((final_value - initial_value) / initial_value) * 100
        year = revenues.index[i - 1].year
        growth_rates[year] = growth_rate

    return growth_rates


def free_cash_flow_growth_rate(ticker_symbol):
    """
    Calculate the free cash flow growth rate for a given ticker symbol for each available year.
    
    Parameters:
    - ticker_symbol (str): The stock ticker symbol.
    
    Returns:
    - dict: A dictionary with years as keys and growth rates as values.
    """
    stock = yf.Ticker(ticker_symbol)
    cashflow = stock.cashflow
    #print(cashflow.info)

    # Fetching the Operating Cash Flow and Capital Expenditures data
    op_cashflow = cashflow.loc["Operating Cash Flow"]
    cap_expenditures = cashflow.loc["Capital Expenditure"]

    # Calculate Free Cash Flow
    free_cash_flow = op_cashflow + cap_expenditures  # Note: Capital Expenditures are usually negative

    growth_rates = {}
    
    # Start from the second last data point and iterate backwards
    for i in range(len(free_cash_flow) - 1, 0, -1):
        initial_value = free_cash_flow.iloc[i]   # The previous year's FCF
        final_value = free_cash_flow.iloc[i - 1] # The current year's FCF
        
        growth_rate = ((final_value - initial_value) / initial_value) * 100
        year = free_cash_flow.index[i - 1].year
        growth_rates[year] = growth_rate

    return growth_rates


def display_pe_ratios(ticker_symbol):
    try:
        # Fetch data for the ticker
        stock = yf.Ticker(ticker_symbol)
        
        # Get today's date and fetch historical data for today
        # today = dt.date.today()
        # data = stock.history(start=today, end=today + dt.timedelta(days=1))
        # print(data)
        # Use the closing price (latest available price) for today as the current stock price
        current_stock_price = get_current_stock_price(ticker_symbol)
        
        # Fetch the trailing earnings per share (EPS)
        # trailing_eps = stock.info.get('trailingEps', None)
    
        # # Fetch the forward earnings per share (EPS)
        # forward_eps = stock.info.get('forwardEps', None)
    
        # # Calculate and display the trailing PE ratio
        # if trailing_eps and trailing_eps != 0:  # Check for valid and non-zero EPS
        #     trailing_pe_ratio = current_stock_price / trailing_eps
        #     print(f"Trailing PE Ratio for {ticker_symbol}: {trailing_pe_ratio:.2f}")
        # else:
        #     print(f"Trailing Earnings Per Share data not available or zero for {ticker_symbol}. Cannot compute PE ratio.")
            
        # # Calculate and display the forward PE ratio
        # if forward_eps and forward_eps != 0:  # Check for valid and non-zero EPS
        #     forward_pe_ratio = current_stock_price / forward_eps
        #     print(f"Forward PE Ratio for {ticker_symbol}: {forward_pe_ratio:.2f}")
        # else:
        #     print(f"Forward Earnings Per Share data not available or zero for {ticker_symbol}. Cannot compute PE ratio.")
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol} in display_pe_ratios method : {e}")


def get_current_stock_price(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    
    # Get today's date
    today = dt.date.today()
    
    # Fetch historical data for today
    data = stock.history(start=today, end=today + dt.timedelta(days=1))
    
    # Return the closing price (latest available price) for today
    return data['Close'].iloc[0]


def fetch_share_volume_data(ticker_symbol):
    try:
        # Fetch data for the ticker
        stock = yf.Ticker(ticker_symbol)
        
        # Fetch the latest volume of shares traded
        latest_volume = stock.info.get('volume', None)
        
        # Fetch the average volume of shares traded
        average_volume = stock.info.get('averageVolume', None)
        
        if latest_volume is None or average_volume is None:
            raise Exception("Unable to fetch volume data")
        
        return latest_volume, average_volume
    except Exception as e:
        print(f"Error fetching volume data for {ticker_symbol}: {e}")
        return None, None


def get_shares_outstanding(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    return stock.info['sharesOutstanding']


def get_current_market_cap(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    return stock.info['marketCap']


def calculate_market_cap_at_price(ticker_symbol, interested_to_buy='Y'):
    print(f"Current market price of {ticker_symbol}: ${get_current_stock_price(ticker_symbol):.2f}")
    # Print current market cap
    market_cap_current = get_current_market_cap(ticker_symbol)
    print(f"Current market cap of {ticker_symbol}: ${market_cap_current:.2f}")
    
    if interested_to_buy == 'Y':
        # Get the share price the user is interested in
        share_price = float(input(f"Enter the share price you are interested in for {ticker_symbol}: "))
        
        # Calculate market cap based on given share price and outstanding shares
        shares = get_shares_outstanding(ticker_symbol)
        market_cap_interested = share_price * shares
        
        print(f"At a share price of ${share_price:.2f}, the market cap of {ticker_symbol} would be ${market_cap_interested:.2f}")

ticker_symbol = 'AAPL'  # For Apple Inc. as an example

compare_annual_performance(ticker_symbol)

roic_growth_rate(ticker_symbol)

egr_dict = equity_growth_rates(ticker_symbol)

print('#############################')
for period, egr in egr_dict.items():
    # Extract the latter year from the 'year to year' format
    current_year = period.split(" to ")[1]
    print(f"Equity Growth Rate for {ticker_symbol} from {int(current_year)-1} to {current_year}: {egr:.2f}%")

print('#############################')
print('Missing Earnings Growth Rate')
# egr = eps_growth_rate(ticker_symbol)
# for period, growth in egr.items():
#     print(f"EPS Growth Rate for {ticker_symbol} from {period}: {growth:.2f}%")

print('#############################')
sgr_dict = sales_growth_rate(ticker_symbol)
for year, sgr in sgr_dict.items():
    print(f"Sales Growth Rate for {ticker_symbol} in {year}: {sgr:.2f}%")

print('#############################')
fcfgr_dict = free_cash_flow_growth_rate(ticker_symbol)
for year, fcfgr in fcfgr_dict.items():
    print(f"Free Cash Flow Growth Rate for {ticker_symbol} in {year}: {fcfgr:.2f}%")

print('#############################')
display_pe_ratios(ticker_symbol)

print('#############################')
latest_volume, average_volume = fetch_share_volume_data(ticker_symbol)
print(f"Latest Volume for {ticker_symbol}: {latest_volume:,}")
print(f"Average Volume for {ticker_symbol}: {average_volume:,}")
shares = get_shares_outstanding(ticker_symbol)
print(f"Total number of shares issued by {ticker_symbol}: {shares}")

print('#############################')
calculate_market_cap_at_price(ticker_symbol)             # Will ask for share price and show both market caps
#calculate_market_cap_at_price(ticker_symbol, 'N')       # Will only show the current market cap