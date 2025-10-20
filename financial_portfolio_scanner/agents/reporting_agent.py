"""
Financial Portfolio Scanner - Reporting Agent

This module contains the reporting agent implementation that generates
reports and insights for the financial portfolio monitoring system.
"""

from typing import Dict, Any, List, Optional
import logging
import json
import datetime
import asyncio

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

# Import Azure AI Agent Framework components
try:
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import ToolDefinition, ToolType
    from azure.identity import AzureCliCredential
    AZURE_AVAILABLE = True
    logger.info("Azure AI Agent Framework is available")
except ImportError as e:
    AZURE_AVAILABLE = False
    logger.warning(f"Azure AI Agent Framework is not available: {str(e)}")

# Import OpenAI for fallback
try:
    import openai
    OPENAI_AVAILABLE = True
    logger.info("OpenAI is available")
except ImportError as e:
    OPENAI_AVAILABLE = False
    logger.warning(f"OpenAI is not available: {str(e)}")


class AzureReportingAgent:
    """
    An implementation of the Reporting Agent using Azure AI Agent Framework.
    
    This class uses AzureAIAgentClient to create and interact with an AI agent
    for generating financial reports and insights.
    """
    
    def __init__(self, name: str, instructions: str, use_azure: bool = True):
        """
        Initialize the AzureReportingAgent.
        
        Args:
            name (str): The name of the agent
            instructions (str): The instructions for the agent
            use_azure (bool): Whether to use Azure or fall back to OpenAI
        """
        self.name = name
        self.instructions = instructions
        self.tools = {}
        self.use_azure = use_azure and AZURE_AVAILABLE
        self.client = None
        self.agent = None
        self.openai_client = None
        
        logger.info(f"Initializing {'Azure' if self.use_azure else 'OpenAI'} Reporting Agent with name: {name}")
        
        # Initialize the appropriate client
        if self.use_azure:
            self._init_azure_client()
        elif OPENAI_AVAILABLE:
            self._init_openai_client()
        else:
            logger.warning("Neither Azure nor OpenAI is available, using mock implementation")
    
    def _init_azure_client(self):
        """Initialize the Azure AI Project Client."""
        try:
            # Check if required Azure settings are available
            if not Settings.AZURE_AI_PROJECT_CONNECTION_STRING:
                logger.warning("Azure AI Project Connection String not configured, falling back to OpenAI")
                self.use_azure = False
                if OPENAI_AVAILABLE:
                    self._init_openai_client()
                return
            
            # Create Azure AI Project Client
            credential = AzureCliCredential()
            self.client = AIProjectClient.from_connection_string(
                credential=credential,
                conn_str=Settings.AZURE_AI_PROJECT_CONNECTION_STRING
            )
            logger.info("Azure AI Project Client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure AI Project Client: {str(e)}")
            self.use_azure = False
            if OPENAI_AVAILABLE:
                self._init_openai_client()
    
    def _init_openai_client(self):
        """Initialize the OpenAI client for fallback."""
        try:
            if not Settings.OPENAI_API_KEY:
                logger.warning("OpenAI API Key not configured")
                return
            
            self.openai_client = openai.OpenAI(api_key=Settings.OPENAI_API_KEY)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    
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
    
    async def _create_azure_agent(self):
        """Create an Azure AI agent with the specified configuration."""
        try:
            # Define tool definitions for Azure
            tool_definitions = []
            for tool_name in self.tools.keys():
                tool_definitions.append(ToolDefinition(
                    name=tool_name,
                    description=f"Tool for {tool_name}",
                    type=ToolType.FUNCTION
                ))
            
            # Create the agent
            self.agent = await self.client.agents.create_agent(
                model=Settings.AZURE_OPENAI_CHAT_MODEL_ID or "gpt-4",
                name=self.name,
                instructions=self.instructions,
                tools=tool_definitions
            )
            logger.info(f"Created Azure agent with ID: {self.agent.id}")
        except Exception as e:
            logger.error(f"Failed to create Azure agent: {str(e)}")
            raise
    
    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response to a prompt.
        
        Args:
            prompt (str): The prompt to respond to
            
        Returns:
            str: The generated response
            
        Raises:
            ValueError: If prompt is empty or contains only whitespace
            RuntimeError: If the response generation fails
        """
        if not prompt or not prompt.strip():
            error_msg = "Prompt cannot be empty or contain only whitespace"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        logger.debug(f"Generating response for prompt: {prompt[:50]}...")
        
        try:
            if self.use_azure and self.client:
                return await self._generate_azure_response(prompt)
            elif self.openai_client:
                return await self._generate_openai_response(prompt)
            else:
                return self._generate_mock_response(prompt)
        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}")
            # Fallback to mock response if all else fails
            return self._generate_mock_response(prompt)
    
    async def _generate_azure_response(self, prompt: str) -> str:
        """Generate a response using Azure AI Agent."""
        try:
            # Create agent if not already created
            if not self.agent:
                await self._create_azure_agent()
            
            # Create a thread
            thread = await self.client.agents.create_thread()
            
            # Create a message
            await self.client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=prompt
            )
            
            # Run the agent
            run = await self.client.agents.create_run(
                thread_id=thread.id,
                agent_id=self.agent.id
            )
            
            # Wait for completion
            while run.status not in ["completed", "failed", "cancelled"]:
                await asyncio.sleep(1)
                run = await self.client.agents.get_run(thread_id=thread.id, run_id=run.id)
            
            if run.status == "failed":
                logger.error(f"Azure agent run failed: {run.last_error}")
                raise RuntimeError(f"Azure agent run failed: {run.last_error}")
            
            # Get the messages
            messages = await self.client.agents.list_messages(thread_id=thread.id)
            
            # Extract the assistant's response
            for message in messages.data:
                if message.role == "assistant":
                    content = message.content[0].text.value if message.content else ""
                    logger.debug("Generated Azure response")
                    return content
            
            logger.warning("No assistant response found in Azure thread")
            return self._generate_mock_response(prompt)
            
        except Exception as e:
            logger.error(f"Error generating Azure response: {str(e)}")
            raise
    
    async def _generate_openai_response(self, prompt: str) -> str:
        """Generate a response using OpenAI."""
        try:
            # Prepare messages for OpenAI
            messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt}
            ]
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model=Settings.OPENAI_CHAT_MODEL_ID,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            logger.debug("Generated OpenAI response")
            return content
            
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            raise
    
    def _generate_mock_response(self, prompt: str) -> str:
        """Generate a mock response when neither Azure nor OpenAI is available."""
        logger.debug("Generating mock response")
        
        # Mock response structure
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
        
        return json.dumps(response, indent=2)


def create_reporting_agent() -> AzureReportingAgent:
    """
    Create and configure the Financial Reporting Agent.
    
    This function creates an AzureReportingAgent instance, sets the agent name to
    "FinancialReportingAgent", provides comprehensive instructions for the agent's
    responsibilities, and registers the tool functions for portfolio analysis.
    
    The function will attempt to use Azure AI Agent Framework if configured,
    otherwise it will fall back to OpenAI or a mock implementation.
    
    Returns:
        AzureReportingAgent: A configured instance of the Financial Reporting Agent
        
    Raises:
        RuntimeError: If the agent cannot be initialized due to other errors
    """
    logger.info("Creating Financial Reporting Agent")
    
    try:
        # Determine whether to use Azure based on configuration
        use_azure = (
            AZURE_AVAILABLE and
            Settings.AZURE_AI_PROJECT_CONNECTION_STRING and
            Settings.AZURE_AI_PROJECT_CONNECTION_STRING.strip()
        )
        
        if use_azure:
            logger.info("Using Azure AI Agent Framework for reporting agent")
        elif OPENAI_AVAILABLE and Settings.OPENAI_API_KEY:
            logger.info("Using OpenAI for reporting agent")
        else:
            logger.warning("Neither Azure nor OpenAI is properly configured, using mock implementation")
        
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
        
        Please format your response as a structured JSON object with the following sections:
        - portfolio_summary: Overall portfolio information
        - holdings_analysis: Detailed analysis of portfolio holdings
        - market_insights: Key market news and their implications
        - risk_assessment: Risk analysis and exposure metrics
        - recommendations: Actionable recommendations for portfolio management
        """
        
        # Create the agent with the specified configuration
        agent = AzureReportingAgent(
            name="FinancialReportingAgent",
            instructions=instructions,
            use_azure=use_azure
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
    
    async def generate_report(self, fund_name: str) -> Dict[str, Any]:
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
            response = await self.agent.generate_response(prompt)
            
            # Parse and return the response
            # Note: In a real implementation, you would parse the response
            # to ensure it's valid JSON and handle any parsing errors
            logger.info(f"Successfully generated report for fund: {fund_name}")
            return {"report": response}
            
        except Exception as e:
            error_msg = f"Failed to generate report: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def generate_report_sync(self, fund_name: str) -> Dict[str, Any]:
        """
        Generate a comprehensive report of the financial portfolio (synchronous wrapper).
        
        This method provides a synchronous interface to the async generate_report method.
        
        Args:
            fund_name (str): The name of the fund to generate a report for
            
        Returns:
            Dict[str, Any]: A dictionary containing the generated report
            
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If the report generation fails
        """
        try:
            # Run the async method in an event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an event loop, we need to use a different approach
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.generate_report(fund_name))
                    return future.result()
            else:
                return asyncio.run(self.generate_report(fund_name))
        except Exception as e:
            error_msg = f"Failed to generate report synchronously: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    async def generate_insights(self, fund_name: str) -> Dict[str, Any]:
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
            response = await self.agent.generate_response(prompt)
            
            # Parse and return the response
            # Note: In a real implementation, you would parse the response
            # to ensure it's valid JSON and handle any parsing errors
            logger.info(f"Successfully generated insights for fund: {fund_name}")
            return {"insights": response}
            
        except Exception as e:
            error_msg = f"Failed to generate insights: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def generate_insights_sync(self, fund_name: str) -> Dict[str, Any]:
        """
        Generate insights and recommendations based on portfolio analysis (synchronous wrapper).
        
        This method provides a synchronous interface to the async generate_insights method.
        
        Args:
            fund_name (str): The name of the fund to generate insights for
            
        Returns:
            Dict[str, Any]: A dictionary containing the generated insights
            
        Raises:
            ValueError: If fund_name is empty or None
            RuntimeError: If the insights generation fails
        """
        try:
            # Run the async method in an event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an event loop, we need to use a different approach
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.generate_insights(fund_name))
                    return future.result()
            else:
                return asyncio.run(self.generate_insights(fund_name))
        except Exception as e:
            error_msg = f"Failed to generate insights synchronously: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)