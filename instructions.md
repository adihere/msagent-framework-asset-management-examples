Build a production-ready financial portfolio monitoring system using Microsoft Agent Framework with direct OpenAI API integration for local VS Code development.

📋 TASK SPECIFICATIONS
OBJECTIVE: Create a multi-agent orchestration system where an orchestrator agent coordinates with a reporting agent to perform automated financial portfolio scans, identify key news alerts, and analyze risk exposures for public equity assets managed by fund managers.​

ARCHITECTURE: Implement the three-layer design: (1) OpenAI API Integration Layer, (2) Microsoft Agent Framework Orchestration, (3) Multi-Agent System with Tool Functions.​

KEY AGENTS TO BUILD:

Portfolio Orchestrator Agent: Coordinates the complete workflow and provides executive summaries

Financial Reporting Agent: Performs detailed analysis, news scanning, and risk assessment with specialized tools

Tool Functions: Portfolio holdings retrieval, market news scanning, risk exposure analysis​

🛠️ TECHNICAL REQUIREMENTS
Framework: Microsoft Agent Framework (latest preview version)
LLM Provider: Direct OpenAI API (no Azure dependencies)
Language: Python 3.10+
Development Environment: Local VS Code with Kilo Code extension
Dependencies: agent-framework, openai, python-dotenv, pandas, asyncio​

Code Structure to Generate:

text
financial_portfolio_scanner/
├── main.py                    # Entry point and orchestrator
├── agents/
│   ├── orchestrator_agent.py  # Portfolio coordination agent
│   ├── reporting_agent.py     # Financial analysis agent
│   └── tool_functions.py      # External API integrations
├── config/
│   ├── settings.py            # Configuration management
│   └── .env.template          # Environment variables
├── requirements.txt           # Dependencies
└── README.md                  # Setup and usage guide
🔧 CORE IMPLEMENTATION PATTERNS
Agent Creation Pattern:

python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

def create_reporting_agent():
    agent = ChatAgent(
        chat_client=OpenAIChatClient(),
        name="FinancialReportingAgent",
        instructions="""You are a specialized financial reporting agent.
        
        Your responsibilities:
        - Retrieve portfolio holdings for funds
        - Scan market news and alerts for portfolio positions  
        - Analyze risk exposure and provide recommendations
        - Generate comprehensive financial reports
        """,
        tools=[get_portfolio_holdings, scan_market_news, analyze_risk_exposure]
    )
    return agent
Orchestration Workflow:

python
class PortfolioScanOrchestrator:
    async def scan_portfolio(self, fund_name: str) -> Dict:
        # Step 1: Get portfolio holdings
        portfolio_data = get_portfolio_holdings(fund_name)
        
        # Step 2: Extract tickers and scan news  
        tickers = [holding['ticker'] for holding in portfolio['holdings']]
        news_data = scan_market_news(tickers)
        
        # Step 3: Perform risk analysis
        risk_data = analyze_risk_exposure(portfolio_data, news_data)
        
        # Step 4: Generate comprehensive report
        report = await self.reporting_agent.run(f"""
        Generate comprehensive report for {fund_name}
        PORTFOLIO HOLDINGS: {portfolio_data}
        NEWS ALERTS: {news_data}  
        RISK ANALYSIS: {risk_data}
        """)
        
        return {"fund_name": fund_name, "report": report, "action_items": [...]}
💼 FINANCIAL TOOL FUNCTIONS
Portfolio Holdings Retrieval:

python
def get_portfolio_holdings(fund_name: str) -> str:
    """Retrieve current portfolio holdings for a fund."""
    # Mock data for development - replace with Bloomberg/FactSet APIs
    portfolio_data = {
        "fund_name": fund_name,
        "total_value": 168_000_000,
        "holdings": [
            {"ticker": "MSFT", "name": "Microsoft Corp", "weight": 0.15, "value": 25_200_000},
            {"ticker": "AAPL", "name": "Apple Inc", "weight": 0.12, "value": 20_160_000},
            {"ticker": "GOOGL", "name": "Alphabet Inc", "weight": 0.10, "value": 16_800_000},
            # Additional holdings...
        ],
        "sector_allocation": {"Technology": 0.45, "Healthcare": 0.20, "Finance": 0.35},
        "last_updated": "2025-10-18T14:30:00Z"
    }
    return json.dumps(portfolio_data)
Market News Scanning:

python
def scan_market_news(tickers: List[str]) -> str:
    """Scan for recent news and alerts for specified tickers."""
    # Mock alerts - replace with Finnhub/Reuters/Bloomberg APIs
    news_alerts = {
        "scan_timestamp": "2025-10-18T14:30:00Z",
        "alerts": [
            {
                "ticker": "MSFT",
                "alert_type": "EARNINGS_ANNOUNCEMENT", 
                "severity": "HIGH",
                "headline": "Microsoft Reports Strong Q3 Azure Growth",
                "sentiment": "POSITIVE",
                "impact_score": 0.85,
                "source": "Reuters"
            },
            {
                "ticker": "AAPL", 
                "alert_type": "REGULATORY",
                "severity": "MEDIUM",
                "headline": "EU Antitrust Investigation into App Store Policies",
                "sentiment": "NEGATIVE", 
                "impact_score": 0.45,
                "source": "Bloomberg"
            }
        ]
    }
    return json.dumps(news_alerts)
Risk Exposure Analysis:

python
def analyze_risk_exposure(portfolio_data: str, news_data: str) -> str:
    """Analyze risk exposure based on holdings and news."""
    # Parse inputs and perform analysis
    portfolio = json.loads(portfolio_data)
    news = json.loads(news_data)
    
    risk_analysis = {
        "overall_risk_level": "MEDIUM",
        "risk_score": 65,  # 0-100 scale
        "key_findings": [
            "High technology sector concentration (45%) creates sector risk",
            "Microsoft earnings positive catalyst reduces near-term volatility",
            "Apple regulatory concerns warrant monitoring"
        ],
        "action_items": [
            "Consider diversification into defensive sectors",
            "Monitor Apple regulatory developments",
            "Maintain overweight position in Microsoft post-earnings"
        ],
        "exposure_metrics": {
            "sector_concentration_risk": 0.72,
            "news_sentiment_impact": 0.15,
            "liquidity_risk": 0.23
        }
    }
    return json.dumps(risk_analysis)
⚙️ LOCAL DEVELOPMENT SETUP
Environment Configuration:

bash
# .env file for local development
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_CHAT_MODEL_ID=gpt-4o              # or gpt-4o-mini for cost efficiency
DEBUG_MODE=true
LOG_LEVEL=INFO

# Optional: Real financial data APIs (for production)
# FINNHUB_API_KEY=your_finnhub_key
# BLOOMBERG_API_KEY=your_bloomberg_key  
# FACTSET_API_KEY=your_factset_key
Installation Script:

bash
# setup.sh - Local development setup
#!/bin/bash

echo "🚀 Setting up Financial Portfolio Scanner..."

# Check Python version
python3 --version | grep -q "3.1[0-9]" || { echo "❌ Python 3.10+ required"; exit 1; }

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install --upgrade pip
pip install agent-framework --pre
pip install openai python-dotenv pandas asyncio-throttle

# Create .env from template
cp .env.template .env
echo "✅ Setup complete! Edit .env with your OpenAI API key"
echo "🔧 Run: python main.py to start the scanner"
Requirements.txt:

text
agent-framework>=1.0.0b251016
openai>=1.54.0  
python-dotenv>=1.0.0
pandas>=2.1.0
asyncio-throttle>=1.0.2
requests>=2.31.0
matplotlib>=3.7.0  # For optional visualizations
tabulate>=0.9.0    # For console output formatting
🧪 TESTING & VALIDATION
Quick Test Function:

python
async def test_portfolio_scan():
    """Quick test of the portfolio scanning system."""
    print("🧪 Testing Financial Portfolio Scanner...")
    
    orchestrator = PortfolioScanOrchestrator()
    result = await orchestrator.scan_portfolio("Tech Growth Fund")
    
    print(f"✅ Scan completed for: {result['fund_name']}")
    print(f"📊 Report generated: {len(result['report'])} characters")
    print(f"⚠️  Action items: {len(result['action_items'])}")
    
    return result

# Run test
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_portfolio_scan())
Usage Examples:

python
# Single portfolio scan
scanner = PortfolioScanOrchestrator()
result = await scanner.scan_portfolio("Growth Equity Fund")

# Batch processing multiple funds
funds = ["Tech Growth Fund", "Healthcare Alpha Fund", "ESG Balanced Fund"]
results = []
for fund in funds:
    result = await scanner.scan_portfolio(fund)
    results.append(result)
    await asyncio.sleep(2)  # Rate limiting

# Export results to CSV
df = pd.DataFrame(results)
df.to_csv("portfolio_scan_results.csv", index=False)
📈 PRODUCTION INTEGRATION POINTS
Financial Data Sources (Replace mock functions):

Portfolio APIs: Bloomberg Terminal API, FactSet API, internal portfolio systems

News Services: Finnhub Stock API, marketaux, Alpha Vantage News API, Reuters feeds

Risk Analytics: FactSet Risk API, MSCI RiskMetrics, internal quant models​

Real API Integration Example:

python
import requests

def scan_market_news_finnhub(tickers: List[str]) -> str:
    """Production news scanning with Finnhub API."""
    api_key = os.getenv("FINNHUB_API_KEY")
    news_data = []
    
    for ticker in tickers:
        response = requests.get(
            "https://finnhub.io/api/v1/company-news",
            params={
                "symbol": ticker,
                "from": "2025-10-01", 
                "to": "2025-10-18",
                "token": api_key
            }
        )
        news_data.extend(response.json())
    
    return json.dumps(news_data)
🔍 VS CODE + KILO CODE OPTIMIZATION
Kilo Code Mode Settings:

Use Code Mode for general implementation

Use Architect Mode for system design decisions

Use Debug Mode for troubleshooting agent interactions

Enable Auto-Approval for file operations during development​

Recommended VS Code Extensions:

Kilo Code AI Agent: Primary coding assistant

Python Extension: Language support

REST Client: For API testing

Azure Account: For future Azure integration​

Project Structure Commands:

bash
# Generate project structure
mkdir -p financial_portfolio_scanner/{agents,config,tests}
touch financial_portfolio_scanner/{main.py,requirements.txt,README.md}
touch financial_portfolio_scanner/agents/{__init__.py,orchestrator_agent.py,reporting_agent.py,tool_functions.py}
touch financial_portfolio_scanner/config/{settings.py,.env.template}

🎯 SUCCESS CRITERIA
Core Functionality:

 Orchestrator agent successfully coordinates workflow

 Reporting agent performs financial analysis with tools

 Tool functions retrieve portfolio, news, and risk data

 System generates comprehensive portfolio reports

 Local VS Code development environment fully functional


Advanced Features:

 Rate limiting and error handling implemented

 CSV export and data persistence working

 Multiple model support (GPT-4o vs GPT-4o-mini)

 Real-time news alerts and portfolio monitoring

 Integration tests and validation suite

Production Readiness:

 Environment configuration management

 API key security and validation

 Logging and monitoring capabilities

 Documentation and setup guides complete

