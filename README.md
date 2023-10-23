# Stock Analysis Tool

This tool provides various functionalities to analyze the financial data of a stock using its ticker symbol. It fetches the data using the `yfinance` library and performs multiple calculations to extract key financial metrics.

## Features

1. **ROIC (Return On Invested Capital) Growth Rate**: This function calculates the ROIC for a given stock and displays the growth rates for the last ten years (or as much data as available).
2. **Equity Growth Rates**: This function calculates the Equity Growth Rate for a stock for each year based on the previous year's equity.
3. **EPS (Earnings Per Share) Growth Rate**: This function calculates the growth rate of Earnings Per Share for a given stock.
4. **Sales Growth Rate**: It calculates the growth rate of sales for a stock for each available year.
5. **Free Cash Flow Growth Rate**: This function determines the growth rate of Free Cash Flow for a stock for each available year.
6. **P/E Ratios**: It displays both the Trailing and Forward Price-to-Earnings ratio for a given stock.
7. **Market Capitalization**: It calculates the market capitalization for a stock.
8. **Share Volume Data**: Fetches the latest volume and the average volume of shares traded for a stock.

## Dependencies

- `yfinance`: To fetch stock data.
- `pandas`: For data manipulation.

## Usage

Firstly, you need to install the required packages:

```bash
pip install yfinance pandas

Then, you can run the tool by executing the script. Before running, you may want to change the `ticker_symbol` in the code to the stock ticker of your choice. For example, the given code uses 'CEIX' as the ticker symbol.

```bash
python <script_name>.py
```

Replace `<script_name>` with the name you've given to the script.

## Output
The output will display various financial metrics calculated for the chosen stock, providing insights into its financial health and performance.

## Note
Ensure you have an active internet connection, as the tool fetches real-time data from Yahoo Finance.
