import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import datetime as dt
from pprint import pprint
import textwrap

# Disable pandas warning
pd.options.mode.chained_assignment = None

class StockAnalysis:
    _dcf_has_run = False

    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.stock = yf.Ticker(ticker_symbol)
        
        # Initialize growth rate variables
        self.avg_roic_growth = None
        self.avg_equity_growth = None
        self.avg_earnings_growth = None
        self.avg_sales_growth = None
        self.avg_fcf_growth = None
        # Initialize attributes
        self.trailing_earnings_yield = 0
        self.forward_earnings_yield = 0
        self.dividend_yield = 0
        self.breakeven_price = 0

        # Calculate and store dividend yield at initialization
        current_price = self.stock.info.get('currentPrice', 0)
        dividend_rate = self.stock.info.get('dividendRate', 0)
        self.dividend_yield = (dividend_rate / current_price * 100) if dividend_rate and current_price else 0

    def display_stock_info(self) -> None:
        """
        Displays basic information about the stock such as name, industry, sector, employees, location, market information, and risk metrics.

        Args:
            None

        Returns:
            None
        """
        try:
            print("\n=== Company Information ===")
            
            # Basic Company Info
            print("\n=== Basic Details ===")
            print(f"{'Metric':<25} | {'Value'}")
            print("-" * 50)
            print(f"{'Company Name':<25} | {self.stock.info.get('longName', 'N/A'):}")
            print(f"{'Industry':<25} | {self.stock.info.get('industry', 'N/A'):}")
            print(f"{'Sector':<25} | {self.stock.info.get('sector', 'N/A'):}")
            print(f"{'Employees':<25} | {self.stock.info.get('fullTimeEmployees', 'N/A'):,}")
            
            # Location Info
            print("\n=== Location ===")
            print(f"{'Metric':<25} | {'Value'}")
            print("-" * 50)
            print(f"{'Address':<25} | {self.stock.info.get('address1', 'N/A'):}")
            if self.stock.info.get('address2'):
                print(f"{'Address (cont.)':<25} | {self.stock.info.get('address2', 'N/A'):}")
            print(f"{'City':<25} | {self.stock.info.get('city', 'N/A'):}")
            print(f"{'State':<25} | {self.stock.info.get('state', 'N/A'):}")
            print(f"{'Country':<25} | {self.stock.info.get('country', 'N/A'):}")
            
            # Market Info
            print("\n=== Market Information ===")
            print(f"{'Metric':<25} | {'Value'}")
            print("-" * 50)
            print(f"{'Market Cap':<25} | ${self.stock.info.get('marketCap', 0):,.2f}")
            print(f"{'Beta':<25} | {self.stock.info.get('beta', 'N/A'):}")
            print(f"{'Forward P/E':<25} | {self.stock.info.get('forwardPE', 'N/A'):}")
            print(f"{'Trailing P/E':<25} | {self.stock.info.get('trailingPE', 'N/A'):}")
            print(f"{'Dividend Yield':<25} | {(self.stock.info.get('dividendYield', 0) * 100):.2f}%")
            
            # Risk Metrics
            if any(key in self.stock.info for key in ['overallRisk', 'auditRisk', 'boardRisk', 'compensationRisk']):
                print("\n=== Risk Metrics (1-10 scale) ===")
                print(f"{'Metric':<25} | {'Value'}")
                print("-" * 50)
                print(f"{'Overall Risk':<25} | {self.stock.info.get('overallRisk', 'N/A'):}")
                print(f"{'Audit Risk':<25} | {self.stock.info.get('auditRisk', 'N/A'):}")
                print(f"{'Board Risk':<25} | {self.stock.info.get('boardRisk', 'N/A'):}")
                print(f"{'Compensation Risk':<25} | {self.stock.info.get('compensationRisk', 'N/A'):}")
            
            # Business Summary
            if self.stock.info.get('longBusinessSummary'):
                print("\n=== Business Summary ===")
                print(textwrap.fill(self.stock.info['longBusinessSummary'], width=80))
        
        except Exception as e:
            print(f"Error displaying stock information: {e}")

    def remind_fundamental_principle(self):
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + f"{'INVESTMENT FUNDAMENTALS CHECKLIST':^78}" + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")

        print("\n=== 1. Business Understanding ===")
        print("□ Do you understand how the business makes money?")
        print("□ Can you explain the business model to a 10-year-old?")
        print("□ Does the business have a sustainable competitive advantage?")
        print("□ Is the business model proven and profitable?")

        print("\n=== 2. Financial Health ===")
        print("□ Does the company have strong cash flows?")
        print("□ Is the balance sheet healthy with manageable debt?")
        print("□ Has the company shown consistent revenue growth?")
        print("□ Are profit margins stable or improving?")

        print("\n=== 3. Management Quality ===")
        print("□ Is management transparent and trustworthy?")
        print("□ Do they have a track record of good capital allocation?")
        print("□ Are management's interests aligned with shareholders?")
        print("□ How long has the current management team been in place?")

        print("\n=== 4. Competitive Position ===")
        print("□ What are the barriers to entry in this industry?")
        print("□ How strong is the company's market position?")
        print("□ Who are the main competitors and how do they compare?")
        print("□ Does the company have pricing power?")

        print("\n=== 5. Risk Assessment ===")
        print("□ What could go wrong with this investment?")
        print("□ Are you prepared for a 50% drop in value?")
        print("□ Is this investment within your circle of competence?")
        print("□ Have you considered regulatory and market risks?")

        print("\n=== 6. Valuation ===")
        print("□ Is the current price reasonable relative to earnings?")
        print("□ What's your margin of safety?")
        print("□ What's the realistic worst-case scenario?")
        print("□ What's your expected return over 5-10 years?")

        print("\n=== 7. Warren Buffett's Key Principles ===")
        print("• Never lose money (protect your downside first)")
        print("• Think like an owner, not a trader")
        print("• Buy wonderful businesses at fair prices")
        print("• Your best investment is often in your circle of competence")

        print("\n=== 8. Red Flags to Watch For ===")
        print("⚠ Complex business models you don't understand")
        print("⚠ Excessive debt or poor cash flow")
        print("⚠ Management with questionable track record")
        print("⚠ Unrealistic growth projections")
        print("⚠ Over-reliance on a single customer or supplier")

        print("\n=== 9. Final Questions ===")
        print("□ Would you be comfortable holding this for 10 years?")
        print("□ Would you invest 20% of your net worth in this?")
        print("□ Would you recommend this investment to your family?")
        print("□ Are you investing or speculating?")

        print("\nRemember: The goal is to find great businesses at reasonable prices,")
        print("not to make quick profits. Take your time and do thorough research.")
    
    def compare_annual_performance(self):
        try:
            print("\n=== Year-by-Year Performance ===")
            
            # Get historical data for SPY and VTI
            spy = yf.download('SPY', start='2000-01-01', end=None)['Adj Close']
            vti = yf.download('VTI', start='2000-01-01', end=None)['Adj Close']
            stock = yf.download(self.ticker_symbol, start='2000-01-01', end=None)['Adj Close']
            
            # Calculate annual returns
            spy_annual = spy.resample('Y').last().pct_change()
            vti_annual = vti.resample('Y').last().pct_change()
            stock_annual = stock.resample('Y').last().pct_change()
            
            # Create DataFrame with all returns
            df = pd.DataFrame({
                'SPY': spy_annual,
                'VTI': vti_annual,
                self.ticker_symbol: stock_annual
            })
            
            # Drop any rows where all values are NaN
            df = df.dropna(how='all')
            
            # Print the comparison table
            print("Year   | SPY          | VTI          | {:<12} | vs SPY     | vs VTI".format(self.ticker_symbol))
            print("-" * 75)
            
            for year in df.index:
                spy_return = df.loc[year, 'SPY']
                vti_return = df.loc[year, 'VTI']
                stock_return = df.loc[year, self.ticker_symbol]
                
                # Calculate differences
                vs_spy = stock_return - spy_return if not pd.isna(spy_return) else None
                vs_vti = stock_return - vti_return if not pd.isna(vti_return) else None
                
                # Format the output
                year_str = str(year.year)
                spy_str = f"{spy_return:+.2%}" if not pd.isna(spy_return) else "N/A"
                vti_str = f"{vti_return:+.2%}" if not pd.isna(vti_return) else "N/A"
                stock_str = f"{stock_return:+.2%}" if not pd.isna(stock_return) else "N/A"
                vs_spy_str = f"{vs_spy:+.2%}" if vs_spy is not None else "N/A"
                vs_vti_str = f"{vs_vti:+.2%}" if vs_vti is not None else "N/A"
                
                print(f"{year_str} | {spy_str:12} | {vti_str:12} | {stock_str:12} | {vs_spy_str:10} | {vs_vti_str:10}")
            
            # Calculate and print average annual returns
            avg_spy = df['SPY'].mean()
            avg_vti = df['VTI'].mean()
            avg_stock = df[self.ticker_symbol].mean()
            
            print("\n=== Average Annual Returns ===")
            print(f"SPY: {avg_spy:+.2%}")
            print(f"VTI: {avg_vti:+.2%}")
            print(f"{self.ticker_symbol}: {avg_stock:+.2%}")
            print(f"vs SPY: {(avg_stock - avg_spy):+.2%}")
            print(f"vs VTI: {(avg_stock - avg_vti):+.2%}")
            
            # Calculate CAGR
            def calculate_cagr(returns):
                # Filter out NaN values
                returns = returns.dropna()
                if len(returns) < 2:
                    return None
                
                # Calculate cumulative return
                cum_return = (1 + returns).prod()
                # Calculate number of years
                years = len(returns)
                # Calculate CAGR
                cagr = (cum_return ** (1/years)) - 1
                return cagr
            
            cagr_spy = calculate_cagr(df['SPY'])
            cagr_vti = calculate_cagr(df['VTI'])
            cagr_stock = calculate_cagr(df[self.ticker_symbol])
            
            print("\n=== Compound Annual Growth Rate (CAGR) ===")
            print(f"SPY CAGR: {cagr_spy:+.2%}")
            print(f"VTI CAGR: {cagr_vti:+.2%}")
            print(f"{self.ticker_symbol} CAGR: {cagr_stock:+.2%}")
            print(f"vs SPY CAGR: {(cagr_stock - cagr_spy):+.2%}")
            print(f"vs VTI CAGR: {(cagr_stock - cagr_vti):+.2%}")
            
            print("\nNote: CAGR represents the geometric mean annual return,")
            print("which accounts for the compounding effect of returns")
            print("and is typically a better measure of long-term performance")
            print("than simple average returns.")
            
        except Exception as e:
            print(f"\nError in performance comparison: {str(e)}")

    def interpret_growth_rate(self, growth_rate, metric_name):
        try:
            # Remove the print statements for the header and growth rate
            # Only print the interpretation
            if growth_rate > 15:
                print(f"• {metric_name} shows STRONG growth")
                print("• Company is expanding rapidly in this metric")
            elif growth_rate > 10:
                print(f"• {metric_name} shows GOOD growth")
                print("• Company is growing steadily")
            elif growth_rate > 5:
                print(f"• {metric_name} shows MODERATE growth")
                print("• Company is growing at a sustainable pace")
            elif growth_rate > 0:
                print(f"• {metric_name} shows SLOW growth")
                print("• Company might be in a mature phase or facing challenges")
            else:
                print(f"• {metric_name} shows NEGATIVE growth")
                print("• Company might be facing significant challenges")
        except Exception as e:
            print(f"Error in growth rate interpretation: {e}")

    def analyze_roic(self):
        try:
            # Retrieve financial data
            financials = self.stock.get_financials()
            balance_sheet = self.stock.get_balance_sheet()

            if financials.empty or balance_sheet.empty:
                print("\nNo financial data available.")
                self.avg_roic_growth = None
                return None

            roic_values = {}
            growth_rates = []
            calculation_details = {}

            # Calculate ROIC for each year
            for date in financials.columns:
                try:
                    year = date.year
                    operating_income = float(financials.loc['OperatingIncome', date])
                    tax_rate = float(financials.loc['TaxRateForCalcs', date])
                    nopat = operating_income * (1 - tax_rate)

                    total_assets = float(balance_sheet.loc['TotalAssets', date])
                    current_liabilities = float(balance_sheet.loc['CurrentLiabilities', date])
                    cash = float(balance_sheet.loc['CashAndCashEquivalents', date])

                    # Calculate invested capital
                    invested_capital = total_assets - current_liabilities - cash

                    if invested_capital != 0:
                        roic = (nopat / invested_capital) * 100
                        roic_values[year] = roic
                        calculation_details[year] = {
                            'operating_income': operating_income,
                            'tax_rate': tax_rate,
                            'nopat': nopat,
                            'total_assets': total_assets,
                            'current_liabilities': current_liabilities,
                            'cash': cash,
                            'invested_capital': invested_capital,
                            'roic': roic,
                        }
                    else:
                        print(f"Debug: Skipped year {year} due to zero invested capital.")
                except Exception as e:
                    print(f"Debug: Error calculating ROIC for {date}: {str(e)}")
                    continue

            if not roic_values:
                print("\nNo valid ROIC data found for any year.")
                self.avg_roic_growth = None
                return None

            # Print ROIC values with growth rates
            print("\n{:<6} | {:>10} | {:>12} | {:>20}".format("Year", "ROIC (%)", "Growth Rate", "Calculation"))
            print("-" * 55)

            sorted_years = sorted(roic_values.keys())
            for i, year in enumerate(sorted_years):
                if i == 0:
                    growth_str = "Base Year"
                    calc_str = "See below"
                else:
                    prev_year = sorted_years[i - 1]
                    prev_roic = roic_values[prev_year]
                    curr_roic = roic_values[year]

                    growth_rate = curr_roic - prev_roic  # ROIC growth in percentage points
                    growth_rates.append(growth_rate)
                    growth_str = f"{growth_rate:+.2f}%"
                    calc_str = "See below"

                print("{:<6} | {:>10.2f} | {:>12} | {:>20}".format(
                    year,
                    roic_values[year],
                    growth_str,
                    calc_str
                ))

            # Print detailed calculations
            print("\n=== Detailed ROIC Calculations ===")
            print("Growth Rate = (Current Year ROIC - Previous Year ROIC)")
            print("ROIC = (NOPAT / Invested Capital) × 100")
            print("NOPAT = Operating Income × (1 - Tax Rate)")
            print("Invested Capital = Total Assets - Current Liabilities - Cash")
            
            for i, year in enumerate(sorted_years):
                details = calculation_details[year]
                print(f"\nYear {year}:")
                print(f"  Operating Income: ${details['operating_income']:,.0f}")
                print(f"  Tax Rate: {details['tax_rate']:.2%}")
                print(f"  NOPAT: ${details['nopat']:,.0f}")
                print(f"  Total Assets: ${details['total_assets']:,.0f}")
                print(f"  Current Liabilities: ${details['current_liabilities']:,.0f}")
                print(f"  Cash: ${details['cash']:,.0f}")
                print(f"  Invested Capital: ${details['invested_capital']:,.0f}")
                print(f"  ROIC: {details['roic']:.2f}%")
                
                if i > 0:
                    prev_year = sorted_years[i-1]
                    prev_details = calculation_details[prev_year]
                    print(f"\nGrowth Rate Calculation:")
                    print(f"Previous Year ({prev_year}) ROIC: {prev_details['roic']:.2f}%")
                    print(f"Current Year ({year}) ROIC: {details['roic']:.2f}%")
                    print(f"Change in ROIC: {(details['roic'] - prev_details['roic']):+.2f}%")

            # Calculate and store average growth rate
            if growth_rates:
                self.avg_roic_growth = sum(growth_rates) / len(growth_rates)
                print(f"\nAverage ROIC Growth Rate: {self.avg_roic_growth:.2f}%")
            else:
                self.avg_roic_growth = None
                print("\nInsufficient data to calculate average ROIC growth rate.")

            print("\nGrowth Rate Explanation:")
            print("- ROIC growth rates show the change in Return on Invested Capital over years.")
            print("- Positive rates indicate improved capital efficiency.")
            print("- Negative rates indicate reduced capital efficiency.")
            print("- Invested capital excludes current liabilities and cash.")

            return roic_values

        except Exception as e:
            print(f"\nError in ROIC calculation: {str(e)}")
            self.avg_roic_growth = None
            return None

    def analyze_equity_growth(self):
        try:
            # Get balance sheet data
            balance_sheet = self.stock.balance_sheet
            if balance_sheet.empty:
                print("\nNo balance sheet data available.")
                self.avg_equity_growth = None
                return None
            
            equity_values = {}
            growth_rates = []
            calculation_details = {}
            
            # Calculate equity for each year
            for date in balance_sheet.columns:
                try:
                    year = date.year
                    # Try different possible column names for stockholders' equity
                    possible_names = ['Stockholders Equity', 'StockholdersEquity', 'Total Equity Gross Minority Interest', 'Common Stock Equity']
                    equity_value = None
                    
                    for name in possible_names:
                        if name in balance_sheet.index:
                            equity_value = float(balance_sheet.loc[name, date])
                            break
                    
                    if equity_value is None or pd.isna(equity_value):
                        continue
                    
                    equity_values[year] = equity_value
                    calculation_details[year] = {
                        'stockholders_equity': equity_value
                    }
                except Exception as e:
                    continue
            
            if not equity_values:
                print("\nNo valid equity data found for any year.")
                self.avg_equity_growth = None
                return None
            
            # Print equity values with growth rates
            print("\n{:<6} | {:>15} | {:>12} | {:>20}".format("Year", "Equity", "Growth Rate", "Calculation"))
            print("-" * 65)
            
            sorted_years = sorted(equity_values.keys())
            for i, year in enumerate(sorted_years):
                if i == 0:
                    growth_str = "Base Year"
                    calc_str = "N/A"
                else:
                    prev_year = sorted_years[i-1]
                    prev_equity = equity_values[prev_year]
                    curr_equity = equity_values[year]
                    
                    if prev_equity != 0:
                        growth_rate = ((curr_equity - prev_equity) / abs(prev_equity)) * 100
                        growth_rates.append(growth_rate)
                        growth_str = f"{growth_rate:+.2f}%"
                        calc_str = f"({curr_equity:,.0f} - {prev_equity:,.0f}) / {abs(prev_equity):,.0f}"
                    else:
                        growth_str = "N/A"
                        calc_str = "prev equity = 0"
                
                print("{:<6} | ${:>14,.0f} | {:>12} | {:>20}".format(
                    year,
                    equity_values[year],
                    growth_str,
                    "See below"
                ))
            
            # Print detailed calculations
            print("\n=== Detailed Equity Growth Calculations ===")
            print("Growth Rate = ((Current Year Equity - Previous Year Equity) / |Previous Year Equity|) × 100")
            
            for i, year in enumerate(sorted_years):
                details = calculation_details[year]
                print(f"\nYear {year}:")
                print(f"Stockholders' Equity: ${details['stockholders_equity']:,.0f}")
                
                if i > 0:
                    prev_year = sorted_years[i-1]
                    prev_equity = equity_values[prev_year]
                    curr_equity = equity_values[year]
                    
                    if prev_equity != 0:
                        growth_rate = ((curr_equity - prev_equity) / abs(prev_equity)) * 100
                        print(f"\nGrowth Rate Calculation:")
                        print(f"Previous Year ({prev_year}) Equity: ${prev_equity:,.0f}")
                        print(f"Current Year ({year}) Equity: ${curr_equity:,.0f}")
                        print(f"Change in Equity: ${(curr_equity - prev_equity):+,.0f}")
                        print(f"Growth Rate: (${curr_equity:,.0f} - ${prev_equity:,.0f}) / ${abs(prev_equity):,.0f} × 100 = {growth_rate:+.2f}%")
            
            # Calculate and store average growth rate
            if growth_rates:
                self.avg_equity_growth = self.calculate_average_growth(growth_rates)
                print(f"\nAverage Equity Growth Rate: {self.avg_equity_growth:.2f}%")
            else:
                self.avg_equity_growth = None
                print("\nInsufficient data to calculate average equity growth rate")
            
            print("\nGrowth Rate Explanation:")
            print("- Growth rates show percentage change in Stockholders' Equity")
            print("- Positive rates indicate increase in equity")
            print("- Negative rates indicate decrease in equity")
            print("- Using absolute value in denominator to handle negative equity values properly")
            
            return equity_values
            
        except Exception as e:
            print(f"\nError in equity growth calculation: {str(e)}")
            self.avg_equity_growth = None
            return None

    def calculate_average_growth(self, growth_rates):
        # Filter out nan values before calculating average
        valid_rates = [rate for rate in growth_rates if not pd.isna(rate)]
        if valid_rates:
            return sum(valid_rates) / len(valid_rates)
        return None

    def eps_growth_rate(self):
        try:
            print("\n=== Earnings Growth Analysis ===")
            
            # Get financial data
            financials = self.stock.get_financials()
            
            eps_values = {}
            growth_rates = []
            calculation_details = {}
            
            # Calculate EPS for each year
            for date in financials.columns:
                try:
                    year = date.year
                    net_income = float(financials.loc['NetIncome', date])
                    shares = float(financials.loc['DilutedAverageShares', date])
                    
                    if shares != 0:
                        eps = net_income / shares
                        eps_values[year] = eps
                        
                        # Store calculation details
                        calculation_details[year] = {
                            'net_income': net_income,
                            'shares': shares,
                            'eps': eps
                        }
                except Exception as e:
                    print(f"Skipping {year} due to missing or invalid data")
                    continue
            
            # Print EPS values with growth rates
            print("\n{:<6} | {:>15} | {:>12} | {:>20}".format("Year", "EPS", "Growth Rate", "Calculation"))
            print("-" * 65)
            
            sorted_years = sorted(eps_values.keys())
            for i, year in enumerate(sorted_years):
                if i == 0:
                    growth_str = "Base Year"
                    calc_str = "N/A"
                else:
                    prev_year = sorted_years[i-1]
                    prev_eps = eps_values[prev_year]
                    curr_eps = eps_values[year]
                    
                    if prev_eps != 0:
                        growth_rate = ((curr_eps - prev_eps) / abs(prev_eps)) * 100
                        growth_rates.append(growth_rate)
                        growth_str = f"{growth_rate:+.2f}%"
                        calc_str = f"({curr_eps:.2f} - {prev_eps:.2f}) / {abs(prev_eps):.2f}"
                    else:
                        growth_str = "N/A"
                        calc_str = "prev EPS = 0"
                
                print("{:<6} | ${:>14,.2f} | {:>12} | {:>20}".format(
                    year,
                    eps_values[year],
                    growth_str,
                    "See below"
                ))
            
            # Print detailed calculations
            print("\n=== Detailed Earnings Growth Calculations ===")
            print("EPS = Net Income / Diluted Average Shares")
            print("Growth Rate = ((Current Year EPS - Previous Year EPS) / |Previous Year EPS|) × 100")
            
            for i, year in enumerate(sorted_years):
                details = calculation_details[year]
                print(f"\nYear {year}:")
                print(f"Net Income: ${details['net_income']:,.0f}")
                print(f"Diluted Average Shares: {details['shares']:,.0f}")
                print(f"EPS Calculation: ${details['net_income']:,.0f} / {details['shares']:,.0f} = ${details['eps']:.2f}")
                
                if i > 0:
                    prev_year = sorted_years[i-1]
                    prev_eps = eps_values[prev_year]
                    curr_eps = eps_values[year]
                    
                    if prev_eps != 0:
                        growth_rate = ((curr_eps - prev_eps) / abs(prev_eps)) * 100
                        print(f"\nGrowth Rate Calculation:")
                        print(f"Previous Year ({prev_year}) EPS: ${prev_eps:.2f}")
                        print(f"Current Year ({year}) EPS: ${curr_eps:.2f}")
                        print(f"Change in EPS: ${(curr_eps - prev_eps):+.2f}")
                        print(f"Growth Rate: (${curr_eps:.2f} - ${prev_eps:.2f}) / ${abs(prev_eps):.2f} × 100 = {growth_rate:+.2f}%")
            
            # Calculate and store average growth rate
            if growth_rates:
                self.avg_earnings_growth = self.calculate_average_growth(growth_rates)
                print(f"\nAverage Earnings Growth Rate: {self.avg_earnings_growth:.2f}%")
            else:
                self.avg_earnings_growth = None
                print("\nUnable to calculate average earnings growth rate")
            
            print("\nGrowth Rate Explanation:")
            print("- Growth rates show percentage change in Earnings Per Share (EPS)")
            print("- Positive rates indicate increase in earnings")
            print("- Negative rates indicate decrease in earnings")
            print("- Using absolute value in denominator to handle negative EPS values properly")
            
            return eps_values
            
        except Exception as e:
            print(f"\nError in EPS growth calculation: {str(e)}")
            self.avg_earnings_growth = None
            return None

    def sales_growth_rate(self):
        try:
            print("\n=== Sales Growth Analysis ===")
            
            # Get income statement data
            income_stmt = self.stock.get_income_stmt()
            
            sales_values = {}
            growth_rates = []
            calculation_details = {}
            
            # Calculate sales for each year
            for date in income_stmt.columns:
                try:
                    year = date.year
                    revenue = float(income_stmt.loc['TotalRevenue', date])
                    sales_values[year] = revenue
                    
                    # Store calculation details
                    calculation_details[year] = {
                        'total_revenue': revenue
                    }
                except Exception as e:
                    print(f"Skipping {year} due to missing or invalid data")
                    continue
            
            # Print sales values with growth rates
            print("\n{:<6} | {:>15} | {:>12} | {:>20}".format("Year", "Revenue", "Growth Rate", "Calculation"))
            print("-" * 65)
            
            sorted_years = sorted(sales_values.keys())
            for i, year in enumerate(sorted_years):
                if i == 0:
                    growth_str = "Base Year"
                    calc_str = "N/A"
                else:
                    prev_year = sorted_years[i-1]
                    prev_sales = sales_values[prev_year]
                    curr_sales = sales_values[year]
                    
                    if prev_sales != 0:
                        growth_rate = ((curr_sales - prev_sales) / abs(prev_sales)) * 100
                        growth_rates.append(growth_rate)
                        growth_str = f"{growth_rate:+.2f}%"
                        calc_str = f"({curr_sales:,.0f} - {prev_sales:,.0f}) / {abs(prev_sales):,.0f}"
                    else:
                        growth_str = "N/A"
                        calc_str = "prev sales = 0"
            
                print("{:<6} | ${:>14,.0f} | {:>12} | {:>20}".format(
                    year,
                    sales_values[year],
                    growth_str,
                    "See below"
                ))
            
            # Print detailed calculations
            print("\n=== Detailed Sales Growth Calculations ===")
            print("Growth Rate = ((Current Year Revenue - Previous Year Revenue) / |Previous Year Revenue|) × 100")
            
            for i, year in enumerate(sorted_years):
                details = calculation_details[year]
                print(f"\nYear {year}:")
                print(f"Total Revenue: ${details['total_revenue']:,.0f}")
                
                if i > 0:
                    prev_year = sorted_years[i-1]
                    prev_sales = sales_values[prev_year]
                    curr_sales = sales_values[year]
                    
                    if prev_sales != 0:
                        growth_rate = ((curr_sales - prev_sales) / abs(prev_sales)) * 100
                        print(f"\nGrowth Rate Calculation:")
                        print(f"Previous Year ({prev_year}) Revenue: ${prev_sales:,.0f}")
                        print(f"Current Year ({year}) Revenue: ${curr_sales:,.0f}")
                        print(f"Change in Revenue: ${(curr_sales - prev_sales):+,.0f}")
                        print(f"Growth Rate: (${curr_sales:,.0f} - ${prev_sales:,.0f}) / ${abs(prev_sales):,.0f} × 100 = {growth_rate:+.2f}%")
            
            # Calculate and store average growth rate
            if growth_rates:
                self.avg_sales_growth = self.calculate_average_growth(growth_rates)
                print(f"\nAverage Sales Growth Rate: {self.avg_sales_growth:.2f}%")
            else:
                self.avg_sales_growth = None
                print("\nUnable to calculate average sales growth rate")
            
            print("\nGrowth Rate Explanation:")
            print("- Growth rates show percentage change in Total Revenue")
            print("- Positive rates indicate increase in sales")
            print("- Negative rates indicate decrease in sales")
            print("- Using absolute value in denominator to handle negative revenue values properly")
            
            return sales_values
            
        except Exception as e:
            print(f"\nError in sales growth calculation: {str(e)}")
            self.avg_sales_growth = None
            return None

    def free_cash_flow_growth_rate(self):
        try:
            print("\n=== Free Cash Flow Growth Analysis ===")
            
            # Get cash flow data
            cash_flow = self.stock.cashflow
            
            fcf_values = {}
            growth_rates = []
            calculation_details = {}
            
            # Calculate FCF for each year
            for date in cash_flow.columns:
                try:
                    year = date.year
                    operating_cf = float(cash_flow.loc['Operating Cash Flow', date])
                    capital_exp = float(cash_flow.loc['Capital Expenditure', date])
                    # Corrected FCF formula: OCF - |CapEx|
                    fcf = operating_cf - abs(capital_exp)  # Take absolute value of CapEx since it's negative
                    fcf_values[year] = fcf
                    
                    # Store calculation details
                    calculation_details[year] = {
                        'operating_cash_flow': operating_cf,
                        'capital_expenditure': capital_exp,
                        'free_cash_flow': fcf
                    }
                except Exception as e:
                    print(f"Skipping {year} due to missing or invalid data")
                    continue
            
            # Print FCF values with growth rates
            print("\n{:<6} | {:>15} | {:>12} | {:>20}".format("Year", "FCF", "Growth Rate", "Calculation"))
            print("-" * 65)
            
            sorted_years = sorted(fcf_values.keys())
            for i, year in enumerate(sorted_years):
                if i == 0:
                    growth_str = "Base Year"
                    calc_str = "N/A"
                else:
                    prev_year = sorted_years[i-1]
                    prev_fcf = fcf_values[prev_year]
                    curr_fcf = fcf_values[year]
                    
                    if prev_fcf != 0:
                        growth_rate = ((curr_fcf - prev_fcf) / abs(prev_fcf)) * 100
                        growth_rates.append(growth_rate)
                        growth_str = f"{growth_rate:+.2f}%"
                        calc_str = f"({curr_fcf:,.0f} - {prev_fcf:,.0f}) / {abs(prev_fcf):,.0f}"
                    else:
                        growth_str = "N/A"
                        calc_str = "prev FCF = 0"
            
                print("{:<6} | ${:>14,.0f} | {:>12} | {:>20}".format(
                    year,
                    fcf_values[year],
                    growth_str,
                    "See below"
                ))
            
            # Print detailed calculations
            print("\n=== Detailed Free Cash Flow Calculations ===")
            print("FCF = Operating Cash Flow - |Capital Expenditure|")
            print("Note: We take the absolute value of Capital Expenditure since it's typically reported as a negative number")
            print("Growth Rate = ((Current Year FCF - Previous Year FCF) / |Previous Year FCF|) × 100")
            
            for i, year in enumerate(sorted_years):
                details = calculation_details[year]
                print(f"\nYear {year}:")
                print(f"Operating Cash Flow: ${details['operating_cash_flow']:,.0f}")
                print(f"Capital Expenditure: ${details['capital_expenditure']:,.0f}")
                print(f"Free Cash Flow Calculation: ${details['operating_cash_flow']:,.0f} - |${details['capital_expenditure']:,.0f}| = ${details['free_cash_flow']:,.0f}")
                
                if i > 0:
                    prev_year = sorted_years[i-1]
                    prev_fcf = fcf_values[prev_year]
                    curr_fcf = fcf_values[year]
                    
                    if prev_fcf != 0:
                        growth_rate = ((curr_fcf - prev_fcf) / abs(prev_fcf)) * 100
                        print(f"\nGrowth Rate Calculation:")
                        print(f"Previous Year ({prev_year}) FCF: ${prev_fcf:,.0f}")
                        print(f"Current Year ({year}) FCF: ${curr_fcf:,.0f}")
                        print(f"Change in FCF: ${(curr_fcf - prev_fcf):+,.0f}")
                        print(f"Growth Rate: (${curr_fcf:,.0f} - ${prev_fcf:,.0f}) / ${abs(prev_fcf):,.0f} × 100 = {growth_rate:+.2f}%")
            
            # Calculate and store average growth rate
            if growth_rates:
                self.avg_fcf_growth = self.calculate_average_growth(growth_rates)
                print(f"\nAverage Free Cash Flow Growth Rate: {self.avg_fcf_growth:.2f}%")
            else:
                self.avg_fcf_growth = None
                print("\nUnable to calculate average FCF growth rate")
            
            print("\nGrowth Rate Explanation:")
            print("- Growth rates show percentage change in Free Cash Flow")
            print("- Positive rates indicate increase in FCF")
            print("- Negative rates indicate decrease in FCF")
            print("- Using absolute value in denominator to handle negative FCF values properly")
            print("- Capital Expenditure is typically negative, so it's subtracted from Operating Cash Flow")
            
            return fcf_values
            
        except Exception as e:
            print(f"\nError in FCF growth calculation: {str(e)}")
            self.avg_fcf_growth = None
            return None

    def calculate_dcf(self, years=10, growth_rate=0.05, discount_rate=0.12, terminal_growth=0.02):
        # Modified default values to match Buffett's conservative approach:
        # - 10 year projection (standard)
        # - 5% initial growth (conservative)
        # - 12% discount rate (includes risk premium)
        # - 2% terminal growth (around inflation)
        try:
            print("\n=== Key Formulas Used ===")
            print("1. Present Value = Future Cash Flow / (1 + Discount Rate)^Year")
            print("2. Future Cash Flow = Current FCF × (1 + Growth Rate)^Year")
            print("3. Terminal Value = Final Year FCF × (1 + Terminal Growth) / (Discount Rate - Terminal Growth)")
            print("4. Enterprise Value = Sum of Present Values + PV of Terminal Value")
            print("5. Fair Value per Share = Enterprise Value / Shares Outstanding")
            print("6. Margin of Safety = (Fair Value - Current Price) / Fair Value × 100")
            
            if not StockAnalysis._dcf_has_run:
                StockAnalysis._dcf_has_run = True
                use_default = input("\nDo you want to use default values for DCF analysis? (Y/N): ").strip()
                if use_default.upper() == "N" or use_default == "y":
                    try:
                        self.dcf_years = int(input("\nEnter number of years for projection (default 10): ") or "10")
                        # Convert percentage inputs to decimals
                        growth_input = float(input("Enter expected growth rate % (default 5): ") or "5")
                        self.dcf_growth = growth_input / 100
                        
                        discount_input = float(input("Enter discount rate % (default 12): ") or "12")
                        self.dcf_discount = discount_input / 100
                        
                        terminal_input = float(input("Enter terminal growth rate % (default 2): ") or "2")
                        self.dcf_terminal = terminal_input / 100
                    except ValueError as e:
                        print("\nInvalid input. Using default values.")
                        self.dcf_years = years
                        self.dcf_growth = growth_rate
                        self.dcf_discount = discount_rate
                        self.dcf_terminal = terminal_growth
                else:
                    self.dcf_years = years
                    self.dcf_growth = growth_rate
                    self.dcf_discount = discount_rate
                    self.dcf_terminal = terminal_growth

            print("\nUsing values:")
            print(f"Years: {self.dcf_years}")
            print(f"Growth Rate: {self.dcf_growth*100:.1f}%")
            print(f"Discount Rate: {self.dcf_discount*100:.1f}%")
            print(f"Terminal Growth: {self.dcf_terminal*100:.1f}%")

            # Use the stored parameters
            params = getattr(self, '_dcf_params', {
                'years': self.dcf_years,
                'growth_rate': self.dcf_growth,
                'discount_rate': self.dcf_discount,
                'terminal_growth': self.dcf_terminal
            })
            
            years = params['years']
            growth_rate = params['growth_rate']
            discount_rate = params['discount_rate']
            terminal_growth = params['terminal_growth']

            try:
                # Get the current free cash flow
                try:
                    cash_flow = self.stock.cashflow
                    if cash_flow.empty:
                        print("\nNo cash flow data available.")
                        return None
                    
                    # Get most recent FCF value
                    fcf = float(cash_flow.loc['Free Cash Flow'].iloc[0])
                    if pd.isna(fcf):
                        print("\nNo valid Free Cash Flow data available.")
                        return None
                    
                    print("\n=== DCF Calculation Details ===")
                    print(f"Starting Free Cash Flow: ${fcf:,.2f}")
                    
                    # Get current year
                    current_year = datetime.now().year
                    
                    # Calculate future cash flows and present values
                    future_cash_flows = []
                    present_values = []
                    
                    print("\nDetailed DCF Calculations:")
                    print(f"Initial Growth Rate (Years 1-5): {growth_rate*100:.1f}%")
                    print(f"Terminal Growth Rate (Years 6+): {terminal_growth*100:.1f}%")
                    print(f"Discount Rate: {discount_rate*100:.1f}%")
                    print("\nYear | Growth Rate | Future Cash Flow | Discount Factor | Present Value")
                    print("-" * 75)
                    
                    for year_offset in range(1, years + 1):
                        projection_year = current_year + year_offset
                        
                        # Calculate projected FCF
                        if year_offset <= 5:
                            fcf *= (1 + growth_rate)
                            growth_rate_used = growth_rate
                        else:
                            fcf *= (1 + terminal_growth)
                            growth_rate_used = terminal_growth
                        
                        future_cash_flows.append(fcf)
                        
                        # Calculate present value
                        discount_factor = 1 / ((1 + discount_rate) ** year_offset)
                        pv = fcf * discount_factor
                        present_values.append(pv)
                        
                        print(f"{projection_year:4d} | {growth_rate_used:>9.1%} | ${fcf:>14,.0f} | {discount_factor:>14.4f} | ${pv:>14,.0f}")
                    
                    # Calculate total present value
                    total_pv = sum(present_values)
                    print("-" * 75)
                    print(f"Total Present Value: ${total_pv:,.0f}")
                    
                    # Get shares outstanding
                    shares_outstanding = self.stock.info.get('sharesOutstanding', None)
                    if shares_outstanding is None:
                        print("\nNo shares outstanding data available.")
                        return None
                    
                    print(f"Shares Outstanding: {shares_outstanding:,.0f}")
                    
                    # Calculate fair value per share
                    fair_value = total_pv / shares_outstanding
                    current_price = self.stock.info.get('currentPrice', None)
                    
                    if current_price is None:
                        print("\nNo current price data available.")
                        return None
                    
                    # Calculate margin of safety
                    margin_of_safety = ((fair_value - current_price) / fair_value) * 100
                    
                    # Print DCF Valuation Summary with better formatting
                    print("\n")
                    print("╔" + "═" * 70 + "╗")
                    print("║" + " DCF VALUATION SUMMARY ".center(70) + "║")
                    print("╠" + "═" * 70 + "╣")
                    print("║" + f" Enterprise Value:        ${total_pv:,.0f}".ljust(70) + "║")
                    print("║" + f" Shares Outstanding:      {shares_outstanding:,.0f}".ljust(70) + "║")
                    print("╟" + "─" * 70 + "╢")
                    print("║" + f" Fair Value per Share:    ${fair_value:,.2f}".ljust(70) + "║")
                    print("║" + f" Current Price:           ${current_price:,.2f}".ljust(70) + "║")
                    print("║" + f" Margin of Safety:        {margin_of_safety:,.1f}%".ljust(70) + "║")
                    print("╟" + "─" * 70 + "╢")
                    
                    # Add interpretation
                    if margin_of_safety > 0:
                        print("║" + f" VERDICT: Stock appears UNDERVALUED by {margin_of_safety:.1f}%".ljust(70) + "║")
                        print("║" + " SUGGESTION: Consider buying if assumptions are valid".ljust(70) + "║")
                    else:
                        print("║" + f" VERDICT: Stock appears OVERVALUED by {abs(margin_of_safety):.1f}%".ljust(70) + "║")
                        print("║" + " SUGGESTION: Caution warranted at current price".ljust(70) + "║")
                    print("╚" + "═" * 70 + "╝")

                    # Print assumptions in a separate box
                    print("\n")
                    print("┌" + "─" * 70 + "┐")
                    print("│" + " KEY ASSUMPTIONS ".center(70) + "│")
                    print("├" + "─" * 70 + "┤")
                    print("│" + f" Growth Rate (Years 1-5):    {growth_rate:.1%}".ljust(70) + "│")
                    print("│" + f" Terminal Growth (Years 6+): {terminal_growth:.1%}".ljust(70) + "│")
                    print("│" + f" Discount Rate:             {discount_rate:.1%}".ljust(70) + "│")
                    print("└" + "─" * 70 + "┘")
                    
                    print("\nNote: DCF results are highly sensitive to input assumptions.")
                    print("Consider running multiple scenarios with different growth rates.")
                    
                    return fair_value
                    
                except Exception as e:
                    print(f"\nError in cash flow calculations: {str(e)}")
                    return None
                
            except Exception as e:
                print(f"\nError in DCF calculation: {str(e)}")
                return None
            
        except Exception as e:
            print(f"\nError in DCF calculation: {str(e)}")
            return None
        
    def calculate_amzn_dcf(self, years=15, growth_rate=0.12, terminal_growth=0.02, discount_rate=0.08):
        try:
            print("\n")
            print("╔" + "═" * 78 + "╗")
            print("║" + " " * 78 + "║")
            print("║" + "AMAZON-STYLE DCF VALUATION".center(78) + "║")
            print("║" + "(Adjusted for High Growth & Investment)".center(78) + "║")
            print("║" + " " * 78 + "║")
            print("╚" + "═" * 78 + "╝")

            # Use the values from regular DCF if they exist
            if hasattr(self, 'dcf_years'):
                years = self.dcf_years
                growth_rate = self.dcf_growth
                discount_rate = self.dcf_discount
                terminal_growth = self.dcf_terminal

            print("\nUsing values:")
            print(f"Years: {years}")
            print(f"Growth Rate: {growth_rate*100:.1f}%")
            print(f"Discount Rate: {discount_rate*100:.1f}%")
            print(f"Terminal Growth: {terminal_growth*100:.1f}%")

            print("\n=== Key Formulas Used ===")
            print("1. Adjusted Free Cash Flow = Operating Cash Flow - Maintenance CapEx")
            print("2. Maintenance CapEx = 33% of Operating Cash Flow")
            print("3. Growth CapEx = 67% of Operating Cash Flow (excluded from FCF)")
            print("4. Present Value = Future Cash Flow / (1 + Discount Rate)^Year")
            print("5. Terminal Value = Final Year FCF × (1 + Terminal Growth) / (Discount Rate - Terminal Growth)")
            
            # Get cash flow data
            cash_flow = self.stock.cashflow
            if cash_flow.empty:
                print("\nNo cash flow data available.")
                return None

            # Get Operating Cash Flow
            operating_cash_flow = float(cash_flow.loc["Operating Cash Flow"].iloc[0])
            
            # Calculate CapEx split
            maintenance_capex = 0.33 * operating_cash_flow
            growth_capex = 0.67 * operating_cash_flow
            adjusted_fcf = operating_cash_flow - maintenance_capex

            print("\n=== Initial Cash Flow Analysis ===")
            print(f"Operating Cash Flow:      ${operating_cash_flow:,.0f}")
            print(f"Maintenance CapEx (33%):  ${maintenance_capex:,.0f}")
            print(f"Growth CapEx (67%):       ${growth_capex:,.0f}")
            print(f"Adjusted Free Cash Flow:  ${adjusted_fcf:,.0f}")

            # Project future cash flows
            print("\n=== Projected Cash Flows ===")
            print("╔" + "═" * 90 + "╗")
            print("║" + "Year".center(10) + "│" + 
                  "Growth".center(12) + "│" + 
                  "Projected FCF".center(20) + "│" + 
                  "Discount Factor".center(20) + "│" + 
                  "Present Value".center(25) + "║")
            print("╠" + "═" * 90 + "╣")

            future_cash_flows = []
            present_values = []
            
            for year in range(1, years + 1):
                # Use different growth rates for different periods
                if year <= 5:
                    growth_rate_used = growth_rate
                else:
                    growth_rate_used = terminal_growth
                
                adjusted_fcf *= (1 + growth_rate_used)
                discount_factor = 1 / ((1 + discount_rate) ** year)
                pv = adjusted_fcf * discount_factor
                
                future_cash_flows.append(adjusted_fcf)
                present_values.append(pv)
                
                print("║" + f"{year + 2023:^10}" + "│" + 
                      f"{growth_rate_used:>10.1%}" + "│" + 
                      f"${adjusted_fcf:>18,.0f}" + "│" + 
                      f"{discount_factor:>19.4f}" + "│" + 
                      f"${pv:>23,.0f}" + "║")

            print("╚" + "═" * 90 + "╝")

            # Calculate terminal value
            terminal_fcf = future_cash_flows[-1]
            # Check if terminal growth rate is less than discount rate
            if terminal_growth >= discount_rate:
                print("\nWarning: Terminal growth rate must be less than discount rate")
                print("Adjusting terminal growth rate to discount rate - 2%")
                terminal_growth = discount_rate - 0.02  # Set terminal growth 2% below discount rate
            
            # Terminal Value calculation using Gordon Growth Model
            terminal_value = terminal_fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
            terminal_value_pv = terminal_value / ((1 + discount_rate) ** years)

            # Add validation check
            if terminal_value < 0:
                print("\nWarning: Invalid terminal value calculation detected")
                print("Please check growth and discount rate assumptions")
                return None

            # Calculate total value
            total_pv = sum(present_values) + terminal_value_pv
            shares_outstanding = self.stock.info.get('sharesOutstanding', 0)
            fair_value = total_pv / shares_outstanding if shares_outstanding else 0
            current_price = self.stock.info.get('currentPrice', 0)
            
            print("\n=== Valuation Summary ===")
            print("╔" + "═" * 70 + "╗")
            print("║" + "FINAL VALUATION".center(70) + "║")
            print("╠" + "═" * 70 + "╣")
            print(f"║ Enterprise Value:        ${total_pv:,.0f}".ljust(71) + "║")
            print(f"║ Shares Outstanding:      {shares_outstanding:,.0f}".ljust(71) + "║")
            print(f"║ Fair Value per Share:    ${fair_value:.2f}".ljust(71) + "║")
            print(f"║ Current Price:           ${current_price:.2f}".ljust(71) + "║")
            margin_of_safety = ((fair_value - current_price) / fair_value) * 100
            print(f"║ Margin of Safety:        {margin_of_safety:,.1f}%".ljust(71) + "║")
            print("╚" + "═" * 70 + "╝")

            print("\n=== Key Assumptions Used ===")
            print("• Initial Growth Rate (Years 1-5): {:.1f}%".format(growth_rate * 100))
            print("• Terminal Growth Rate: {:.1f}%".format(terminal_growth * 100))
            print("• Discount Rate: {:.1f}%".format(discount_rate * 100))
            print("• Maintenance CapEx: 33% of Operating Cash Flow")
            print("• Growth CapEx: 67% of Operating Cash Flow (excluded)")
            
            print("\n=== Important Notes ===")
            print("1. This model adjusts for Amazon's high reinvestment strategy")
            print("2. Growth CapEx is excluded as it represents investment in future growth")
            print("3. Actual returns depend on successful conversion of investments")
            print("4. High growth assumptions reflect Amazon's reinvestment efficiency")

            return fair_value

        except Exception as e:
            print(f"\nError in DCF calculation: {e}")
            return None

    def get_bond_yield(self):
        try:
            # Try to get the 10-year Treasury yield
            treasury = yf.Ticker('^TNX')
            history = treasury.history(period='1d')
            if not history.empty:
                # ^TNX gives yield in percentage points (e.g., 4.5 for 4.5%)
                bond_yield = float(history['Close'].iloc[-1])
                if bond_yield > 0:
                    return bond_yield
            
            # Fallback to info method if history fails
            raw_yield = treasury.info.get('regularMarketPrice')
            if raw_yield and raw_yield > 0:
                return float(raw_yield)
            
            # Default value if both methods fail
            print("Warning: Using default 10-year Treasury yield of 4.0%")
            return 4.0
            
        except Exception as e:
            print(f"Error fetching Treasury yield: {e}")
            print("Using default 10-year Treasury yield of 4.0%")
            return 4.0

    def display_pe_and_earnings_yield(self):
        try:
            # Get stock metrics
            trailing_eps = self.stock.info.get('trailingEps', 0)
            forward_eps = self.stock.info.get('forwardEps', 0)
            current_price = self.stock.info.get('currentPrice', 0)
            dividend_rate = self.stock.info.get('dividendRate', 0)
            
            # Get bond yield using the new method
            bond_yield = self.get_bond_yield()
            
            # Calculate breakeven price
            if forward_eps and bond_yield:
                self.breakeven_price = forward_eps / (bond_yield/100)
            else:
                self.breakeven_price = 0
                print("Could not calculate breakeven price - missing data")
            
            # Calculate ratios
            trailing_pe = current_price / trailing_eps if trailing_eps else 0
            forward_pe = current_price / forward_eps if forward_eps else 0
            dividend_yield = (dividend_rate / current_price * 100) if current_price else 0
            trailing_earnings_yield = (trailing_eps / current_price) * 100 if current_price and trailing_eps else 0
            forward_earnings_yield = (forward_eps / current_price) * 100 if current_price and forward_eps else 0

            # Calculate earnings yields
            trailing_earnings_yield = (trailing_eps / current_price * 100) if current_price and trailing_eps else 0
            forward_earnings_yield = (forward_eps / current_price * 100) if current_price and forward_eps else 0
            
            # Print the formatted table
            print("\n")
            print("╔" + "═" * 70 + "╗")
            print("║" + "VALUATION METRICS SUMMARY".center(70) + "║")
            print("╠" + "═" * 70 + "╣")
            print("║" + "Metric".ljust(25) + "│" + "Value".center(12) + "│" + "Notes".ljust(31) + "║")
            print("╟" + "─" * 25 + "┼" + "─" * 12 + "┼" + "─" * 31 + "╢")
            
            # Print metrics in table
            print("║" + "Current Price".ljust(25) + "│" + f"$ {current_price:>9.2f}" + "│" + " Market Price".ljust(31) + "║")
            print("║" + "Trailing EPS".ljust(25) + "│" + f"$ {trailing_eps:>9.2f}" + "│" + " Based on past 12 months".ljust(31) + "║")
            print("║" + "Forward EPS".ljust(25) + "│" + f"$ {forward_eps:>9.2f}" + "│" + " Expected future EPS".ljust(31) + "║")
            print("║" + "Trailing PE".ljust(25) + "│" + f"{trailing_pe:>11.2f}" + "│" + " Price/Trailing EPS".ljust(31) + "║")
            print("║" + "Forward PE".ljust(25) + "│" + f"{forward_pe:>11.2f}" + "│" + " Price/Forward EPS".ljust(31) + "║")
            print("╟" + "─" * 25 + "┼" + "─" * 12 + "┼" + "─" * 31 + "╢")
            print("║" + "Trailing Earnings Yield".ljust(25) + "│" + f"{trailing_earnings_yield:>10.2f}%" + "│" + " (EPS/Price)*100".ljust(31) + "║")
            print("║" + "Forward Earnings Yield".ljust(25) + "│" + f"{forward_earnings_yield:>10.2f}%" + "│" + " (EPS/Price)*100".ljust(31) + "║")
            print("║" + "Dividend Yield".ljust(25) + "│" + f"{self.dividend_yield:>9.2f}%" + "│" + " (Dividend/Price)*100".ljust(31) + "║")
            print("╟" + "─" * 70 + "╢")
            print("║" + "Total Yield".ljust(25) + "│" + f"{(forward_earnings_yield + self.dividend_yield):>10.2f}%" + "│" + " Earnings Yield + Dividend Yield".ljust(31) + "║")
            print("║" + "Breakeven Price".ljust(25) + "│" + f"${self.breakeven_price:>9.2f}" + "│" + " At Bond Yield Rate".ljust(31) + "║")
            print("║" + "Current Price".ljust(25) + "│" + f"${current_price:>9.2f}" + "│" + f" {'OVER' if current_price > self.breakeven_price else 'UNDER'}VALUED".ljust(31) + "║")
            print("╚" + "═" * 70 + "╝")
            
        except Exception as e:
            print(f"\nError in PE and Earnings Yield calculation: {str(e)}")

    def get_margin_of_safety(self):
        try:
            print("\n")
            print("╔" + "═" * 58 + "╗")
            print("║" + " YIELD COMPARISON AND MARGIN OF SAFETY ".center(58) + "║")
            print("╚" + "═" * 58 + "╝")
            
            # Get bond yield using the new method
            self.bond_yield = self.get_bond_yield()
            
            # Calculate earnings yield using EPS/Price
            current_price = self.stock.info.get('currentPrice', 0)
            trailing_eps = self.stock.info.get('trailingEps', 0)
            earnings_yield = (trailing_eps / current_price * 100) if current_price and trailing_eps else 0
            
            # Get dividend yield
            dividend_yield = self.stock.info.get('dividendYield', 0)
            if dividend_yield:
                dividend_yield *= 100
            
            # Calculate total stock yield
            total_stock_yield = earnings_yield + dividend_yield
            margin_of_safety = total_stock_yield - self.bond_yield
            
            # Print Components Table
            print("\n=== Yield Components ===")
            print(f"{'Component':<30} | {'Value':<10}")
            print("-" * 43)
            print(f"{'Earnings Yield (EPS/Price)':<30} | {earnings_yield:>9.2f}%")  # Updated label
            print(f"{'Dividend Yield':<30} | {dividend_yield:>9.2f}%")
            print(f"{'Total Stock Yield':<30} | {total_stock_yield:>9.2f}%")
            print(f"{'Bond Yield':<30} | {self.bond_yield:>9.2f}%")
            print(f"{'Margin of Safety':<30} | {margin_of_safety:>9.2f}%")
            
            # Add interpretation
            print("\n=== Interpretation ===")
            if margin_of_safety > 0:
                print(f"• Stock yields {margin_of_safety:.2f}% more than the bond")
                if margin_of_safety > 5:
                    print("• STRONG margin of safety")
                elif margin_of_safety > 2:
                    print("• MODERATE margin of safety")
                else:
                    print("• MINIMAL margin of safety")
            else:
                print(f"• Stock yields {abs(margin_of_safety):.2f}% less than the bond")
                print("• Negative spread suggests potential overvaluation")
        
        except Exception as e:
            print(f"\nError calculating margin of safety: {e}")
            print("Please ensure bond yield and stock yields are properly calculated first")

    def get_current_market_cap(self):
        return self.stock.info['marketCap']

    def calculate_market_cap_at_price(self, interested_to_buy='Y'):
        try:
            # Get current price and shares outstanding
            current_price = self.stock.info.get('currentPrice')
            shares = self.stock.info.get('sharesOutstanding')
            
            # Calculate current market cap
            market_cap_current = current_price * shares
            
            # Get dividend rate and calculate yields
            dividend_rate = self.stock.info.get('dividendRate', 0)
            current_dividend_yield = (dividend_rate / current_price * 100) if dividend_rate and current_price else 0
            
            print("\n")
            print("╔" + "═" * 70 + "╗")
            print("║" + " MARKET CAP ANALYSIS ".center(70) + "║")
            print("╠" + "═" * 70 + "╣")
            print("║" + f" Current Price: ${current_price:,.2f}".center(70) + "║")
            print("╚" + "═" * 70 + "╝")
            
            if interested_to_buy.upper() in ['Y', '']:
                # Get the share price, use current price if no input
                share_price_input = input(f"\nEnter the share price you are interested in for {self.ticker_symbol}: ").strip()
                share_price = float(share_price_input) if share_price_input else current_price
                
                # Calculate market cap at interested price
                market_cap_interested = share_price * shares
                
                # Calculate target dividend yield based on same dividend_rate but new price
                target_dividend_yield = (dividend_rate / share_price * 100) if dividend_rate and share_price else 0
                
                # Calculate percentage changes
                price_change_pct = ((share_price - current_price) / current_price) * 100
                market_cap_change_pct = ((market_cap_interested - market_cap_current) / market_cap_current) * 100
                
                # Calculate PE ratios and yields at target price
                trailing_eps = self.stock.info.get('trailingEps', 0)
                target_pe_ratio = share_price / trailing_eps if trailing_eps else None
                current_pe_ratio = current_price / trailing_eps if trailing_eps else None
                
                # Calculate earnings yields using EPS/Price
                current_earnings_yield = (trailing_eps / current_price * 100) if current_price else 0
                target_earnings_yield = (trailing_eps / share_price * 100) if share_price else 0
                
                # Calculate total yields (earnings yield + constant dividend yield)
                current_total_yield = current_earnings_yield + current_dividend_yield
                target_total_yield = target_earnings_yield + current_dividend_yield  # Use current_dividend_yield
                
                # Get bond yield
                try:
                    bond = yf.Ticker('^TNX')
                    bond_info = bond.history(period='1d')
                    if not bond_info.empty:
                        bond_yield = float(bond_info['Close'].iloc[-1])
                    else:
                        print("Error: Could not retrieve bond yield data")
                        return
                except Exception as e:
                    print(f"Error fetching bond yield: {e}")
                    return
                
                # Calculate breakeven price where total yield equals bond yield
                # Total Yield = Earnings Yield + Dividend Yield = Bond Yield
                # (EPS/Price) + (Dividend/Price) = Bond Yield
                # (EPS + Dividend)/Price = Bond Yield
                # Price = (EPS + Dividend)/Bond Yield
                
                if trailing_eps and bond_yield:
                    annual_dividend = dividend_rate if dividend_rate else 0
                    breakeven_price = (trailing_eps + annual_dividend) / (bond_yield/100)
                else:
                    breakeven_price = 0
                
                # Calculate margin of safety at target price
                target_margin_of_safety = target_total_yield - bond_yield
                
                # Calculate yield spreads
                current_yield_spread = current_total_yield - bond_yield
                target_yield_spread = target_total_yield - bond_yield
                
                # Calculate margin of safety (% above/below breakeven price)
                current_margin_of_safety = ((breakeven_price - current_price) / breakeven_price * 100)
                target_margin_of_safety = ((breakeven_price - share_price) / breakeven_price * 100)
                
                # Print valuation metrics comparison
                print("\n")
                print("╔" + "═" * 70 + "╗")
                print("║" + " VALUATION METRICS COMPARISON ".center(70) + "║")
                print("╠" + "═" * 70 + "╣")
                print("║" + f" {'Metric':<25} │ {'Current':>10} │ {'At Target':>10} │ {'Change':>10}".ljust(70) + "║")
                print("╟" + "─" * 70 + "╢")
                print("║" + f" {'Price':<25} │ ${current_price:>9.2f} │ ${share_price:>9.2f} │ {(share_price - current_price):>8.2f} ({price_change_pct:+.1f}%)".ljust(70) + "║")
                print("║" + f" {'Market Cap':<25} │ ${market_cap_current/1e9:>9.1f}B │ ${market_cap_interested/1e9:>9.1f}B │ ${(market_cap_interested - market_cap_current)/1e9:>8.1f}B".ljust(70) + "║")
                print("╟" + "─" * 70 + "╢")
                print("║" + f" {'P/E Ratio':<25} │ {current_pe_ratio:>9.2f}x │ {target_pe_ratio:>9.2f}x │ {(target_pe_ratio - current_pe_ratio):>9.2f}x".ljust(70) + "║")
                print("║" + f" {'Earnings Yield':<25} │ {current_earnings_yield:>9.2f}% │ {target_earnings_yield:>9.2f}% │ {(target_earnings_yield - current_earnings_yield):>9.2f}%".ljust(70) + "║")
                print("║" + f" {'Dividend Yield':<25} │ {current_dividend_yield:>9.2f}% │ {target_dividend_yield:>9.2f}% │ {(target_dividend_yield - current_dividend_yield):>9.2f}%".ljust(70) + "║")
                print("║" + f" {'Total Yield':<25} │ {current_total_yield:>9.2f}% │ {target_total_yield:>9.2f}% │ {(target_total_yield - current_total_yield):>9.2f}%".ljust(70) + "║")
                print("║" + f" {'Bond Yield':<25} │ {bond_yield:>9.2f}% │ {bond_yield:>9.2f}% │ {0:>9.2f}%".ljust(70) + "║")
                print("║" + f" {'Yield Spread':<25} │ {current_yield_spread:>9.2f}% │ {target_yield_spread:>9.2f}% │ {(target_yield_spread - current_yield_spread):>9.2f}%".ljust(70) + "║")
                print("║" + f" {'Breakeven Price':<25} │ ${breakeven_price:>9.2f} │ ${breakeven_price:>9.2f} │ {0:>9.2f}".ljust(70) + "║")
                print("║" + f" {'Margin of Safety':<25} │ {current_margin_of_safety:>9.2f}% │ {target_margin_of_safety:>9.2f}% │ {(target_margin_of_safety - current_margin_of_safety):>9.2f}%".ljust(70) + "║")
                print("╚" + "═" * 70 + "╝")

                # Calculate price-based margin of safety
                price_margin_of_safety = ((breakeven_price - current_price) / breakeven_price * 100)
                target_price_margin = ((breakeven_price - share_price) / breakeven_price * 100)
                
                # Calculate yield-based margin of safety
                yield_margin_of_safety = current_total_yield - bond_yield
                target_yield_margin = target_total_yield - bond_yield
                
                print("║" + f" {'Breakeven Price':<25} │ ${breakeven_price:>9.2f} │ ${breakeven_price:>9.2f} │ {0:>9.2f}".ljust(70) + "║")
                print("║" + f" {'Price Margin of Safety':<25} │ {price_margin_of_safety:>9.2f}% │ {target_price_margin:>9.2f}% │ {(target_price_margin - price_margin_of_safety):>9.2f}%".ljust(70) + "║")
                print("║" + f" {'Yield Margin of Safety':<25} │ {yield_margin_of_safety:>9.2f}% │ {target_yield_margin:>9.2f}% │ {(target_yield_margin - yield_margin_of_safety):>9.2f}%".ljust(70) + "║")
                print("╚" + "═" * 70 + "╝")

        except Exception as e:
            print(f"\nError in market cap calculation: {str(e)}")

    def format_market_cap(self, cap):
        if cap >= 1e9:
            return f"${cap / 1e9:,.2f}B"
        else:
            return f"${cap:,.2f}"

    def get_finances_stock(self):
        financials = self.stock.get_financials()
        print(financials)

    def get_ebit_stock(self):
        try:
            print(f"\n=== EBIT Analysis: {self.ticker_symbol} ===")
            
            def format_ebit(value):
                if abs(value) >= 1e9:
                    return f"${value / 1e9:.2f}B"
                elif abs(value) >= 1e6:
                    return f"${value / 1e6:.2f}M"
                else:
                    return f"${value:.2f}"
            
            # Fetch financial data
            financials = self.stock.get_financials()
            if 'EBIT' not in financials.index:
                print("Error: EBIT data not available")
                print("Available metrics:", ', '.join(financials.index))
                return None
            
            ebit_series = financials.loc['EBIT']
            ebit_values = {}
            
            # Store EBIT values
            for i in range(len(ebit_series)):
                year = ebit_series.index[i].year
                ebit = ebit_series.iloc[i]
                ebit_values[year] = ebit
            
            # Print combined table
            print("\n=== EBIT Values and Growth ===")
            headers = ['Year', 'EBIT', 'Raw Value', 'YoY Change', 'Growth Rate', 'Status']
            col_widths = [6, 15, 20, 15, 15, 15]
            
            # Print headers
            header_row = " | ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers)))
            print(header_row)
            print("-" * (sum(col_widths) + 3 * (len(col_widths) - 1)))  # Account for " | " separators
            
            sorted_years = sorted(ebit_values.keys())
            total_growth_rate = 0
            growth_periods = 0
            
            for i, year in enumerate(sorted_years):
                ebit = ebit_values[year]
                
                if i == 0:
                    # First year - no growth rate to calculate
                    row = [
                        f"{year}",
                        format_ebit(ebit),
                        f"${ebit:,.2f}",
                        "N/A",
                        "Base Year",
                        "Initial Year"
                    ]
                else:
                    prev_year = sorted_years[i-1]
                    prev_ebit = ebit_values[prev_year]
                    change = ebit - prev_ebit
                    
                    if prev_ebit != 0:
                        growth_rate = ((ebit / prev_ebit) - 1) * 100
                        total_growth_rate += growth_rate
                        growth_periods += 1
                        status = "Improvement" if change > 0 else "Decline"
                        
                        row = [
                            f"{year}",
                            format_ebit(ebit),
                            f"${ebit:,.2f}",
                            format_ebit(change),
                            f"{growth_rate:>8.2f}%",
                            status
                        ]
                    else:
                        row = [
                            f"{year}",
                            format_ebit(ebit),
                            f"${ebit:,.2f}",
                            format_ebit(change),
                            "N/A",
                            "N/A"
                        ]
                
                # Print row with proper alignment
                print(" | ".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row))))
            
            # Calculate and display average growth rate
            if growth_periods > 0:
                avg_growth_rate = total_growth_rate / growth_periods
                print("\n=== EBIT Growth Rate Analysis ===")
                print(f"Average Annual Growth Rate: {avg_growth_rate:.2f}%")
                print("")
                self.interpret_growth_rate(avg_growth_rate, "EBIT")
            
            return ebit_values
            
        except Exception as e:
            print(f"\nError in EBIT analysis: {e}")
            return None

    def format_cashflow(self, value):
        if abs(value) >= 1e9:
            return f"{value / 1e9:.1f} billion"
        elif abs(value) >= 1e6:
            return f"{value / 1e6:.1f} million"
        else:
            return f"{value:.1f}"
    
    def get_free_cashflow(self):
        try:
            # Fetch cash flow statement
            cashflow = self.stock.cashflow
            if cashflow.empty:
                print(f"No cash flow data available for {self.ticker_symbol}.")
                return
            
            # Get free cash flow (FCF) from the cash flow statement
            fcf_series = cashflow.loc['Free Cash Flow']
            fcf_df = fcf_series.reset_index()
            fcf_df.columns = ['Date', 'Free Cash Flow']
            fcf_df['Free Cash Flow'] = fcf_df['Free Cash Flow'].apply(self.format_cashflow)
            
            print("Free Cash Flow:")
            print(fcf_df.to_string(index=False))
        
        except Exception as e:
            print(f"Error fetching data for {self.ticker_symbol} in get_free_cashflow method: {e}")

    def print_growth_metrics_summary(self):
        try:
            # Add the decorative header
            print("\n")
            print("╔" + "═" * 78 + "╗")
            print("║" + " " * 78 + "║")
            print("║" + f"{'GROWTH METRICS':^78}" + "║")
            print("║" + " " * 78 + "║")
            print("╚" + "═" * 78 + "╝")

            print("\n┌" + "─" * 70 + "┐")
            print("│" + " AVERAGE ANNUAL GROWTH RATES ".center(70) + "│")
            print("├" + "─" * 70 + "┤")
            
            def classify_growth(rate):
                if rate is None or pd.isna(rate):
                    return "NO DATA"
                elif rate > 15:
                    return "STRONG"
                elif rate > 10:
                    return "GOOD"
                elif rate > 5:
                    return "MODERATE"
                elif rate > 0:
                    return "SLOW"
                else:
                    return "NEGATIVE"
            
            # Get all the growth rates
            metrics = {
                'ROIC': getattr(self, 'avg_roic_growth', None),
                'Equity': getattr(self, 'avg_equity_growth', None),  # Use the calculated value from equity analysis
                'Earnings': getattr(self, 'avg_earnings_growth', None),  # Use the calculated value from EPS analysis
                'Sales': getattr(self, 'avg_sales_growth', None),  # Use the calculated value from sales analysis
                'Free Cash Flow': getattr(self, 'avg_fcf_growth', None)  # Use the calculated value from FCF analysis
            }
            
            valid_rates = []
            for metric, rate in metrics.items():
                if rate is not None and not pd.isna(rate):
                    classification = classify_growth(rate)
                    rate_str = f"{rate:>9.2f}%" if not pd.isna(rate) else "NO DATA"
                    print("│" + f" {metric:<20} │ {rate_str:^12} │ {classification:^20}".ljust(70) + "║")
                    valid_rates.append(rate)
                else:
                    print("│" + f" {metric:<20} │ {'NO DATA':^12} │ {'NO DATA':^20}".ljust(70) + "║")
            
            print("└" + "─" * 70 + "┘")
            
            # Calculate and print overall health
            if valid_rates:
                avg_overall = sum(valid_rates) / len(valid_rates)
                print("\n┌" + "─" * 70 + "┐")
                print("│" + " OVERALL GROWTH HEALTH ".center(70) + "│")
                print("├" + "─" * 70 + "┤")
                print("│" + f" Average Growth Rate: {avg_overall:>6.2f}%".ljust(70) + "│")
                
                health_msg = ""
                if avg_overall > 15:
                    health_msg = "EXCELLENT - Strong performance across metrics"
                elif avg_overall > 10:
                    health_msg = "STRONG - Good performance in most areas"
                elif avg_overall > 5:
                    health_msg = "MODERATE - Stable growth"
                elif avg_overall > 0:
                    health_msg = "MODEST - Slow but positive growth"
                else:
                    health_msg = "CONCERNING - Decline in multiple areas"
                
                print("│" + f" Overall Health: {health_msg}".ljust(70) + "│")
                print("└" + "─" * 70 + "┘")
            
        except Exception as e:
            print(f"Error in growth metrics summary: {str(e)}")

    def display_basic_info(self):
        try:
            print("\n")
            print("╔" + "═" * 70 + "╗")
            print("║" + " BASIC STOCK INFORMATION ".center(70) + "║")
            print("╠" + "═" * 70 + "╣")
            
            info = self.stock.info
            cash_flow = self.stock.cashflow
            
            # Shares Outstanding
            shares = info.get('sharesOutstanding', 0)
            print("║" + f" Shares Outstanding: {shares:,.0f}".ljust(70) + "║")
            
            # Market Cap
            market_cap = info.get('marketCap', 0)
            print("║" + f" Market Cap: ${market_cap/1e9:,.2f}B".ljust(70) + "║")
            
            # Current Price
            current_price = info.get('currentPrice', 0)
            print("║" + f" Current Price: ${current_price:,.2f}".ljust(70) + "║")
            
            print("╠" + "═" * 70 + "╣")
            print("║" + " CASH FLOW METRICS ".center(70) + "║")
            print("╠" + "═" * 70 + "╣")
            
            # Get the most recent year's data
            if not cash_flow.empty:
                recent_date = cash_flow.columns[0]
                
                # Capital Expenditure
                capex = cash_flow.loc['Capital Expenditure', recent_date]
                print("║" + f" Capital Expenditure (Recent): ${abs(capex)/1e6:,.2f}M".ljust(70) + "║")
                
                # Stock Based Compensation
                try:
                    stock_comp = cash_flow.loc['Stock Based Compensation', recent_date]
                    print("║" + f" Stock Based Compensation (Recent): ${stock_comp/1e6:,.2f}M".ljust(70) + "║")
                except:
                    print("║" + " Stock Based Compensation: Data not available".ljust(70) + "║")
                
                # Operating Cash Flow
                try:
                    op_cash_flow = cash_flow.loc['Operating Cash Flow', recent_date]
                    print("║" + f" Operating Cash Flow (Recent): ${op_cash_flow/1e6:,.2f}M".ljust(70) + "║")
                except:
                    print("║" + " Operating Cash Flow: Data not available".ljust(70) + "║")
                
                # Free Cash Flow
                try:
                    free_cash_flow = cash_flow.loc['Free Cash Flow', recent_date]
                    print("║" + f" Free Cash Flow (Recent): ${free_cash_flow/1e6:,.2f}M".ljust(70) + "║")
                except:
                    print("║" + " Free Cash Flow: Data not available".ljust(70) + "║")
            
            print("╚" + "═" * 70 + "╝")
            
            # Add interpretation box
            print("\n")
            print("┌" + "─" * 70 + "┐")
            print("│" + " KEY METRICS INTERPRETATION ".center(70) + "│")
            print("├" + "─" * 70 + "┤")
            
            # Stock Based Compensation as % of Operating Cash Flow
            if 'stock_comp' in locals() and 'op_cash_flow' in locals() and op_cash_flow != 0:
                sbc_percent = (stock_comp / op_cash_flow) * 100
                print("│" + f" SBC as % of Operating Cash Flow: {sbc_percent:.1f}%".ljust(70) + "│")
                if sbc_percent > 15:
                    print("│" + " • High stock-based compensation relative to cash flow".ljust(70) + "│")
                elif sbc_percent > 5:
                    print("│" + " • Moderate stock-based compensation".ljust(70) + "│")
                else:
                    print("│" + " • Conservative stock-based compensation".ljust(70) + "│")
            
            # CapEx as % of Operating Cash Flow
            if 'capex' in locals() and 'op_cash_flow' in locals() and op_cash_flow != 0:
                capex_percent = (abs(capex) / op_cash_flow) * 100
                print("│" + f" CapEx as % of Operating Cash Flow: {capex_percent:.1f}%".ljust(70) + "│")
                if capex_percent > 30:
                    print("│" + " • High capital intensity business".ljust(70) + "│")
                elif capex_percent > 15:
                    print("│" + " • Moderate capital requirements".ljust(70) + "│")
                else:
                    print("│" + " • Light capital requirements".ljust(70) + "│")
            
            print("└" + "─" * 70 + "┘")
            
        except Exception as e:
            print(f"\nError displaying basic information: {str(e)}")

    def analyze_profit_factors(self):
        try:
            # Get income statement data
            income_stmt = self.stock.income_stmt
            
            print("\n")
            print("╔" + "═" * 70 + "╗")
            print("║" + " PROFIT REDUCTION ANALYSIS ".center(70) + "║")
            print("╠" + "═" * 70 + "╣")
            
            # 1. Operating Costs
            print("║" + " 1. OPERATING COSTS ".ljust(70) + "║")
            print("╟" + "─" * 70 + "╢")
            print("║" + " • Cost of Revenue".ljust(70) + "║")
            print("║" + " • Operating Expenses".ljust(70) + "║")
            print("║" + " • Research & Development".ljust(70) + "║")
            print("║" + " • SG&A (Selling, General & Admin)".ljust(70) + "║")
            
            # 2. Financial Costs
            print("╟" + "─" * 70 + "╢")
            print("║" + " 2. FINANCIAL COSTS ".ljust(70) + "║")
            print("╟" + "─" * 70 + "╢")
            print("║" + " • Interest Expense".ljust(70) + "║")
            print("║" + " • Debt Service Costs".ljust(70) + "║")
            print("║" + " • Foreign Exchange Losses".ljust(70) + "║")
            
            # 3. Tax Expenses
            print("╟" + "─" * 70 + "╢")
            print("║" + " 3. TAX EXPENSES ".ljust(70) + "║")
            print("╟" + "─" * 70 + "╢")
            print("║" + " • Income Tax".ljust(70) + "║")
            print("║" + " • State & Local Taxes".ljust(70) + "║")
            print("║" + " • International Tax Obligations".ljust(70) + "║")
            
            # 4. Non-Cash Charges
            print("╟" + "─" * 70 + "╢")
            print("║" + " 4. NON-CASH CHARGES ".ljust(70) + "║")
            print("╟" + "─" * 70 + "╢")
            print("║" + " • Depreciation".ljust(70) + "║")
            print("║" + " • Amortization".ljust(70) + "║")
            print("║" + " • Stock-Based Compensation".ljust(70) + "║")
            
            # 5. One-Time Items
            print("╟" + "─" * 70 + "╢")
            print("║" + " 5. ONE-TIME ITEMS ".ljust(70) + "║")
            print("╟" + "─" * 70 + "╢")
            print("║" + " • Restructuring Costs".ljust(70) + "║")
            print("║" + " • Asset Write-downs".ljust(70) + "║")
            print("║" + " • Legal Settlements".ljust(70) + "║")
            
            # 6. Market Factors
            print("╟" + "─" * 70 + "╢")
            print("║" + " 6. MARKET FACTORS ".ljust(70) + "║")
            print("╟" + "─" * 70 + "╢")
            print("║" + " • Competition & Price Pressure".ljust(70) + "║")
            print("║" + " • Market Share Loss".ljust(70) + "║")
            print("║" + " • Industry Cyclicality".ljust(70) + "║")
            
            print("╚" + "═" * 70 + "╝")
            
        except Exception as e:
            print(f"\nError in profit factors analysis: {str(e)}")

# At the start of the script, add this function
def print_section_header(title):
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + f"{title:^78}" + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

def print_subsection_header(title):
    print("\n")
    print("┌" + "─" * 58 + "┐")
    print("│" + f"{title:^58}" + "│")
    print("└" + "─" * 58 + "┘")

# Then modify the main execution flow:
if __name__ == "__main__":
    print_section_header("STOCK ANALYSIS DASHBOARD")
    ticker_symbol = input("Enter the stock ticker symbol: ").upper()
    analysis = StockAnalysis(ticker_symbol)
    
    # Add Basic Info display at the start
    print_section_header("BASIC INFORMATION")
    analysis.display_basic_info()
    
    # 1. Basic Information
    print_section_header("BASIC INFORMATION")
    analysis.remind_fundamental_principle()
    analysis.display_stock_info()
    
    # 2. Performance Metrics
    print_section_header("PERFORMANCE METRICS")
    print_subsection_header("Annual Performance")
    analysis.compare_annual_performance()
    
    print_section_header("BUSINESS VALUATION METRICS")
    print_subsection_header("ROIC Analysis")
    roic_dict = analysis.analyze_roic()
    
    # 3. Growth Metrics
    #print_section_header("GROWTH METRICS")
    
    print_subsection_header("Equity Growth")
    equity_dict = analysis.analyze_equity_growth()
    
    print_subsection_header("Earnings Growth")
    earnings_dict = analysis.eps_growth_rate()
    
    print_subsection_header("Sales Growth")
    sales_dict = analysis.sales_growth_rate()
    
    print_subsection_header("Free Cash Flow Growth")
    fcf_dict = analysis.free_cash_flow_growth_rate()
    
    # Print Growth Metrics Summary
    analysis.print_growth_metrics_summary()
    
    # 4. Valuation Metrics
    print_section_header("VALUATION METRICS")
    print_subsection_header("PE and Earnings Yield")
    analysis.display_pe_and_earnings_yield()
    analysis.get_margin_of_safety()
    
    # 6. Financial Analysis
    print_section_header("FINANCIAL ANALYSIS")
    print_subsection_header("EBIT Analysis")
    analysis.get_ebit_stock()
    
    # Add Profit Factors Analysis before DCF Valuation
    print_section_header("PROFIT REDUCTION ANALYSIS")
    analysis.analyze_profit_factors()
    
    # 7. DCF Valuation
    print_section_header("DCF VALUATION")
    # Define default values
    DEFAULT_YEARS = 10
    DEFAULT_GROWTH_RATE = 5.0
    DEFAULT_DISCOUNT_RATE = 12.0
    DEFAULT_TERMINAL_GROWTH = 2.0
    
    default_values = ""

    if default_values == 'n':
        print("\nPlease enter your custom values:")
        print(f"(Default values: Years={DEFAULT_YEARS}, Growth={DEFAULT_GROWTH_RATE}%, Discount={DEFAULT_DISCOUNT_RATE}%, Terminal Growth={DEFAULT_TERMINAL_GROWTH}%)")
        
        years = int(input("Enter the number of years for projection [10]: ") or DEFAULT_YEARS)
        growth_rate = float(input("Enter the earnings growth rate % [5.0]: ") or DEFAULT_GROWTH_RATE)
        discount_rate = float(input("Enter the discount rate % [12.0]: ") or DEFAULT_DISCOUNT_RATE)
        terminal_growth = float(input("Enter the terminal growth rate % [2.0]: ") or DEFAULT_TERMINAL_GROWTH)
    else:
        years = DEFAULT_YEARS
        growth_rate = DEFAULT_GROWTH_RATE
        discount_rate = DEFAULT_DISCOUNT_RATE
        terminal_growth = DEFAULT_TERMINAL_GROWTH

    # Calculate DCF with chosen values - only call it once
    fair_price = analysis.calculate_dcf(years, growth_rate/100, discount_rate/100, terminal_growth/100)
    
    analysis.calculate_amzn_dcf(years, growth_rate/100, discount_rate/100, terminal_growth/100)

    # Add Market Cap Analysis here
    print_section_header("MARKET CAP ANALYSIS")
    analysis.calculate_market_cap_at_price()
    
    # Final Summary
    #print_section_header("ANALYSIS SUMMARY")
    # Add a summary of key metrics and recommendations here
