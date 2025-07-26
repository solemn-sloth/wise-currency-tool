#!/usr/bin/env python3
import requests
import json
import datetime
import argparse
import sys
from textwrap import dedent

class WiseCurrencyTool:
    def __init__(self):
        self.auth_token = "OGNhN2FlMjUtOTNjNS00MmFlLThhYjQtMzlkZTFlOTQzZDEwOjliN2UzNmZkLWRjYjgtNDEwZS1hYzc3LTQ5NGRmYmEyZGJjZA=="
        self.base_url = "https://api.wise.com/v1"
        self.headers = {
            "Authorization": f"Basic {self.auth_token}",
            "Content-Type": "application/json"
        }

    def get_all_currencies(self):
        """Fetch all available currencies from Wise API"""
        try:
            response = requests.get(f"{self.base_url}/currencies", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching currencies: {e}")
            return []

    def get_exchange_rate(self, source, target, date=None):
        """Get exchange rate between two currencies, optionally at a specific date"""
        params = {
            "source": source,
            "target": target
        }
        
        # Add time parameter if date is provided
        if date:
            params["time"] = date.isoformat()
            
        try:
            response = requests.get(f"{self.base_url}/rates", headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and data:
                return data[0]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    def get_multiple_rates(self, source=None, target=None, limit=10):
        """Get multiple exchange rates for a source or target currency"""
        params = {}
        if source:
            params["source"] = source
        if target:
            params["target"] = target
            
        try:
            response = requests.get(f"{self.base_url}/rates", headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Limit the number of results to display
            return data[:limit] if isinstance(data, list) else []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching rates: {e}")
            return []

    def get_historical_rates(self, source, target, start_date, end_date=None, interval="day"):
        """Get historical rates between two dates"""
        # Default end date to today if not specified
        if not end_date:
            end_date = datetime.datetime.now()
            
        params = {
            "source": source,
            "target": target,
            "from": start_date.isoformat(),
            "to": end_date.isoformat(),
            "group": interval  # May not work as intended, API capabilities unclear
        }
        
        try:
            response = requests.get(f"{self.base_url}/rates", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching historical rates: {e}")
            return []


def format_rate_output(rate_data):
    """Format a single exchange rate for display"""
    if not rate_data:
        return "No rate data available."
        
    source = rate_data.get("source", "")
    target = rate_data.get("target", "")
    rate = rate_data.get("rate", 0)
    time = rate_data.get("time", "")
    
    # Calculate reverse rate
    reverse_rate = 1 / rate if rate else 0
    
    output = f"""
    {source}/{target} Exchange Rate:
    
    1 {source} = {rate:.6f} {target}
    1 {target} = {reverse_rate:.6f} {source}
    
    Rate timestamp: {time}
    """
    return dedent(output)

def format_multiple_rates(rates_data, title=None):
    """Format multiple rates for display"""
    if not rates_data:
        return "No rates data available."
        
    if title:
        output = f"\n{title}\n{'-' * len(title)}\n\n"
    else:
        output = "\nExchange Rates:\n--------------\n\n"
        
    # Table header
    output += f"{'SOURCE':<8} {'TARGET':<8} {'RATE':<15} {'DATE':<25}\n"
    output += f"{'-' * 8:<8} {'-' * 8:<8} {'-' * 15:<15} {'-' * 25:<25}\n"
    
    # Table rows
    for rate in rates_data:
        source = rate.get("source", "")
        target = rate.get("target", "")
        rate_value = rate.get("rate", 0)
        time = rate.get("time", "")
        
        output += f"{source:<8} {target:<8} {rate_value:<15.6f} {time:<25}\n"
        
    return output


def parse_date(date_str):
    """Parse date string in various formats"""
    if not date_str:
        return None
        
    formats = [
        "%Y-%m-%d",           # 2023-01-15
        "%Y-%m-%dT%H:%M:%S",  # 2023-01-15T14:30:00
        "%d/%m/%Y",           # 15/01/2023
        "%m/%d/%Y",           # 01/15/2023
        "%Y%m%d"              # 20230115
    ]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
            
    print(f"Error: Could not parse date '{date_str}'.")
    print("Supported formats: YYYY-MM-DD, YYYY-MM-DDTHH:MM:SS, DD/MM/YYYY, MM/DD/YYYY, YYYYMMDD")
    return None


def interactive_mode():
    """Run the tool in interactive mode"""
    tool = WiseCurrencyTool()
    
    print("\n=== Wise Currency Tool - Interactive Mode ===\n")
    
    while True:
        print("\nChoose an option:")
        print("1. Get exchange rate between two currencies")
        print("2. Get multiple rates for a source currency")
        print("3. Get multiple rates for a target currency")
        print("4. Get historical rates between dates")
        print("5. List all available currencies")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            source = input("Enter source currency code (e.g., USD): ").strip().upper()
            target = input("Enter target currency code (e.g., EUR): ").strip().upper()
            
            date_str = input("Enter date (optional, press Enter for current rate): ").strip()
            date = parse_date(date_str) if date_str else None
            
            rate = tool.get_exchange_rate(source, target, date)
            print(format_rate_output(rate))
            
        elif choice == "2":
            source = input("Enter source currency code (e.g., USD): ").strip().upper()
            limit_str = input("Enter maximum number of results (default: 10): ").strip()
            limit = int(limit_str) if limit_str.isdigit() else 10
            
            rates = tool.get_multiple_rates(source=source, limit=limit)
            print(format_multiple_rates(rates, f"Exchange rates from {source}"))
            
        elif choice == "3":
            target = input("Enter target currency code (e.g., EUR): ").strip().upper()
            limit_str = input("Enter maximum number of results (default: 10): ").strip()
            limit = int(limit_str) if limit_str.isdigit() else 10
            
            rates = tool.get_multiple_rates(target=target, limit=limit)
            print(format_multiple_rates(rates, f"Exchange rates to {target}"))
            
        elif choice == "4":
            source = input("Enter source currency code (e.g., USD): ").strip().upper()
            target = input("Enter target currency code (e.g., EUR): ").strip().upper()
            
            start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
            start_date = parse_date(start_date_str)
            if not start_date:
                continue
                
            end_date_str = input("Enter end date (optional, press Enter for today): ").strip()
            end_date = parse_date(end_date_str) if end_date_str else None
            
            rates = tool.get_historical_rates(source, target, start_date, end_date)
            print(format_multiple_rates(rates, f"Historical {source}/{target} rates"))
            
        elif choice == "5":
            currencies = tool.get_all_currencies()
            
            if currencies:
                print("\nAvailable Currencies:")
                print("-" * 40)
                for currency in currencies:
                    code = currency.get("code", "")
                    name = currency.get("name", "")
                    print(f"{code:<8} - {name}")
            else:
                print("No currency information available.")
                
        elif choice == "6":
            print("\nThank you for using the Wise Currency Tool!")
            break
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Wise Currency Tool - Get exchange rates and currency information")
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # rate command - get a specific exchange rate
    rate_parser = subparsers.add_parser("rate", help="Get exchange rate between two currencies")
    rate_parser.add_argument("source", help="Source currency code (e.g., USD)")
    rate_parser.add_argument("target", help="Target currency code (e.g., EUR)")
    rate_parser.add_argument("--date", "-d", help="Date for historical rate (YYYY-MM-DD)")
    
    # rates command - get multiple rates
    rates_parser = subparsers.add_parser("rates", help="Get multiple exchange rates")
    rates_parser.add_argument("--source", "-s", help="Source currency code (e.g., USD)")
    rates_parser.add_argument("--target", "-t", help="Target currency code (e.g., EUR)")
    rates_parser.add_argument("--limit", "-l", type=int, default=10, help="Maximum number of results")
    
    # history command - get historical rates
    history_parser = subparsers.add_parser("history", help="Get historical exchange rates")
    history_parser.add_argument("source", help="Source currency code (e.g., USD)")
    history_parser.add_argument("target", help="Target currency code (e.g., EUR)")
    history_parser.add_argument("--start", "-s", required=True, help="Start date (YYYY-MM-DD)")
    history_parser.add_argument("--end", "-e", help="End date (YYYY-MM-DD), defaults to today")
    
    # currencies command - list all available currencies
    currencies_parser = subparsers.add_parser("currencies", help="List all available currencies")
    
    return parser.parse_args()


def main():
    """Main function"""
    # Check if any arguments were provided
    if len(sys.argv) == 1:
        interactive_mode()
        return
        
    args = parse_args()
    tool = WiseCurrencyTool()
    
    if args.command == "rate":
        date = parse_date(args.date) if args.date else None
        rate = tool.get_exchange_rate(args.source.upper(), args.target.upper(), date)
        print(format_rate_output(rate))
        
    elif args.command == "rates":
        if not args.source and not args.target:
            print("Error: Either source or target currency must be specified.")
            return
            
        rates = tool.get_multiple_rates(
            source=args.source.upper() if args.source else None,
            target=args.target.upper() if args.target else None,
            limit=args.limit
        )
        
        title = None
        if args.source:
            title = f"Exchange rates from {args.source.upper()}"
        elif args.target:
            title = f"Exchange rates to {args.target.upper()}"
            
        print(format_multiple_rates(rates, title))
        
    elif args.command == "history":
        start_date = parse_date(args.start)
        if not start_date:
            return
            
        end_date = parse_date(args.end) if args.end else None
        
        rates = tool.get_historical_rates(
            args.source.upper(),
            args.target.upper(),
            start_date,
            end_date
        )
        
        print(format_multiple_rates(
            rates,
            f"Historical {args.source.upper()}/{args.target.upper()} rates"
        ))
        
    elif args.command == "currencies":
        currencies = tool.get_all_currencies()
        
        if currencies:
            print("\nAvailable Currencies:")
            print("-" * 40)
            for currency in currencies:
                code = currency.get("code", "")
                name = currency.get("name", "")
                print(f"{code:<8} - {name}")
        else:
            print("No currency information available.")


if __name__ == "__main__":
    main()