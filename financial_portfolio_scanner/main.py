"""
Financial Portfolio Scanner - Main Entry Point

This module serves as the entry point for the financial portfolio monitoring system.
It initializes and coordinates the various agents and components.
"""

import asyncio
import logging
import json
import argparse
import pandas as pd
from typing import Dict, Any, List, Optional
from agents.orchestrator_agent import PortfolioScanOrchestrator
from config.settings import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_portfolio_scan(fund_name: str = "Tech Growth Fund") -> Dict[str, Any]:
    """
    Test function for portfolio scanning.
    
    This function creates an instance of PortfolioScanOrchestrator,
    calls scan_portfolio with a test fund name, prints the results,
    and returns the result.
    
    Args:
        fund_name (str): The name of the fund to scan. Defaults to "Tech Growth Fund".
        
    Returns:
        Dict[str, Any]: The scan result containing fund name, report, and action items.
        
    Raises:
        ValueError: If fund_name is empty or contains only whitespace
        RuntimeError: If the portfolio scanning process fails.
    """
    if not fund_name or not fund_name.strip():
        error_msg = "fund_name cannot be empty or contain only whitespace"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    try:
        logger.info(f"Testing portfolio scan for fund: {fund_name}")
        
        # Create an instance of PortfolioScanOrchestrator
        orchestrator = PortfolioScanOrchestrator()
        
        # Call scan_portfolio with the test fund name
        scan_result = await orchestrator.scan_portfolio(fund_name)
        
        # Print the results
        print("\n=== Test Portfolio Scan Results ===")
        print(f"Fund Name: {scan_result['fund_name']}")
        print(f"Report Length: {len(scan_result['report'])} characters")
        print(f"Action Items Count: {len(scan_result['action_items'])}")
        
        print("\n--- Action Items ---")
        for i, action_item in enumerate(scan_result['action_items'], 1):
            print(f"{i}. {action_item}")
        
        logger.info(f"Test portfolio scan completed successfully for fund: {fund_name}")
        return scan_result
        
    except Exception as e:
        error_msg = f"Error in test portfolio scan for fund '{fund_name}': {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


async def scan_single_portfolio(fund_name: str) -> Dict[str, Any]:
    """
    Scan a single portfolio and display the results.
    
    Args:
        fund_name (str): The name of the fund to scan.
        
    Returns:
        Dict[str, Any]: The scan result containing fund name, report, and action items.
        
    Raises:
        ValueError: If fund_name is empty or contains only whitespace
        RuntimeError: If the portfolio scanning process fails.
    """
    if not fund_name or not fund_name.strip():
        error_msg = "fund_name cannot be empty or contain only whitespace"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    try:
        logger.info(f"Scanning single portfolio for fund: {fund_name}")
        
        # Initialize the orchestrator
        orchestrator = PortfolioScanOrchestrator()
        
        # Perform the portfolio scan
        scan_result = await orchestrator.scan_portfolio(fund_name)
        
        # Display the results
        print("\n=== Portfolio Scan Results ===")
        print(f"Fund Name: {scan_result['fund_name']}")
        print("\n--- Report ---")
        print(scan_result['report'])
        
        print("\n--- Action Items ---")
        for i, action_item in enumerate(scan_result['action_items'], 1):
            print(f"{i}. {action_item}")
        
        logger.info(f"Single portfolio scan completed successfully for fund: {fund_name}")
        return scan_result
        
    except Exception as e:
        error_msg = f"Error scanning single portfolio for fund '{fund_name}': {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


async def batch_process_portfolios(fund_names: List[str]) -> List[Dict[str, Any]]:
    """
    Process multiple portfolios in batch.
    
    Args:
        fund_names (List[str]): List of fund names to scan.
        
    Returns:
        List[Dict[str, Any]]: List of scan results for each fund.
        
    Raises:
        ValueError: If fund_names is empty or contains invalid fund names
        RuntimeError: If the batch processing fails
    """
    if not fund_names:
        error_msg = "fund_names list cannot be empty"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    # Validate each fund name
    for fund_name in fund_names:
        if not fund_name or not fund_name.strip():
            error_msg = "Fund name in list cannot be empty or contain only whitespace"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    try:
        logger.info(f"Starting batch processing for {len(fund_names)} funds")
        
        # Initialize the orchestrator
        orchestrator = PortfolioScanOrchestrator()
        
        # Process each fund
        results = []
        for fund_name in fund_names:
            try:
                logger.info(f"Processing fund: {fund_name}")
                scan_result = await orchestrator.scan_portfolio(fund_name)
                results.append(scan_result)
                
                # Display summary for this fund
                print(f"\n=== Batch Processing: {fund_name} ===")
                print(f"Report Length: {len(scan_result['report'])} characters")
                print(f"Action Items Count: {len(scan_result['action_items'])}")
                
            except Exception as e:
                logger.error(f"Error processing fund '{fund_name}': {str(e)}")
                # Add error result to maintain consistency in output
                results.append({
                    "fund_name": fund_name,
                    "report": f"Error: {str(e)}",
                    "action_items": []
                })
        
        logger.info(f"Batch processing completed for {len(fund_names)} funds")
        return results
        
    except Exception as e:
        error_msg = f"Error in batch processing: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


def export_results_to_csv(results: List[Dict[str, Any]], output_file: str = "portfolio_scan_results.csv") -> None:
    """
    Export portfolio scan results to a CSV file.
    
    Args:
        results (List[Dict[str, Any]]): List of scan results to export.
        output_file (str): Path to the output CSV file. Defaults to "portfolio_scan_results.csv".
        
    Raises:
        ValueError: If results is empty or output_file is invalid
        RuntimeError: If the CSV export fails
    """
    if not results:
        error_msg = "results list cannot be empty"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    if not output_file or not output_file.strip():
        error_msg = "output_file cannot be empty or contain only whitespace"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    try:
        logger.info(f"Exporting {len(results)} results to CSV file: {output_file}")
        
        # Prepare data for CSV export
        csv_data = []
        for result in results:
            # Validate result structure
            if not isinstance(result, dict) or 'fund_name' not in result or 'report' not in result or 'action_items' not in result:
                logger.warning(f"Skipping invalid result: {result}")
                continue
                
            # Create a row for each action item
            if result['action_items']:
                for i, action_item in enumerate(result['action_items']):
                    csv_data.append({
                        "Fund Name": result['fund_name'],
                        "Report Length": len(result['report']),
                        "Action Item Number": i + 1,
                        "Action Item": action_item
                    })
            else:
                # Add a row even if there are no action items
                csv_data.append({
                    "Fund Name": result['fund_name'],
                    "Report Length": len(result['report']),
                    "Action Item Number": 0,
                    "Action Item": "No action items"
                })
        
        # Create DataFrame and export to CSV
        df = pd.DataFrame(csv_data)
        df.to_csv(output_file, index=False)
        
        logger.info(f"Results successfully exported to {output_file}")
        print(f"\nResults exported to: {output_file}")
        
    except Exception as e:
        error_msg = f"Error exporting results to CSV: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


async def main():
    """
    Main function to start the financial portfolio scanner.
    
    This function sets up logging and configuration, handles command-line arguments,
    creates an instance of the PortfolioScanOrchestrator, executes portfolio scans,
    and displays results.
    
    Raises:
        RuntimeError: If the main execution fails
    """
    try:
        # Set up logging and configuration
        logging_config = Settings.get_logging_config()
        logging.basicConfig(**logging_config)
        
        logger.info("Starting Financial Portfolio Scanner")
        
        # Validate settings
        Settings.validate_settings()
        
        # Handle command-line arguments
        parser = argparse.ArgumentParser(description="Financial Portfolio Scanner")
        parser.add_argument("--fund", type=str, help="Name of the fund to scan")
        parser.add_argument("--funds", nargs="+", help="Names of multiple funds to scan in batch")
        parser.add_argument("--test", action="store_true", help="Run test portfolio scan")
        parser.add_argument("--export", type=str, help="Export results to CSV file")
        args = parser.parse_args()
        
        # Create an instance of the PortfolioScanOrchestrator
        orchestrator = PortfolioScanOrchestrator()
        
        # Execute portfolio scans based on arguments
        if args.test:
            # Run test portfolio scan
            await test_portfolio_scan()
        
        elif args.fund:
            # Single portfolio scan
            scan_result = await scan_single_portfolio(args.fund)
            
            # Export to CSV if requested
            if args.export:
                export_results_to_csv([scan_result], args.export)
        
        elif args.funds:
            # Batch processing multiple funds
            results = await batch_process_portfolios(args.funds)
            
            # Export to CSV if requested
            if args.export:
                export_results_to_csv(results, args.export)
        
        else:
            # Default behavior - run a demo scan
            fund_name = "Tech Growth Fund"
            scan_result = await scan_single_portfolio(fund_name)
            
            # Get a portfolio summary (without full scan)
            logger.info(f"Getting portfolio summary for fund: {fund_name}")
            summary = orchestrator.get_portfolio_summary(fund_name)
            
            # Print the summary
            print("\n=== Portfolio Summary ===")
            print(json.dumps(summary, indent=2))
            
            # Get a risk assessment (without full scan)
            logger.info(f"Getting risk assessment for fund: {fund_name}")
            risk_assessment = orchestrator.get_portfolio_risk_assessment(fund_name)
            
            # Print the risk assessment
            print("\n=== Risk Assessment ===")
            print(json.dumps(risk_assessment, indent=2))
        
        logger.info("Financial Portfolio Scanner completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Financial Portfolio Scanner: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())