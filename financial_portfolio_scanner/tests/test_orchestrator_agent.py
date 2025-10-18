"""
Financial Portfolio Scanner - Orchestrator Agent Tests

This module contains unit tests for the orchestrator agent implementation.
"""

import pytest
import asyncio
import json
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.orchestrator_agent import (
    PortfolioScanOrchestrator,
    OrchestratorAgent
)
from agents.reporting_agent import ReportingAgent


class TestPortfolioScanOrchestrator:
    """
    Test suite for the PortfolioScanOrchestrator class.
    """
    
    @pytest.fixture
    def orchestrator(self):
        """
        Create a PortfolioScanOrchestrator instance for testing.
        
        Returns:
            PortfolioScanOrchestrator: A test instance of the orchestrator
        """
        with patch('agents.orchestrator_agent.ReportingAgent'):
            return PortfolioScanOrchestrator()
    
    @pytest.mark.asyncio
    async def test_scan_portfolio_success(self, orchestrator):
        """
        Test successful portfolio scanning.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        # Mock the reporting agent's generate_report method
        orchestrator.reporting_agent.generate_report = MagicMock(return_value={"report": "Test report"})
        
        # Mock the tool functions
        with patch('agents.orchestrator_agent.get_portfolio_holdings') as mock_get_holdings, \
             patch('agents.orchestrator_agent.scan_market_news') as mock_scan_news, \
             patch('agents.orchestrator_agent.analyze_risk_exposure') as mock_analyze_risk:
            
            # Set up mock return values
            mock_portfolio_data = json.dumps({
                "fund_name": "Test Fund",
                "holdings": [
                    {"ticker": "AAPL", "name": "Apple Inc.", "weight": 15.2, "value": 152000.00},
                    {"ticker": "MSFT", "name": "Microsoft Corporation", "weight": 12.8, "value": 128000.00}
                ],
                "sector_allocation": [
                    {"sector": "Technology", "weight": 45.2},
                    {"sector": "Financials", "weight": 18.5}
                ],
                "last_updated": "2023-01-01T00:00:00"
            })
            
            mock_news_data = json.dumps({
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
                    }
                ]
            })
            
            mock_risk_data = json.dumps({
                "analysis_timestamp": "2023-01-01T00:00:00",
                "overall_risk_level": "Medium",
                "risk_score": 45,
                "key_findings": ["Portfolio shows adequate diversification across holdings"],
                "action_items": ["Consider diversifying portfolio to reduce concentration risk"],
                "exposure_metrics": {
                    "concentration_risk": 10,
                    "news_sentiment_impact": 5,
                    "volatility_exposure": 31.5,
                    "liquidity_risk": 13.5,
                    "market_risk": 22.5
                }
            })
            
            mock_get_holdings.return_value = mock_portfolio_data
            mock_scan_news.return_value = mock_news_data
            mock_analyze_risk.return_value = mock_risk_data
            
            # Call the method under test
            result = await orchestrator.scan_portfolio("Test Fund")
            
            # Verify the result
            assert result["fund_name"] == "Test Fund"
            assert result["report"] == "Test report"
            assert len(result["action_items"]) == 1
            assert result["action_items"][0] == "Consider diversifying portfolio to reduce concentration risk"
            
            # Verify the tool functions were called with correct arguments
            mock_get_holdings.assert_called_once_with("Test Fund")
            mock_scan_news.assert_called_once_with(["AAPL", "MSFT"])
            mock_analyze_risk.assert_called_once_with(mock_portfolio_data, mock_news_data)
            
            # Verify the reporting agent was called
            orchestrator.reporting_agent.generate_report.assert_called_once_with("Test Fund")
    
    @pytest.mark.asyncio
    async def test_scan_portfolio_empty_fund_name(self, orchestrator):
        """
        Test portfolio scanning with empty fund name.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        with pytest.raises(ValueError, match="fund_name cannot be empty or contain only whitespace"):
            await orchestrator.scan_portfolio("")
    
    @pytest.mark.asyncio
    async def test_scan_portfolio_whitespace_fund_name(self, orchestrator):
        """
        Test portfolio scanning with whitespace-only fund name.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        with pytest.raises(ValueError, match="fund_name cannot be empty or contain only whitespace"):
            await orchestrator.scan_portfolio("   ")
    
    @pytest.mark.asyncio
    async def test_scan_portfolio_no_holdings(self, orchestrator):
        """
        Test portfolio scanning with no holdings.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        # Mock the reporting agent's generate_report method
        orchestrator.reporting_agent.generate_report = MagicMock(return_value={"report": "Test report"})
        
        # Mock the tool functions
        with patch('agents.orchestrator_agent.get_portfolio_holdings') as mock_get_holdings, \
             patch('agents.orchestrator_agent.scan_market_news') as mock_scan_news, \
             patch('agents.orchestrator_agent.analyze_risk_exposure') as mock_analyze_risk:
            
            # Set up mock return values
            mock_portfolio_data = json.dumps({
                "fund_name": "Test Fund",
                "holdings": [],
                "sector_allocation": [],
                "last_updated": "2023-01-01T00:00:00"
            })
            
            mock_news_data = json.dumps({"scan_timestamp": "", "alerts": []})
            
            mock_risk_data = json.dumps({
                "analysis_timestamp": "2023-01-01T00:00:00",
                "overall_risk_level": "Low",
                "risk_score": 20,
                "key_findings": [],
                "action_items": [],
                "exposure_metrics": {}
            })
            
            mock_get_holdings.return_value = mock_portfolio_data
            mock_scan_news.return_value = mock_news_data
            mock_analyze_risk.return_value = mock_risk_data
            
            # Call the method under test
            result = await orchestrator.scan_portfolio("Test Fund")
            
            # Verify the result
            assert result["fund_name"] == "Test Fund"
            assert result["report"] == "Test report"
            assert len(result["action_items"]) == 0
            
            # Verify the tool functions were called with correct arguments
            mock_get_holdings.assert_called_once_with("Test Fund")
            # When there are no tickers, scan_market_news is not called
            mock_scan_news.assert_not_called()
            mock_analyze_risk.assert_called_once_with(mock_portfolio_data, mock_news_data)
    
    def test_get_portfolio_summary_success(self, orchestrator):
        """
        Test successful portfolio summary generation.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        # Mock the get_portfolio_holdings function
        with patch('agents.orchestrator_agent.get_portfolio_holdings') as mock_get_holdings:
            # Set up mock return value
            mock_portfolio_data = json.dumps({
                "fund_name": "Test Fund",
                "total_value": 1000000.00,
                "holdings": [
                    {"ticker": "AAPL", "name": "Apple Inc.", "weight": 15.2, "value": 152000.00},
                    {"ticker": "MSFT", "name": "Microsoft Corporation", "weight": 12.8, "value": 128000.00}
                ],
                "sector_allocation": [
                    {"sector": "Technology", "weight": 45.2},
                    {"sector": "Financials", "weight": 18.5}
                ],
                "last_updated": "2023-01-01T00:00:00"
            })
            
            mock_get_holdings.return_value = mock_portfolio_data
            
            # Call the method under test
            result = orchestrator.get_portfolio_summary("Test Fund")
            
            # Verify the result
            assert result["fund_name"] == "Test Fund"
            assert result["total_value"] == 1000000.00
            assert result["holdings_count"] == 2
            assert len(result["sector_allocation"]) == 2
            assert result["last_updated"] == "2023-01-01T00:00:00"
            
            # Verify the tool function was called with correct arguments
            mock_get_holdings.assert_called_once_with("Test Fund")
    
    def test_get_portfolio_summary_empty_fund_name(self, orchestrator):
        """
        Test portfolio summary generation with empty fund name.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        with pytest.raises(ValueError, match="fund_name cannot be empty or contain only whitespace"):
            orchestrator.get_portfolio_summary("")
    
    def test_get_portfolio_risk_assessment_success(self, orchestrator):
        """
        Test successful portfolio risk assessment generation.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        # Mock the tool functions
        with patch('agents.orchestrator_agent.get_portfolio_holdings') as mock_get_holdings, \
             patch('agents.orchestrator_agent.scan_market_news') as mock_scan_news, \
             patch('agents.orchestrator_agent.analyze_risk_exposure') as mock_analyze_risk:
            
            # Set up mock return values
            mock_portfolio_data = json.dumps({
                "fund_name": "Test Fund",
                "holdings": [
                    {"ticker": "AAPL", "name": "Apple Inc.", "weight": 15.2, "value": 152000.00},
                    {"ticker": "MSFT", "name": "Microsoft Corporation", "weight": 12.8, "value": 128000.00}
                ],
                "sector_allocation": [],
                "last_updated": "2023-01-01T00:00:00"
            })
            
            mock_news_data = json.dumps({
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
                    }
                ]
            })
            
            mock_risk_data = json.dumps({
                "analysis_timestamp": "2023-01-01T00:00:00",
                "overall_risk_level": "Medium",
                "risk_score": 45,
                "key_findings": ["Portfolio shows adequate diversification across holdings"],
                "action_items": ["Consider diversifying portfolio to reduce concentration risk"],
                "exposure_metrics": {
                    "concentration_risk": 10,
                    "news_sentiment_impact": 5,
                    "volatility_exposure": 31.5,
                    "liquidity_risk": 13.5,
                    "market_risk": 22.5
                }
            })
            
            mock_get_holdings.return_value = mock_portfolio_data
            mock_scan_news.return_value = mock_news_data
            mock_analyze_risk.return_value = mock_risk_data
            
            # Call the method under test
            result = orchestrator.get_portfolio_risk_assessment("Test Fund")
            
            # Verify the result
            assert result["fund_name"] == "Test Fund"
            assert result["overall_risk_level"] == "Medium"
            assert result["risk_score"] == 45
            assert len(result["key_findings"]) == 1
            assert len(result["action_items"]) == 1
            assert len(result["exposure_metrics"]) == 5
            assert result["analysis_timestamp"] == "2023-01-01T00:00:00"
            
            # Verify the tool functions were called with correct arguments
            mock_get_holdings.assert_called_once_with("Test Fund")
            mock_scan_news.assert_called_once_with(["AAPL", "MSFT"])
            mock_analyze_risk.assert_called_once_with(mock_portfolio_data, mock_news_data)


class TestOrchestratorAgent:
    """
    Test suite for the OrchestratorAgent class.
    """
    
    @pytest.fixture
    def orchestrator(self):
        """
        Create an OrchestratorAgent instance for testing.
        
        Returns:
            OrchestratorAgent: A test instance of the orchestrator
        """
        with patch('agents.orchestrator_agent.PortfolioScanOrchestrator'):
            return OrchestratorAgent()
    
    def test_coordinate_agents_success(self, orchestrator):
        """
        Test successful agent coordination.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        # Call the method under test
        result = orchestrator.coordinate_agents()
        
        # Verify the result
        assert result["status"] == "success"
        assert result["message"] == "Agents coordinated successfully"
    
    @pytest.mark.asyncio
    async def test_scan_portfolio_delegation(self, orchestrator):
        """
        Test that scan_portfolio delegates to PortfolioScanOrchestrator.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        # Mock the portfolio_orchestrator's scan_portfolio method
        expected_result = {"fund_name": "Test Fund", "report": "Test report", "action_items": []}
        orchestrator.portfolio_orchestrator.scan_portfolio = AsyncMock(return_value=expected_result)
        
        # Call the method under test
        result = await orchestrator.scan_portfolio("Test Fund")
        
        # Verify the result
        assert result == expected_result
        
        # Verify the portfolio_orchestrator was called with correct arguments
        orchestrator.portfolio_orchestrator.scan_portfolio.assert_called_once_with("Test Fund")
    
    def test_get_portfolio_summary_delegation(self, orchestrator):
        """
        Test that get_portfolio_summary delegates to PortfolioScanOrchestrator.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        # Mock the portfolio_orchestrator's get_portfolio_summary method
        expected_result = {"fund_name": "Test Fund", "total_value": 1000000.00, "holdings_count": 2}
        orchestrator.portfolio_orchestrator.get_portfolio_summary = MagicMock(return_value=expected_result)
        
        # Call the method under test
        result = orchestrator.get_portfolio_summary("Test Fund")
        
        # Verify the result
        assert result == expected_result
        
        # Verify the portfolio_orchestrator was called with correct arguments
        orchestrator.portfolio_orchestrator.get_portfolio_summary.assert_called_once_with("Test Fund")
    
    def test_get_portfolio_risk_assessment_delegation(self, orchestrator):
        """
        Test that get_portfolio_risk_assessment delegates to PortfolioScanOrchestrator.
        
        Args:
            orchestrator: The test orchestrator instance
        """
        # Mock the portfolio_orchestrator's get_portfolio_risk_assessment method
        expected_result = {"fund_name": "Test Fund", "overall_risk_level": "Medium", "risk_score": 45}
        orchestrator.portfolio_orchestrator.get_portfolio_risk_assessment = MagicMock(return_value=expected_result)
        
        # Call the method under test
        result = orchestrator.get_portfolio_risk_assessment("Test Fund")
        
        # Verify the result
        assert result == expected_result
        
        # Verify the portfolio_orchestrator was called with correct arguments
        orchestrator.portfolio_orchestrator.get_portfolio_risk_assessment.assert_called_once_with("Test Fund")