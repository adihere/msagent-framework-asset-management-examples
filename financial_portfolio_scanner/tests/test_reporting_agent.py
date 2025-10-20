"""
Financial Portfolio Scanner - Reporting Agent Tests

This module contains unit tests for the reporting agent implementation.
"""

import pytest
import json
import sys
import os
from unittest.mock import MagicMock, patch, AsyncMock

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.reporting_agent import (
    create_reporting_agent,
    ReportingAgent,
    AzureReportingAgent
)
from agents.tool_functions import (
    get_portfolio_holdings,
    scan_market_news,
    analyze_risk_exposure
)


class TestCreateReportingAgent:
    """
    Test suite for the create_reporting_agent function.
    """
    
    def test_create_reporting_agent_success(self):
        """
        Test successful creation of the reporting agent.
        
        This test verifies that the create_reporting_agent function
        successfully creates an AzureReportingAgent instance with the correct
        name, instructions, and registered tools.
        """
        # Call the function under test
        agent = create_reporting_agent()
        
        # Verify the agent is an AzureReportingAgent instance
        assert isinstance(agent, AzureReportingAgent)
        
        # Verify the agent name
        assert agent.name == "FinancialReportingAgent"
        
        # Verify the agent instructions are not empty
        assert agent.instructions
        assert "FinancialReportingAgent" in agent.instructions
        assert "portfolio holdings" in agent.instructions
        assert "market news" in agent.instructions
        assert "risk exposure" in agent.instructions
        
        # Verify the tools are registered
        assert "get_portfolio_holdings" in agent.tools
        assert "scan_market_news" in agent.tools
        assert "analyze_risk_exposure" in agent.tools
        
        # Verify the tool functions are correct
        assert agent.tools["get_portfolio_holdings"] == get_portfolio_holdings
        assert agent.tools["scan_market_news"] == scan_market_news
        assert agent.tools["analyze_risk_exposure"] == analyze_risk_exposure
    
    @patch('agents.reporting_agent.AzureReportingAgent')
    def test_create_reporting_agent_initialization_failure(self, mock_agent_class):
        """
        Test handling of agent initialization failure.
        
        This test verifies that the create_reporting_agent function
        properly handles and raises a RuntimeError when the agent
        initialization fails.
        
        Args:
            mock_agent_class: Mocked AzureReportingAgent class
        """
        # Configure the mock to raise an exception during initialization
        mock_agent_class.side_effect = Exception("Initialization failed")
        
        # Verify that a RuntimeError is raised
        with pytest.raises(RuntimeError, match="Failed to create Financial Reporting Agent: Initialization failed"):
            create_reporting_agent()
    
    @patch('agents.reporting_agent.AzureReportingAgent')
    def test_create_reporting_agent_tool_registration_failure(self, mock_agent_class):
        """
        Test handling of tool registration failure.
        
        This test verifies that the create_reporting_agent function
        properly handles and raises a RuntimeError when tool registration
        fails.
        
        Args:
            mock_agent_class: Mocked AzureReportingAgent class
        """
        # Create a mock agent instance
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # Configure the register_tool method to raise an exception
        mock_agent.register_tool.side_effect = Exception("Tool registration failed")
        
        # Verify that a RuntimeError is raised
        with pytest.raises(RuntimeError, match="Failed to create Financial Reporting Agent: Tool registration failed"):
            create_reporting_agent()


class TestAzureReportingAgent:
    """
    Test suite for the AzureReportingAgent class.
    """
    
    @pytest.fixture
    def mock_agent(self):
        """
        Create an AzureReportingAgent instance for testing.
        
        Returns:
            AzureReportingAgent: A test instance of the Azure agent
        """
        return AzureReportingAgent(
            name="TestAgent",
            instructions="Test instructions",
            use_azure=False  # Use mock mode for testing
        )
    
    def test_azure_reporting_agent_initialization(self, mock_agent):
        """
        Test AzureReportingAgent initialization.
        
        This test verifies that the AzureReportingAgent is properly initialized
        with the provided name and instructions, and that the tools
        dictionary is empty.
        
        Args:
            mock_agent: The test mock agent instance
        """
        # Verify the name and instructions are set correctly
        assert mock_agent.name == "TestAgent"
        assert mock_agent.instructions == "Test instructions"
        
        # Verify the tools dictionary is empty
        assert mock_agent.tools == {}
    
    def test_azure_reporting_agent_register_tool(self, mock_agent):
        """
        Test tool registration with AzureReportingAgent.
        
        This test verifies that the register_tool method correctly
        adds a tool function to the tools dictionary.
        
        Args:
            mock_agent: The test mock agent instance
        """
        # Define a mock tool function
        def mock_tool_function():
            return "Mock result"
        
        # Register the tool
        mock_agent.register_tool("mock_tool", mock_tool_function)
        
        # Verify the tool is registered
        assert "mock_tool" in mock_agent.tools
        assert mock_agent.tools["mock_tool"] == mock_tool_function
    
    @pytest.mark.asyncio
    async def test_azure_reporting_agent_generate_response(self, mock_agent):
        """
        Test response generation with AzureReportingAgent.
        
        This test verifies that the generate_response method returns
        a properly formatted JSON string with the expected structure.
        
        Args:
            mock_agent: The test mock agent instance
        """
        # Generate a response
        response = await mock_agent.generate_response("Test prompt")
        
        # Verify the response is a string
        assert isinstance(response, str)
        
        # Verify the response can be parsed as JSON
        parsed_response = json.loads(response)
        
        # Verify the structure of the response
        assert "portfolio_summary" in parsed_response
        assert "holdings_analysis" in parsed_response
        assert "market_insights" in parsed_response
        assert "risk_assessment" in parsed_response
        assert "recommendations" in parsed_response
        
        # Verify portfolio summary structure
        portfolio_summary = parsed_response["portfolio_summary"]
        assert "fund_name" in portfolio_summary
        assert "total_value" in portfolio_summary
        assert "holdings_count" in portfolio_summary
        assert "last_updated" in portfolio_summary
        
        # Verify holdings analysis structure
        holdings_analysis = parsed_response["holdings_analysis"]
        assert "top_holdings" in holdings_analysis
        assert "sector_allocation" in holdings_analysis
        
        # Verify market insights structure
        market_insights = parsed_response["market_insights"]
        assert "news_alerts" in market_insights
        
        # Verify risk assessment structure
        risk_assessment = parsed_response["risk_assessment"]
        assert "overall_risk_level" in risk_assessment
        assert "risk_score" in risk_assessment
        assert "key_findings" in risk_assessment
        
        # Verify recommendations structure
        recommendations = parsed_response["recommendations"]
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
    
    def test_azure_reporting_agent_init_azure_fallback(self):
        """
        Test AzureReportingAgent initialization with Azure unavailable.
        
        This test verifies that the AzureReportingAgent falls back to mock mode
        when Azure is not available.
        """
        agent = AzureReportingAgent(
            name="TestAgent",
            instructions="Test instructions",
            use_azure=True
        )
        
        # Agent should still be created but with use_azure set to False
        # if Azure is not available
        assert agent.name == "TestAgent"
        assert agent.instructions == "Test instructions"


class TestReportingAgent:
    """
    Test suite for the ReportingAgent class.
    """
    
    @pytest.fixture
    def reporting_agent(self):
        """
        Create a ReportingAgent instance for testing.
        
        Returns:
            ReportingAgent: A test instance of the reporting agent
        """
        with patch('agents.reporting_agent.create_reporting_agent') as mock_create:
            # Create a mock agent
            mock_agent = MagicMock()
            mock_create.return_value = mock_agent
            
            # Create and return the ReportingAgent
            return ReportingAgent()
    
    def test_reporting_agent_initialization_success(self):
        """
        Test successful ReportingAgent initialization.
        
        This test verifies that the ReportingAgent is properly initialized
        with a valid agent instance.
        """
        with patch('agents.reporting_agent.create_reporting_agent') as mock_create:
            # Create a mock agent
            mock_agent = MagicMock()
            mock_create.return_value = mock_agent
            
            # Create the ReportingAgent
            agent = ReportingAgent()
            
            # Verify the agent is set correctly
            assert agent.agent == mock_agent
            
            # Verify create_reporting_agent was called
            mock_create.assert_called_once()
    
    def test_reporting_agent_initialization_failure(self):
        """
        Test ReportingAgent initialization failure.
        
        This test verifies that the ReportingAgent properly handles and
        raises a RuntimeError when the agent creation fails.
        """
        with patch('agents.reporting_agent.create_reporting_agent') as mock_create:
            # Configure the mock to raise an exception
            mock_create.side_effect = Exception("Agent creation failed")
            
            # Verify that a RuntimeError is raised
            with pytest.raises(RuntimeError, match="Failed to initialize ReportingAgent: Agent creation failed"):
                ReportingAgent()
    
    @pytest.mark.asyncio
    async def test_generate_report_success(self, reporting_agent):
        """
        Test successful report generation.
        
        This test verifies that the generate_report method correctly
        generates a report for a valid fund name.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        # Configure the mock agent's generate_response method
        mock_response = json.dumps({
            "portfolio_summary": {
                "fund_name": "Test Fund",
                "total_value": 1000000.00,
                "holdings_count": 5,
                "last_updated": "2023-01-01T00:00:00"
            },
            "holdings_analysis": {
                "top_holdings": [
                    {"ticker": "AAPL", "weight": 15.2, "value": 152000.00}
                ],
                "sector_allocation": [
                    {"sector": "Technology", "weight": 45.2}
                ]
            },
            "market_insights": {
                "news_alerts": []
            },
            "risk_assessment": {
                "overall_risk_level": "Medium",
                "risk_score": 45,
                "key_findings": []
            },
            "recommendations": []
        })
        reporting_agent.agent.generate_response = AsyncMock(return_value=mock_response)
        
        # Generate the report
        result = await reporting_agent.generate_report("Test Fund")
        
        # Verify the result structure
        assert "report" in result
        assert result["report"] == mock_response
        
        # Verify the agent's generate_response method was called
        reporting_agent.agent.generate_response.assert_called_once()
        
        # Verify the prompt contains the fund name
        call_args = reporting_agent.agent.generate_response.call_args[0][0]
        assert "Test Fund" in call_args
        assert "portfolio holdings" in call_args
        assert "market news" in call_args
        assert "assess the portfolio's risk" in call_args
        assert "portfolio_summary" in call_args
        assert "holdings_analysis" in call_args
        assert "market_insights" in call_args
        assert "risk_assessment" in call_args
        assert "recommendations" in call_args
    
    @pytest.mark.asyncio
    async def test_generate_report_empty_fund_name(self, reporting_agent):
        """
        Test report generation with empty fund name.
        
        This test verifies that the generate_report method raises a
        ValueError when the fund name is empty.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        with pytest.raises(ValueError, match="fund_name cannot be empty or contain only whitespace"):
            await reporting_agent.generate_report("")
    
    @pytest.mark.asyncio
    async def test_generate_report_whitespace_fund_name(self, reporting_agent):
        """
        Test report generation with whitespace-only fund name.
        
        This test verifies that the generate_report method raises a
        ValueError when the fund name contains only whitespace.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        with pytest.raises(ValueError, match="fund_name cannot be empty or contain only whitespace"):
            await reporting_agent.generate_report("   ")
    
    @pytest.mark.asyncio
    async def test_generate_report_agent_failure(self, reporting_agent):
        """
        Test report generation when the agent fails.
        
        This test verifies that the generate_report method properly
        handles and raises a RuntimeError when the agent's generate_response
        method fails.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        # Configure the mock agent's generate_response method to raise an exception
        reporting_agent.agent.generate_response = AsyncMock(side_effect=Exception("Agent response failed"))
        
        # Verify that a RuntimeError is raised
        with pytest.raises(RuntimeError, match="Failed to generate report: Agent response failed"):
            await reporting_agent.generate_report("Test Fund")
    
    @pytest.mark.asyncio
    async def test_generate_insights_success(self, reporting_agent):
        """
        Test successful insights generation.
        
        This test verifies that the generate_insights method correctly
        generates insights for a valid fund name.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        # Configure the mock agent's generate_response method
        mock_response = json.dumps({
            "opportunities": [
                "Diversify portfolio to reduce concentration risk"
            ],
            "risks": [
                "Market volatility may impact short-term performance"
            ],
            "holding_recommendations": [
                {"ticker": "AAPL", "action": "Hold"}
            ],
            "market_trends": [
                "Technology sector showing strong growth"
            ],
            "strategic_recommendations": [
                "Consider long-term growth opportunities in emerging markets"
            ]
        })
        reporting_agent.agent.generate_response = AsyncMock(return_value=mock_response)
        
        # Generate the insights
        result = await reporting_agent.generate_insights("Test Fund")
        
        # Verify the result structure
        assert "insights" in result
        assert result["insights"] == mock_response
        
        # Verify the agent's generate_response method was called
        reporting_agent.agent.generate_response.assert_called_once()
        
        # Verify the prompt contains the fund name
        call_args = reporting_agent.agent.generate_response.call_args[0][0]
        assert "Test Fund" in call_args
        assert "portfolio holdings" in call_args
        assert "market news" in call_args
        assert "assess the portfolio's risk" in call_args
        assert "opportunities" in call_args
        assert "risks" in call_args
        assert "holding_recommendations" in call_args
        assert "market_trends" in call_args
        assert "strategic_recommendations" in call_args
    
    @pytest.mark.asyncio
    async def test_generate_insights_empty_fund_name(self, reporting_agent):
        """
        Test insights generation with empty fund name.
        
        This test verifies that the generate_insights method raises a
        ValueError when the fund name is empty.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        with pytest.raises(ValueError, match="fund_name cannot be empty or contain only whitespace"):
            await reporting_agent.generate_insights("")
    
    @pytest.mark.asyncio
    async def test_generate_insights_whitespace_fund_name(self, reporting_agent):
        """
        Test insights generation with whitespace-only fund name.
        
        This test verifies that the generate_insights method raises a
        ValueError when the fund name contains only whitespace.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        with pytest.raises(ValueError, match="fund_name cannot be empty or contain only whitespace"):
            await reporting_agent.generate_insights("   ")
    
    @pytest.mark.asyncio
    async def test_generate_insights_agent_failure(self, reporting_agent):
        """
        Test insights generation when the agent fails.
        
        This test verifies that the generate_insights method properly
        handles and raises a RuntimeError when the agent's generate_response
        method fails.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        # Configure the mock agent's generate_response method to raise an exception
        reporting_agent.agent.generate_response = AsyncMock(side_effect=Exception("Agent response failed"))
        
        # Verify that a RuntimeError is raised
        with pytest.raises(RuntimeError, match="Failed to generate insights: Agent response failed"):
            await reporting_agent.generate_insights("Test Fund")
    
    def test_generate_report_sync(self, reporting_agent):
        """
        Test synchronous wrapper for report generation.
        
        This test verifies that the generate_report_sync method provides
        a synchronous interface to the async generate_report method.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        # Configure the mock agent's generate_response method
        mock_response = json.dumps({
            "portfolio_summary": {
                "fund_name": "Test Fund",
                "total_value": 1000000.00,
                "holdings_count": 5,
                "last_updated": "2023-01-01T00:00:00"
            },
            "recommendations": []
        })
        reporting_agent.agent.generate_response = AsyncMock(return_value=mock_response)
        
        # Generate the report synchronously
        result = reporting_agent.generate_report_sync("Test Fund")
        
        # Verify the result structure
        assert "report" in result
        assert result["report"] == mock_response
    
    def test_generate_insights_sync(self, reporting_agent):
        """
        Test synchronous wrapper for insights generation.
        
        This test verifies that the generate_insights_sync method provides
        a synchronous interface to the async generate_insights method.
        
        Args:
            reporting_agent: The test reporting agent instance
        """
        # Configure the mock agent's generate_response method
        mock_response = json.dumps({
            "opportunities": [
                "Diversify portfolio to reduce concentration risk"
            ],
            "risks": [],
            "holding_recommendations": [],
            "market_trends": [],
            "strategic_recommendations": []
        })
        reporting_agent.agent.generate_response = AsyncMock(return_value=mock_response)
        
        # Generate the insights synchronously
        result = reporting_agent.generate_insights_sync("Test Fund")
        
        # Verify the result structure
        assert "insights" in result
        assert result["insights"] == mock_response