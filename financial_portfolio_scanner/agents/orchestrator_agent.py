"""
Financial Portfolio Scanner - Orchestrator Agent

This module contains the orchestrator agent implementation that coordinates
the various components of the financial portfolio monitoring system.
"""

import json
import logging
import datetime
from typing import Dict, Any, List, Optional

from .tool_functions import (
    get_portfolio_holdings,
    scan_market_news,
    analyze_risk_exposure
)
from .reporting_agent import ReportingAgent

logger = logging.getLogger(__name__)


class PortfolioScanOrchestrator:
    """
    The PortfolioScanOrchestrator class coordinates the workflow for scanning
    and analyzing financial portfolios, integrating various components to provide
    comprehensive portfolio analysis and reporting.
    
    This orchestrator manages the entire portfolio scanning process, from retrieving
    portfolio holdings to generating final reports with actionable insights.
    """
    
    def __init__(self):
        """
        Initialize the PortfolioScanOrchestrator.
        
        This sets up the orchestrator with necessary components including the
        reporting agent for generating comprehensive reports.
        
        Raises:
            RuntimeError: If initialization fails due to any reason
        """
        try:
            self.reporting_agent = ReportingAgent()
            logger.info("PortfolioScanOrchestrator initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize PortfolioScanOrchestrator: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    async def scan_portfolio(self, fund_name: str) -> Dict[str, Any]:
        """
        Perform a comprehensive scan and analysis of a financial portfolio.
        
        This method orchestrates the entire portfolio scanning workflow, including:
        1. Retrieving portfolio holdings
        2. Scanning market news for portfolio tickers
        3. Analyzing risk exposure based on portfolio data and market news
        4. Generating a comprehensive report with actionable insights
        
        Args:
            fund_name (str): The name of the fund to scan and analyze
            
        Returns:
            Dict[str, Any]: A dictionary containing the scan results with the following structure:
                - fund_name: The name of the analyzed fund
                - report: Comprehensive portfolio analysis report
                - action_items: List of actionable recommendations
                
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If any step in the scanning process fails
        """
        # Input validation
        if not fund_name or not fund_name.strip():
            error_msg = "fund_name cannot be empty or contain only whitespace"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            logger.info(f"Starting portfolio scan for fund: {fund_name}")
            
            # Step 1: Get portfolio holdings
            logger.info("Step 1: Retrieving portfolio holdings")
            portfolio_data = get_portfolio_holdings(fund_name)
            
            # Parse portfolio data to extract tickers
            try:
                portfolio_json = json.loads(portfolio_data)
                holdings = portfolio_json.get("holdings", [])
                tickers = [holding.get("ticker") for holding in holdings if holding.get("ticker")]
                logger.info(f"Extracted {len(tickers)} tickers from portfolio holdings")
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse portfolio data: {str(e)}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            # Step 2: Extract tickers and scan market news
            logger.info("Step 2: Scanning market news for portfolio tickers")
            if not tickers:
                logger.warning("No tickers found in portfolio holdings")
                news_data = json.dumps({"scan_timestamp": "", "alerts": []})
            else:
                news_data = scan_market_news(tickers)
            
            # Step 3: Perform risk analysis
            logger.info("Step 3: Analyzing risk exposure")
            risk_analysis = analyze_risk_exposure(portfolio_data, news_data)
            
            # Step 4: Generate a comprehensive report using the reporting agent
            logger.info("Step 4: Generating comprehensive report")
            report_result = await self.reporting_agent.generate_report(fund_name)
            
            # Extract action items from risk analysis
            try:
                risk_json = json.loads(risk_analysis)
                action_items = risk_json.get("action_items", [])
                logger.debug(f"Extracted {len(action_items)} action items from risk analysis")
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse risk analysis for action items: {str(e)}")
                action_items = []
            
            # Compile the final result
            result = {
                "fund_name": fund_name,
                "report": report_result.get("report", ""),
                "action_items": action_items
            }
            
            logger.info(f"Portfolio scan completed successfully for fund: {fund_name}")
            return result
            
        except Exception as e:
            error_msg = f"Failed to scan portfolio for fund '{fund_name}': {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def get_portfolio_summary(self, fund_name: str) -> Dict[str, Any]:
        """
        Generate a summary of the portfolio without performing a full scan.
        
        This method provides a quick overview of the portfolio holdings and basic metrics.
        
        Args:
            fund_name (str): The name of the fund to summarize
            
        Returns:
            Dict[str, Any]: A dictionary containing the portfolio summary
            
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If the summary generation fails
        """
        if not fund_name or not fund_name.strip():
            error_msg = "fund_name cannot be empty or contain only whitespace"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            logger.info(f"Generating portfolio summary for fund: {fund_name}")
            
            # Get portfolio holdings
            portfolio_data = get_portfolio_holdings(fund_name)
            
            # Parse portfolio data
            try:
                portfolio_json = json.loads(portfolio_data)
                
                # Extract key information for summary
                summary = {
                    "fund_name": portfolio_json.get("fund_name", fund_name),
                    "total_value": portfolio_json.get("total_value", 0),
                    "holdings_count": len(portfolio_json.get("holdings", [])),
                    "sector_allocation": portfolio_json.get("sector_allocation", []),
                    "last_updated": portfolio_json.get("last_updated", "")
                }
                
                logger.info(f"Portfolio summary generated successfully for fund: {fund_name}")
                return summary
                
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse portfolio data for summary: {str(e)}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            
        except Exception as e:
            error_msg = f"Failed to generate portfolio summary for fund '{fund_name}': {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def get_portfolio_risk_assessment(self, fund_name: str) -> Dict[str, Any]:
        """
        Generate a risk assessment for the portfolio without performing a full scan.
        
        This method provides a focused risk analysis of the portfolio holdings.
        
        Args:
            fund_name (str): The name of the fund to assess
            
        Returns:
            Dict[str, Any]: A dictionary containing the risk assessment
            
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If the risk assessment fails
        """
        if not fund_name or not fund_name.strip():
            error_msg = "fund_name cannot be empty or contain only whitespace"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            logger.info(f"Generating risk assessment for fund: {fund_name}")
            
            # Get portfolio holdings
            portfolio_data = get_portfolio_holdings(fund_name)
            
            # Parse portfolio data to extract tickers
            try:
                portfolio_json = json.loads(portfolio_data)
                holdings = portfolio_json.get("holdings", [])
                tickers = [holding.get("ticker") for holding in holdings if holding.get("ticker")]
                logger.debug(f"Extracted {len(tickers)} tickers from portfolio holdings")
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse portfolio data: {str(e)}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            # Scan market news for portfolio tickers
            if not tickers:
                logger.warning("No tickers found in portfolio holdings")
                news_data = json.dumps({"scan_timestamp": "", "alerts": []})
            else:
                news_data = scan_market_news(tickers)
            
            # Perform risk analysis
            risk_analysis = analyze_risk_exposure(portfolio_data, news_data)
            
            # Parse risk analysis
            try:
                risk_json = json.loads(risk_analysis)
                
                # Extract key risk information
                risk_assessment = {
                    "fund_name": fund_name,
                    "overall_risk_level": risk_json.get("overall_risk_level", "Unknown"),
                    "risk_score": risk_json.get("risk_score", 0),
                    "key_findings": risk_json.get("key_findings", []),
                    "action_items": risk_json.get("action_items", []),
                    "exposure_metrics": risk_json.get("exposure_metrics", {}),
                    "analysis_timestamp": risk_json.get("analysis_timestamp", "")
                }
                
                logger.info(f"Risk assessment generated successfully for fund: {fund_name}")
                return risk_assessment
                
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse risk analysis: {str(e)}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            
        except Exception as e:
            error_msg = f"Failed to generate risk assessment for fund '{fund_name}': {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)


class OrchestratorAgent:
    """
    The OrchestratorAgent class coordinates the various agents and components
    of the financial portfolio monitoring system.
    
    This class serves as a wrapper around the PortfolioScanOrchestrator,
    providing a simplified interface for coordinating portfolio scanning activities.
    """
    
    def __init__(self):
        """
        Initialize the OrchestratorAgent.
        
        This creates an instance of the PortfolioScanOrchestrator for managing
        the portfolio scanning workflow.
        
        Raises:
            RuntimeError: If initialization fails due to any reason
        """
        try:
            self.portfolio_orchestrator = PortfolioScanOrchestrator()
            logger.info("OrchestratorAgent initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize OrchestratorAgent: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def coordinate_agents(self) -> Dict[str, Any]:
        """
        Coordinate the activities of all agents in the system.
        
        This method serves as a high-level interface for coordinating the
        various agents and components in the financial portfolio monitoring system.
        
        Returns:
            Dict[str, Any]: A status message indicating successful coordination
            
        Raises:
            RuntimeError: If the coordination process fails
        """
        try:
            logger.info("Coordinating agents in the financial portfolio monitoring system")
            
            # In a real implementation, this method would coordinate multiple agents
            # For now, it simply returns a success message
            result = {
                "status": "success",
                "message": "Agents coordinated successfully",
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            logger.info("Agent coordination completed successfully")
            return result
            
        except Exception as e:
            error_msg = f"Failed to coordinate agents: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    async def scan_portfolio(self, fund_name: str) -> Dict[str, Any]:
        """
        Perform a comprehensive scan and analysis of a financial portfolio.
        
        This method delegates to the PortfolioScanOrchestrator to perform the
        actual portfolio scanning and analysis.
        
        Args:
            fund_name (str): The name of the fund to scan and analyze
            
        Returns:
            Dict[str, Any]: A dictionary containing the scan results
            
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If the scanning process fails
        """
        return await self.portfolio_orchestrator.scan_portfolio(fund_name)
    
    def get_portfolio_summary(self, fund_name: str) -> Dict[str, Any]:
        """
        Generate a summary of the portfolio without performing a full scan.
        
        This method delegates to the PortfolioScanOrchestrator to generate the
        portfolio summary.
        
        Args:
            fund_name (str): The name of the fund to summarize
            
        Returns:
            Dict[str, Any]: A dictionary containing the portfolio summary
            
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If the summary generation fails
        """
        return self.portfolio_orchestrator.get_portfolio_summary(fund_name)
    
    def get_portfolio_risk_assessment(self, fund_name: str) -> Dict[str, Any]:
        """
        Generate a risk assessment for the portfolio without performing a full scan.
        
        This method delegates to the PortfolioScanOrchestrator to generate the
        risk assessment.
        
        Args:
            fund_name (str): The name of the fund to assess
            
        Returns:
            Dict[str, Any]: A dictionary containing the risk assessment
            
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If the risk assessment fails
        """
        return self.portfolio_orchestrator.get_portfolio_risk_assessment(fund_name)