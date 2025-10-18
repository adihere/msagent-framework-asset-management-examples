"""
Financial Portfolio Scanner - Reporting Agent

This module contains the reporting agent implementation that generates
reports and insights for the financial portfolio monitoring system.
"""

from typing import Dict, Any, List, Optional
import logging
import json
import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import Settings
from .tool_functions import (
    get_portfolio_holdings,
    scan_market_news,
    analyze_risk_exposure
)

logger = logging.getLogger(__name__)


class MockChatAgent:
    """
    A mock implementation of the ChatAgent class for testing purposes.
    
    This class simulates the behavior of a ChatAgent without requiring
    the actual microsoft-agent-framework dependency.
    """
    
    def __init__(self, name: str, instructions: str, client: Any = None):
        """
        Initialize the MockChatAgent.
        
        Args:
            name (str): The name of the agent
            instructions (str): The instructions for the agent
            client (Any, optional): The client for the agent (not used in mock)
        """
        self.name = name
        self.instructions = instructions
        self.tools = {}
        logger.info(f"MockChatAgent initialized with name: {name}")
    
    def register_tool(self, name: str, func: callable) -> None:
        """
        Register a tool function with the agent.
        
        Args:
            name (str): The name of the tool
            func (callable): The tool function
            
        Raises:
            ValueError: If name is empty or func is not callable
        """
        if not name or not name.strip():
            error_msg = "Tool name cannot be empty or contain only whitespace"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if not callable(func):
            error_msg = f"Tool function must be callable, got {type(func).__name__}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        self.tools[name] = func
        logger.debug(f"Registered tool: {name}")
    
    def generate_response(self, prompt: str) -> str:
        """
        Generate a response to a prompt.
        
        Args:
            prompt (str): The prompt to respond to
            
        Returns:
            str: The generated response
            
        Raises:
            ValueError: If prompt is empty or contains only whitespace
        """
        if not prompt or not prompt.strip():
            error_msg = "Prompt cannot be empty or contain only whitespace"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        logger.debug(f"Generating response for prompt: {prompt[:50]}...")
        
        # In a real implementation, this would use the LLM to generate a response
        # For the mock, we'll return a simple JSON response
        response = {
            "portfolio_summary": {
                "fund_name": "Mock Fund",
                "total_value": 1000000.00,
                "holdings_count": 5,
                "last_updated": datetime.datetime.now().isoformat()
            },
            "holdings_analysis": {
                "top_holdings": [
                    {"ticker": "AAPL", "weight": 15.2, "value": 152000.00},
                    {"ticker": "MSFT", "weight": 12.8, "value": 128000.00}
                ],
                "sector_allocation": [
                    {"sector": "Technology", "weight": 45.2},
                    {"sector": "Financials", "weight": 18.5}
                ]
            },
            "market_insights": {
                "news_alerts": [
                    {
                        "ticker": "AAPL",
                        "alert_type": "Earnings Report",
                        "severity": "Medium",
                        "headline": "Apple Inc. Reports Q4 Earnings Beat Expectations",
                        "sentiment": "Positive"
                    }
                ]
            },
            "risk_assessment": {
                "overall_risk_level": "Medium",
                "risk_score": 45,
                "key_findings": [
                    "Portfolio shows adequate diversification across holdings"
                ]
            },
            "recommendations": [
                "Consider diversifying portfolio to reduce concentration risk",
                "Review holdings with negative news sentiment and consider rebalancing"
            ]
        }
        
        logger.debug("Generated mock response")
        return json.dumps(response, indent=2)


def create_reporting_agent() -> MockChatAgent:
    """
    Create and configure the Financial Reporting Agent.
    
    This function creates a MockChatAgent instance for testing purposes,
    sets the agent name to "FinancialReportingAgent", provides
    comprehensive instructions for the agent's responsibilities, and registers the
    tool functions for portfolio analysis.
    
    Returns:
        MockChatAgent: A configured instance of the Financial Reporting Agent
        
    Raises:
        RuntimeError: If the agent cannot be initialized due to other errors
    """
    logger.info("Creating Financial Reporting Agent")
    
    try:
        # Define comprehensive instructions for the agent
        instructions = """
        You are the FinancialReportingAgent, responsible for generating comprehensive
        financial reports and insights based on portfolio data and market analysis.
        
        Your responsibilities include:
        1. Analyzing portfolio holdings to understand asset allocation and diversification
        2. Scanning market news for relevant information that might impact portfolio performance
        3. Assessing risk exposure based on portfolio composition and market conditions
        4. Generating detailed reports with actionable insights and recommendations
        5. Identifying opportunities for portfolio optimization and risk mitigation
        
        When generating reports, you should:
        - Provide clear, concise summaries of portfolio performance
        - Highlight key risks and opportunities
        - Offer actionable recommendations for portfolio management
        - Use data-driven insights to support your analysis
        - Consider both short-term market conditions and long-term investment goals
        
        You have access to the following tools:
        - get_portfolio_holdings: Retrieve portfolio holdings data for a specified fund
        - scan_market_news: Scan market news for specified tickers
        - analyze_risk_exposure: Analyze risk exposure based on portfolio data and market news
        
        Use these tools to gather the necessary information before generating your reports.
        Always base your analysis on the most current data available.
        """
        
        # Create the agent with the specified configuration
        agent = MockChatAgent(
            name="FinancialReportingAgent",
            instructions=instructions
        )
        
        # Register the tool functions
        agent.register_tool("get_portfolio_holdings", get_portfolio_holdings)
        agent.register_tool("scan_market_news", scan_market_news)
        agent.register_tool("analyze_risk_exposure", analyze_risk_exposure)
        
        logger.info("Financial Reporting Agent created successfully")
        return agent
        
    except Exception as e:
        error_msg = f"Failed to create Financial Reporting Agent: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


class ReportingAgent:
    """
    The ReportingAgent class generates reports and insights based on
    the financial portfolio data analyzed by the system.
    
    This class serves as a wrapper around the ChatAgent implementation,
    providing a simplified interface for generating financial reports.
    """
    
    def __init__(self):
        """
        Initialize the ReportingAgent.
        
        This creates an instance of the Financial Reporting Agent using the
        create_reporting_agent function.
        
        Raises:
            RuntimeError: If initialization fails due to any reason
        """
        try:
            self.agent = create_reporting_agent()
            logger.info("ReportingAgent initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize ReportingAgent: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def generate_report(self, fund_name: str) -> Dict[str, Any]:
        """
        Generate a comprehensive report of the financial portfolio.
        
        This method uses the underlying ChatAgent to generate a detailed
        report based on the portfolio holdings, market news, and risk analysis.
        
        Args:
            fund_name (str): The name of the fund to generate a report for
            
        Returns:
            Dict[str, Any]: A dictionary containing the generated report
            
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If the report generation fails
        """
        if not fund_name or not fund_name.strip():
            error_msg = "fund_name cannot be empty or contain only whitespace"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            logger.info(f"Generating comprehensive report for fund: {fund_name}")
            
            # Prepare the prompt for the agent
            prompt = f"""
            Generate a comprehensive financial report for the fund '{fund_name}'.
            
            Please follow these steps:
            1. Use the get_portfolio_holdings tool to retrieve the portfolio data
            2. Extract the ticker symbols from the portfolio holdings
            3. Use the scan_market_news tool to get relevant market news for these tickers
            4. Use the analyze_risk_exposure tool to assess the portfolio's risk
            5. Generate a comprehensive report that includes:
               - Portfolio summary and performance overview
               - Analysis of holdings and asset allocation
               - Key market news and their potential impact
               - Risk assessment and exposure analysis
               - Actionable recommendations for portfolio management
            
            Format your response as a structured JSON object with the following sections:
            - portfolio_summary: Overall portfolio information
            - holdings_analysis: Detailed analysis of portfolio holdings
            - market_insights: Key market news and their implications
            - risk_assessment: Risk analysis and exposure metrics
            - recommendations: Actionable recommendations for portfolio management
            """
            
            # Generate the report using the agent
            response = self.agent.generate_response(prompt)
            
            # Parse and return the response
            # Note: In a real implementation, you would parse the response
            # to ensure it's valid JSON and handle any parsing errors
            logger.info(f"Successfully generated report for fund: {fund_name}")
            return {"report": response}
            
        except Exception as e:
            error_msg = f"Failed to generate report: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def generate_insights(self, fund_name: str) -> Dict[str, Any]:
        """
        Generate insights and recommendations based on portfolio analysis.
        
        This method uses the underlying ChatAgent to generate focused insights
        and recommendations based on the portfolio data and market conditions.
        
        Args:
            fund_name (str): The name of the fund to generate insights for
            
        Returns:
            Dict[str, Any]: A dictionary containing the generated insights
            
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If the insights generation fails
        """
        if not fund_name or not fund_name.strip():
            error_msg = "fund_name cannot be empty or contain only whitespace"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            logger.info(f"Generating insights for fund: {fund_name}")
            
            # Prepare the prompt for the agent
            prompt = f"""
            Generate focused insights and recommendations for the fund '{fund_name}'.
            
            Please follow these steps:
            1. Use the get_portfolio_holdings tool to retrieve the portfolio data
            2. Extract the ticker symbols from the portfolio holdings
            3. Use the scan_market_news tool to get relevant market news for these tickers
            4. Use the analyze_risk_exposure tool to assess the portfolio's risk
            5. Generate focused insights that include:
               - Key opportunities for portfolio optimization
               - Potential risks and mitigation strategies
               - Specific recommendations for individual holdings
               - Market trends and their implications for the portfolio
               - Short-term and long-term strategic recommendations
            
            Format your response as a structured JSON object with the following sections:
            - opportunities: Key opportunities for portfolio optimization
            - risks: Potential risks and mitigation strategies
            - holding_recommendations: Specific recommendations for individual holdings
            - market_trends: Analysis of relevant market trends
            - strategic_recommendations: Short-term and long-term strategic recommendations
            """
            
            # Generate the insights using the agent
            response = self.agent.generate_response(prompt)
            
            # Parse and return the response
            # Note: In a real implementation, you would parse the response
            # to ensure it's valid JSON and handle any parsing errors
            logger.info(f"Successfully generated insights for fund: {fund_name}")
            return {"insights": response}
            
        except Exception as e:
            error_msg = f"Failed to generate insights: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)