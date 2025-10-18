"""
Financial Portfolio Scanner - Main Entry Point Tests

This module contains comprehensive test cases for the main entry point of the
financial portfolio monitoring system.

Note: The test_portfolio_scan function in main.py is not a test function but a utility function.
It's imported here for testing purposes but should not be collected as a test by pytest.
"""

import asyncio
import json
import os
import tempfile
import unittest.mock as mock
from typing import Dict, Any, List
import pytest
import pandas as pd
from unittest.mock import AsyncMock, MagicMock, patch

# Import the functions to be tested
# Note: test_portfolio_scan is a utility function, not a test function
from main import (
    scan_single_portfolio,
    batch_process_portfolios,
    export_results_to_csv,
    main
)

# Import the test_portfolio_scan function with a different name to avoid pytest collecting it as a test
from main import test_portfolio_scan as portfolio_scan_util
from agents.orchestrator_agent import PortfolioScanOrchestrator
from config.settings import Settings


# Test fixtures
@pytest.fixture
def mock_portfolio_data() -> str:
    """
    Fixture providing mock portfolio data in JSON format.
    
    Returns:
        str: JSON string containing mock portfolio data
    """
    portfolio_data = {
        "fund_name": "Test Fund",
        "total_value": 1000000.00,
        "holdings": [
            {
                "ticker": "AAPL",
                "name": "Apple Inc.",
                "weight": 15.2,
                "value": 152000.00
            },
            {
                "ticker": "MSFT",
                "name": "Microsoft Corporation",
                "weight": 12.8,
                "value": 128000.00
            }
        ],
        "sector_allocation": [
            {
                "sector": "Technology",
                "weight": 45.2
            },
            {
                "sector": "Financials",
                "weight": 18.5
            }
        ],
        "last_updated": "2023-01-01T00:00:00"
    }
    return json.dumps(portfolio_data, indent=2)


@pytest.fixture
def mock_news_data() -> str:
    """
    Fixture providing mock market news data in JSON format.
    
    Returns:
        str: JSON string containing mock market news data
    """
    news_data = {
        "scan_timestamp": "2023-01-01T00:00:00",
        "alerts": [
            {
                "ticker": "AAPL",
                "alert_type": "Earnings Report",
                "severity": "Medium",
                "headline": "Apple Inc. Reports Q4 Earnings Beat Expectations",
                "sentiment": "Positive",
                "impact_score": 0.75,
                "source": "Financial Times"
            },
            {
                "ticker": "MSFT",
                "alert_type": "Regulatory",
                "severity": "Medium",
                "headline": "Microsoft Faces EU Antitrust Investigation Over Cloud Practices",
                "sentiment": "Negative",
                "impact_score": -0.65,
                "source": "Reuters"
            }
        ]
    }
    return json.dumps(news_data, indent=2)


@pytest.fixture
def mock_risk_analysis() -> str:
    """
    Fixture providing mock risk analysis data in JSON format.
    
    Returns:
        str: JSON string containing mock risk analysis data
    """
    risk_analysis = {
        "analysis_timestamp": "2023-01-01T00:00:00",
        "overall_risk_level": "Medium",
        "risk_score": 45,
        "key_findings": [
            "Portfolio shows adequate diversification across holdings",
            "Negative news sentiment outweighs positive sentiment for portfolio holdings"
        ],
        "action_items": [
            "Consider diversifying portfolio to reduce concentration risk",
            "Review holdings with negative news sentiment and consider rebalancing"
        ],
        "exposure_metrics": {
            "concentration_risk": 10,
            "news_sentiment_impact": -5,
            "volatility_exposure": 31.5,
            "liquidity_risk": 13.5,
            "market_risk": 22.5
        }
    }
    return json.dumps(risk_analysis, indent=2)


@pytest.fixture
def mock_scan_result() -> Dict[str, Any]:
    """
    Fixture providing a mock scan result dictionary.
    
    Returns:
        Dict[str, Any]: Mock scan result containing fund name, report, and action items
    """
    return {
        "fund_name": "Test Fund",
        "report": "This is a comprehensive portfolio analysis report.",
        "action_items": [
            "Consider diversifying portfolio to reduce concentration risk",
            "Review holdings with negative news sentiment and consider rebalancing"
        ]
    }


@pytest.fixture
def mock_portfolio_summary() -> Dict[str, Any]:
    """
    Fixture providing a mock portfolio summary dictionary.
    
    Returns:
        Dict[str, Any]: Mock portfolio summary
    """
    return {
        "fund_name": "Test Fund",
        "total_value": 1000000.00,
        "holdings_count": 5,
        "sector_allocation": [
            {"sector": "Technology", "weight": 45.2},
            {"sector": "Financials", "weight": 18.5}
        ],
        "last_updated": "2023-01-01T00:00:00"
    }


@pytest.fixture
def mock_risk_assessment() -> Dict[str, Any]:
    """
    Fixture providing a mock risk assessment dictionary.
    
    Returns:
        Dict[str, Any]: Mock risk assessment
    """
    return {
        "fund_name": "Test Fund",
        "overall_risk_level": "Medium",
        "risk_score": 45,
        "key_findings": [
            "Portfolio shows adequate diversification across holdings"
        ],
        "action_items": [
            "Consider diversifying portfolio to reduce concentration risk"
        ],
        "exposure_metrics": {
            "concentration_risk": 10,
            "news_sentiment_impact": -5,
            "volatility_exposure": 31.5,
            "liquidity_risk": 13.5,
            "market_risk": 22.5
        },
        "analysis_timestamp": "2023-01-01T00:00:00"
    }


@pytest.fixture
def mock_batch_results() -> List[Dict[str, Any]]:
    """
    Fixture providing a list of mock batch scan results.
    
    Returns:
        List[Dict[str, Any]]: List of mock scan results
    """
    return [
        {
            "fund_name": "Fund 1",
            "report": "Report for Fund 1",
            "action_items": ["Action 1 for Fund 1", "Action 2 for Fund 1"]
        },
        {
            "fund_name": "Fund 2",
            "report": "Report for Fund 2",
            "action_items": ["Action 1 for Fund 2"]
        },
        {
            "fund_name": "Fund 3",
            "report": "Report for Fund 3",
            "action_items": []
        }
    ]


@pytest.fixture
def mock_orchestrator() -> MagicMock:
    """
    Fixture providing a mock PortfolioScanOrchestrator.
    
    Returns:
        MagicMock: Mocked PortfolioScanOrchestrator
    """
    orchestrator = MagicMock(spec=PortfolioScanOrchestrator)
    orchestrator.scan_portfolio = AsyncMock()
    orchestrator.get_portfolio_summary = MagicMock()
    orchestrator.get_portfolio_risk_assessment = MagicMock()
    return orchestrator


@pytest.fixture
def mock_settings() -> MagicMock:
    """
    Fixture providing a mock Settings class.
    
    Returns:
        MagicMock: Mocked Settings class
    """
    settings = MagicMock(spec=Settings)
    settings.get_logging_config.return_value = {
        "level": 20,  # INFO level
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "filename": None,
        "filemode": "a"
    }
    settings.validate_settings.return_value = True
    return settings


# Test cases for test_portfolio_scan function
class TestTestPortfolioScan:
    """
    Test cases for the test_portfolio_scan function.
    """

    @pytest.mark.asyncio
    async def test_test_portfolio_scan_success(self, mock_orchestrator, mock_scan_result):
        """
        Test test_portfolio_scan function with successful execution.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
            mock_scan_result: Mock scan result
        """
        # Setup mock
        mock_orchestrator.scan_portfolio.return_value = mock_scan_result
        
        # Patch the PortfolioScanOrchestrator to return our mock
        with patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator):
            # Call the function
            result = await portfolio_scan_util("Test Fund")
            
            # Assertions
            assert result == mock_scan_result
            mock_orchestrator.scan_portfolio.assert_called_once_with("Test Fund")

    @pytest.mark.asyncio
    async def test_test_portfolio_scan_default_fund(self, mock_orchestrator, mock_scan_result):
        """
        Test test_portfolio_scan function with default fund name.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
            mock_scan_result: Mock scan result
        """
        # Setup mock
        mock_orchestrator.scan_portfolio.return_value = mock_scan_result
        
        # Patch the PortfolioScanOrchestrator to return our mock
        with patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator):
            # Call the function without specifying fund name
            result = await portfolio_scan_util()
            
            # Assertions
            assert result == mock_scan_result
            mock_orchestrator.scan_portfolio.assert_called_once_with("Tech Growth Fund")

    @pytest.mark.asyncio
    async def test_test_portfolio_scan_exception(self, mock_orchestrator):
        """
        Test test_portfolio_scan function when an exception occurs.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
        """
        # Setup mock to raise an exception
        mock_orchestrator.scan_portfolio.side_effect = Exception("Test exception")
        
        # Patch the PortfolioScanOrchestrator to return our mock
        with patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator):
            # Call the function and expect an exception
            with pytest.raises(RuntimeError, match="Error in test portfolio scan for fund 'Test Fund': Test exception"):
                await portfolio_scan_util("Test Fund")


# Test cases for scan_single_portfolio function
class TestScanSinglePortfolio:
    """
    Test cases for the scan_single_portfolio function.
    """

    @pytest.mark.asyncio
    async def test_scan_single_portfolio_success(self, mock_orchestrator, mock_scan_result):
        """
        Test scan_single_portfolio function with successful execution.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
            mock_scan_result: Mock scan result
        """
        # Setup mock
        mock_orchestrator.scan_portfolio.return_value = mock_scan_result
        
        # Patch the PortfolioScanOrchestrator to return our mock
        with patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator):
            # Call the function
            result = await scan_single_portfolio("Test Fund")
            
            # Assertions
            assert result == mock_scan_result
            mock_orchestrator.scan_portfolio.assert_called_once_with("Test Fund")

    @pytest.mark.asyncio
    async def test_scan_single_portfolio_exception(self, mock_orchestrator):
        """
        Test scan_single_portfolio function when an exception occurs.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
        """
        # Setup mock to raise an exception
        mock_orchestrator.scan_portfolio.side_effect = Exception("Test exception")
        
        # Patch the PortfolioScanOrchestrator to return our mock
        with patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator):
            # Call the function and expect an exception
            with pytest.raises(RuntimeError, match="Error scanning single portfolio for fund 'Test Fund': Test exception"):
                await scan_single_portfolio("Test Fund")


# Test cases for batch_process_portfolios function
class TestBatchProcessPortfolios:
    """
    Test cases for the batch_process_portfolios function.
    """

    @pytest.mark.asyncio
    async def test_batch_process_portfolios_success(self, mock_orchestrator, mock_batch_results):
        """
        Test batch_process_portfolios function with successful execution.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
            mock_batch_results: Mock batch results
        """
        # Setup mock to return different results for different funds
        def side_effect(fund_name):
            for result in mock_batch_results:
                if result["fund_name"] == fund_name:
                    return result
            return {"fund_name": fund_name, "report": "Default report", "action_items": []}
        
        mock_orchestrator.scan_portfolio.side_effect = side_effect
        
        # Patch the PortfolioScanOrchestrator to return our mock
        with patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator):
            # Call the function
            fund_names = ["Fund 1", "Fund 2", "Fund 3"]
            result = await batch_process_portfolios(fund_names)
            
            # Assertions
            assert len(result) == 3
            assert result == mock_batch_results
            assert mock_orchestrator.scan_portfolio.call_count == 3
            mock_orchestrator.scan_portfolio.assert_any_call("Fund 1")
            mock_orchestrator.scan_portfolio.assert_any_call("Fund 2")
            mock_orchestrator.scan_portfolio.assert_any_call("Fund 3")

    @pytest.mark.asyncio
    async def test_batch_process_portfolios_with_exception(self, mock_orchestrator):
        """
        Test batch_process_portfolios function when an exception occurs for one fund.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
        """
        # Setup mock to raise an exception for one fund
        def side_effect(fund_name):
            if fund_name == "Fund 2":
                raise Exception("Test exception for Fund 2")
            return {
                "fund_name": fund_name,
                "report": f"Report for {fund_name}",
                "action_items": [f"Action for {fund_name}"]
            }
        
        mock_orchestrator.scan_portfolio.side_effect = side_effect
        
        # Patch the PortfolioScanOrchestrator to return our mock
        with patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator):
            # Call the function
            fund_names = ["Fund 1", "Fund 2", "Fund 3"]
            result = await batch_process_portfolios(fund_names)
            
            # Assertions
            assert len(result) == 3
            assert result[0]["fund_name"] == "Fund 1"
            assert result[1]["fund_name"] == "Fund 2"
            assert result[1]["report"] == "Error: Test exception for Fund 2"
            assert result[1]["action_items"] == []
            assert result[2]["fund_name"] == "Fund 3"
            assert mock_orchestrator.scan_portfolio.call_count == 3

    @pytest.mark.asyncio
    async def test_batch_process_portfolios_orchestrator_exception(self):
        """
        Test batch_process_portfolios function when an exception occurs during orchestrator initialization.
        """
        # Patch the PortfolioScanOrchestrator to raise an exception during initialization
        with patch('main.PortfolioScanOrchestrator', side_effect=Exception("Test exception")):
            # Call the function and expect an exception
            with pytest.raises(RuntimeError, match="Error in batch processing: Test exception"):
                await batch_process_portfolios(["Fund 1", "Fund 2"])


# Test cases for export_results_to_csv function
class TestExportResultsToCsv:
    """
    Test cases for the export_results_to_csv function.
    """

    def test_export_results_to_csv_success(self, mock_batch_results):
        """
        Test export_results_to_csv function with successful execution.
        
        Args:
            mock_batch_results: Mock batch results
        """
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Call the function
            export_results_to_csv(mock_batch_results, temp_filename)
            
            # Verify the file was created and contains expected data
            assert os.path.exists(temp_filename)
            
            # Read the CSV file and verify its contents
            df = pd.read_csv(temp_filename)
            
            # Assertions
            assert len(df) == 4  # 2 actions for Fund 1, 1 for Fund 2, 1 for Fund 3 (no actions)
            assert list(df.columns) == ["Fund Name", "Report Length", "Action Item Number", "Action Item"]
            
            # Verify specific rows
            fund1_rows = df[df["Fund Name"] == "Fund 1"]
            assert len(fund1_rows) == 2
            assert fund1_rows.iloc[0]["Action Item Number"] == 1
            assert fund1_rows.iloc[0]["Action Item"] == "Action 1 for Fund 1"
            assert fund1_rows.iloc[1]["Action Item Number"] == 2
            assert fund1_rows.iloc[1]["Action Item"] == "Action 2 for Fund 1"
            
            fund2_rows = df[df["Fund Name"] == "Fund 2"]
            assert len(fund2_rows) == 1
            assert fund2_rows.iloc[0]["Action Item Number"] == 1
            assert fund2_rows.iloc[0]["Action Item"] == "Action 1 for Fund 2"
            
            fund3_rows = df[df["Fund Name"] == "Fund 3"]
            assert len(fund3_rows) == 1
            assert fund3_rows.iloc[0]["Action Item Number"] == 0
            assert fund3_rows.iloc[0]["Action Item"] == "No action items"
            
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_export_results_to_csv_default_filename(self, mock_batch_results):
        """
        Test export_results_to_csv function with default filename.
        
        Args:
            mock_batch_results: Mock batch results
        """
        # Create a temporary file for testing
        default_filename = "portfolio_scan_results.csv"
        
        # Mock the to_csv method to avoid creating a real file
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            # Call the function with default filename
            export_results_to_csv(mock_batch_results)
            
            # Verify to_csv was called with the default filename
            mock_to_csv.assert_called_once_with(default_filename, index=False)

    def test_export_results_to_csv_exception(self, mock_batch_results):
        """
        Test export_results_to_csv function when an exception occurs.
        
        Args:
            mock_batch_results: Mock batch results
        """
        # Mock the DataFrame constructor to raise an exception
        with patch('pandas.DataFrame', side_effect=Exception("Test exception")):
            # Call the function and expect an exception
            with pytest.raises(RuntimeError, match="Error exporting results to CSV: Test exception"):
                export_results_to_csv(mock_batch_results, "test.csv")


# Test cases for main function
class TestMain:
    """
    Test cases for the main function.
    """

    @pytest.mark.asyncio
    async def test_main_with_test_argument(self, mock_orchestrator, mock_scan_result, mock_settings):
        """
        Test main function with --test argument.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
            mock_scan_result: Mock scan result
            mock_settings: Mocked Settings class
        """
        # Setup mocks
        mock_orchestrator.scan_portfolio.return_value = mock_scan_result
        
        # Patch dependencies
        with patch('main.argparse.ArgumentParser') as mock_parser, \
             patch('main.Settings', mock_settings), \
             patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator), \
             patch('main.test_portfolio_scan', new_callable=AsyncMock) as mock_test_scan:
            
            # Setup argument parser mock
            mock_args = mock.MagicMock()
            mock_args.test = True
            mock_args.fund = None
            mock_args.funds = None
            mock_args.export = None
            mock_parser.return_value.parse_args.return_value = mock_args
            
            # Call the function
            await main()
            
            # Assertions
            mock_settings.validate_settings.assert_called_once()
            mock_test_scan.assert_called_once()

    @pytest.mark.asyncio
    async def test_main_with_fund_argument(self, mock_orchestrator, mock_scan_result, mock_settings):
        """
        Test main function with --fund argument.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
            mock_scan_result: Mock scan result
            mock_settings: Mocked Settings class
        """
        # Setup mocks
        mock_orchestrator.scan_portfolio.return_value = mock_scan_result
        
        # Patch dependencies
        with patch('main.argparse.ArgumentParser') as mock_parser, \
             patch('main.Settings', mock_settings), \
             patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator), \
             patch('main.scan_single_portfolio', new_callable=AsyncMock, return_value=mock_scan_result) as mock_scan_single, \
             patch('main.export_results_to_csv') as mock_export:
            
            # Setup argument parser mock
            mock_args = mock.MagicMock()
            mock_args.test = False
            mock_args.fund = "Test Fund"
            mock_args.funds = None
            mock_args.export = "test_output.csv"
            mock_parser.return_value.parse_args.return_value = mock_args
            
            # Call the function
            await main()
            
            # Assertions
            mock_settings.validate_settings.assert_called_once()
            mock_scan_single.assert_called_once_with("Test Fund")
            mock_export.assert_called_once_with([mock_scan_result], "test_output.csv")

    @pytest.mark.asyncio
    async def test_main_with_funds_argument(self, mock_orchestrator, mock_batch_results, mock_settings):
        """
        Test main function with --funds argument.
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
            mock_batch_results: Mock batch results
            mock_settings: Mocked Settings class
        """
        # Setup mocks
        mock_orchestrator.scan_portfolio.return_value = mock_batch_results[0]
        
        # Patch dependencies
        with patch('main.argparse.ArgumentParser') as mock_parser, \
             patch('main.Settings', mock_settings), \
             patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator), \
             patch('main.batch_process_portfolios', new_callable=AsyncMock, return_value=mock_batch_results) as mock_batch, \
             patch('main.export_results_to_csv') as mock_export:
            
            # Setup argument parser mock
            mock_args = mock.MagicMock()
            mock_args.test = False
            mock_args.fund = None
            mock_args.funds = ["Fund 1", "Fund 2", "Fund 3"]
            mock_args.export = "test_output.csv"
            mock_parser.return_value.parse_args.return_value = mock_args
            
            # Call the function
            await main()
            
            # Assertions
            mock_settings.validate_settings.assert_called_once()
            mock_batch.assert_called_once_with(["Fund 1", "Fund 2", "Fund 3"])
            mock_export.assert_called_once_with(mock_batch_results, "test_output.csv")

    @pytest.mark.asyncio
    async def test_main_with_no_arguments(self, mock_orchestrator, mock_portfolio_summary, mock_risk_assessment, mock_settings):
        """
        Test main function with no arguments (default behavior).
        
        Args:
            mock_orchestrator: Mocked PortfolioScanOrchestrator
            mock_portfolio_summary: Mock portfolio summary
            mock_risk_assessment: Mock risk assessment
            mock_settings: Mocked Settings class
        """
        # Setup mocks
        mock_orchestrator.get_portfolio_summary.return_value = mock_portfolio_summary
        mock_orchestrator.get_portfolio_risk_assessment.return_value = mock_risk_assessment
        
        # Patch dependencies
        with patch('main.argparse.ArgumentParser') as mock_parser, \
             patch('main.Settings', mock_settings), \
             patch('main.PortfolioScanOrchestrator', return_value=mock_orchestrator), \
             patch('main.scan_single_portfolio', new_callable=AsyncMock) as mock_scan_single, \
             patch('builtins.print') as mock_print:
            
            # Setup argument parser mock
            mock_args = mock.MagicMock()
            mock_args.test = False
            mock_args.fund = None
            mock_args.funds = None
            mock_args.export = None
            mock_parser.return_value.parse_args.return_value = mock_args
            
            # Call the function
            await main()
            
            # Assertions
            mock_settings.validate_settings.assert_called_once()
            mock_scan_single.assert_called_once_with("Tech Growth Fund")
            mock_orchestrator.get_portfolio_summary.assert_called_once_with("Tech Growth Fund")
            mock_orchestrator.get_portfolio_risk_assessment.assert_called_once_with("Tech Growth Fund")
            
            # Verify print was called for summary and risk assessment
            assert mock_print.call_count >= 2  # At least for summary and risk assessment

    @pytest.mark.asyncio
    async def test_main_with_exception(self, mock_settings):
        """
        Test main function when an exception occurs.
        
        Args:
            mock_settings: Mocked Settings class
        """
        # Patch dependencies
        with patch('main.argparse.ArgumentParser') as mock_parser, \
             patch('main.Settings', mock_settings), \
             patch('main.PortfolioScanOrchestrator', side_effect=Exception("Test exception")):
            
            # Setup argument parser mock
            mock_args = mock.MagicMock()
            mock_args.test = False
            mock_args.fund = None
            mock_args.funds = None
            mock_args.export = None
            mock_parser.return_value.parse_args.return_value = mock_args
            
            # Call the function and expect an exception
            with pytest.raises(Exception, match="Test exception"):
                await main()