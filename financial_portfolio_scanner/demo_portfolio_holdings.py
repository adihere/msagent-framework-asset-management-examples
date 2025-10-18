#!/usr/bin/env python3
"""
Demo script to showcase the get_portfolio_holdings function.
"""

import json
from agents.tool_functions import get_portfolio_holdings


def main():
    """Main function to demonstrate the get_portfolio_holdings function."""
    print("Financial Portfolio Scanner - Portfolio Holdings Demo")
    print("=" * 60)
    
    # Test with a valid fund name
    fund_name = "Growth Equity Fund"
    print(f"\nRetrieving portfolio holdings for: {fund_name}")
    print("-" * 60)
    
    try:
        portfolio_data = get_portfolio_holdings(fund_name)
        
        # Parse the JSON string to display it nicely
        parsed_data = json.loads(portfolio_data)
        
        # Display fund information
        print(f"Fund Name: {parsed_data['fund_name']}")
        print(f"Total Value: ${parsed_data['total_value']:,.2f}")
        print(f"Last Updated: {parsed_data['last_updated']}")
        
        # Display holdings
        print("\nHoldings:")
        print("-" * 60)
        print(f"{'Ticker':<10} {'Name':<25} {'Weight':<10} {'Value':<15}")
        print("-" * 60)
        for holding in parsed_data['holdings']:
            print(f"{holding['ticker']:<10} {holding['name']:<25} {holding['weight']:<10.2f}% ${holding['value']:<14,.2f}")
        
        # Display sector allocation
        print("\nSector Allocation:")
        print("-" * 60)
        print(f"{'Sector':<25} {'Weight':<10}")
        print("-" * 60)
        for sector in parsed_data['sector_allocation']:
            print(f"{sector['sector']:<25} {sector['weight']:<10.2f}%")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test error handling
    print("\n" + "=" * 60)
    print("Testing Error Handling")
    print("=" * 60)
    
    # Test with empty fund name
    print("\nTesting with empty fund name:")
    try:
        get_portfolio_holdings("")
    except ValueError as e:
        print(f"Expected error caught: {e}")
    
    # Test with non-string input
    print("\nTesting with non-string input:")
    try:
        get_portfolio_holdings(123)
    except TypeError as e:
        print(f"Expected error caught: {e}")


if __name__ == "__main__":
    main()