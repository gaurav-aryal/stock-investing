import yfinance as yf
import pandas as pd

# Disable pandas warning
pd.options.mode.chained_assignment = None

def roic_growth_rate(ticker_symbol):
    
    # Fetch data
    stock = yf.Ticker(ticker_symbol)
    financials = stock.financials.transpose()
    balancesheet = stock.balance_sheet.transpose()

    # Calculate NOPAT
    operating_income = financials['Operating Income']
    tax_rate = financials['Tax Provision'] / financials['Pretax Income']
    nopat = operating_income * (1 - tax_rate)

    # Calculate Invested Capital
    total_assets = balancesheet['Total Assets']
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
    # Fetch data for the ticker
    stock = yf.Ticker(ticker_symbol)
    
    # Fetch the current stock price
    current_stock_price = stock.info['currentPrice']
    
    # Fetch the trailing earnings per share (EPS)
    trailing_eps = stock.info['trailingEps']

    # Fetch the forward earnings per share (EPS)
    forward_eps = stock.info['forwardEps']

    # Calculate and display the trailing PE ratio
    if trailing_eps and trailing_eps != 0:  # Check for valid and non-zero EPS
        trailing_pe_ratio = current_stock_price / trailing_eps
        print(f"Trailing PE Ratio for {ticker_symbol}: {trailing_pe_ratio:.2f}")
    else:
        print(f"Trailing Earnings Per Share data not available or zero for {ticker_symbol}. Cannot compute PE ratio.")
        
    # Calculate and display the forward PE ratio
    if forward_eps and forward_eps != 0:  # Check for valid and non-zero EPS
        forward_pe_ratio = current_stock_price / forward_eps
        print(f"Forward PE Ratio for {ticker_symbol}: {forward_pe_ratio:.2f}")
    else:
        print(f"Forward Earnings Per Share data not available or zero for {ticker_symbol}. Cannot compute PE ratio.")

def calculate_market_cap(ticker_symbol):
    # Fetch data for the ticker
    stock = yf.Ticker(ticker_symbol)
    
    # Fetch the current stock price
    current_stock_price = stock.info['currentPrice']
    
    # Fetch the number of outstanding shares
    outstanding_shares = stock.info['sharesOutstanding']

    # Calculate the market cap
    market_cap = current_stock_price * outstanding_shares
    
    return market_cap

def fetch_share_volume_data(ticker_symbol):
    # Fetch data for the ticker
    stock = yf.Ticker(ticker_symbol)
    
    # Fetch the latest volume of shares traded
    latest_volume = stock.info['volume']
    
    # Fetch the average volume of shares traded
    average_volume = stock.info['averageVolume']

    return latest_volume, average_volume

ticker_symbol = 'CEIX'  # For Apple Inc. as an example
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
market_cap = calculate_market_cap(ticker_symbol)
print(f"Market Capitalization for {ticker_symbol}: ${market_cap:,.2f}")

print('#############################')
latest_volume, average_volume = fetch_share_volume_data(ticker_symbol)
print(f"Latest Volume for {ticker_symbol}: {latest_volume:,}")
print(f"Average Volume for {ticker_symbol}: {average_volume:,}")