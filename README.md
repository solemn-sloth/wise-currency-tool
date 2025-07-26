# Wise Currency Tool

A command-line tool for interacting with Wise's exchange rate API. This tool allows you to easily retrieve currency exchange rates, historical data, and currency information through a simple interface.

## Features

- Get current exchange rates between any two currencies
- Retrieve multiple exchange rates for a specific currency
- Access historical exchange rates with date range support
- List all available currencies supported by Wise
- Interactive mode for easy exploration
- Command-line mode for scripting and automation

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/solemn-sloth/wise-currency-tool.git
   cd wise-currency-tool
   ```

2. Make the script executable (if needed):
   ```
   chmod +x wise_exchange_rates.py
   ```

3. No additional dependencies required - uses only standard Python libraries.

## Usage

### Interactive Mode

Simply run the script without arguments to enter interactive mode:

```
./wise_exchange_rates.py
```

This provides a menu-based interface to:
- Get exchange rates between specific currencies
- View multiple rates for a source or target currency
- Access historical rates
- List all available currencies

### Command-line Mode

#### Get Current Exchange Rate

```
./wise_exchange_rates.py rate USD EUR
```

#### Get Historical Exchange Rate

```
./wise_exchange_rates.py rate USD EUR --date 2023-01-15
```

#### Get Multiple Exchange Rates From a Currency

```
./wise_exchange_rates.py rates --source USD --limit 20
```

#### Get Multiple Exchange Rates To a Currency

```
./wise_exchange_rates.py rates --target EUR --limit 15
```

#### Get Historical Rates Between Dates

```
./wise_exchange_rates.py history USD EUR --start 2023-01-01 --end 2023-01-31
```

#### List All Available Currencies

```
./wise_exchange_rates.py currencies
```

## Date Formats

The tool accepts dates in various formats:
- YYYY-MM-DD (e.g., 2023-01-15)
- YYYY-MM-DDTHH:MM:SS (e.g., 2023-01-15T14:30:00)
- DD/MM/YYYY (e.g., 15/01/2023)
- MM/DD/YYYY (e.g., 01/15/2023)
- YYYYMMDD (e.g., 20230115)

## Example Output

```
USD/EUR Exchange Rate:

1 USD = 0.937258 EUR
1 EUR = 1.067171 USD

Rate timestamp: 2023-08-01T12:00:00Z
```
