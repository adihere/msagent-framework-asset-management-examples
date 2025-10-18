# Financial Portfolio Scanner

A comprehensive financial portfolio monitoring system that leverages AI agents to track, analyze, and provide insights on investment portfolios. The system performs automated portfolio scanning, risk assessment, market news analysis, and generates actionable recommendations for portfolio optimization.

## Architecture Overview

The Financial Portfolio Scanner is built on a three-layer architecture designed for scalability, maintainability, and extensibility:

### 1. Presentation Layer
- **Entry Point**: [`main.py`](financial_portfolio_scanner/main.py:1) serves as the primary interface for the application
- **Command-Line Interface**: Provides various options for single portfolio scans, batch processing, and CSV export
- **Demo Interface**: [`demo_portfolio_holdings.py`](financial_portfolio_scanner/demo_portfolio_holdings.py:1) for showcasing portfolio holdings functionality

### 2. Agent Layer
- **Orchestrator Agent**: [`orchestrator_agent.py`](financial_portfolio_scanner/agents/orchestrator_agent.py:1) coordinates the entire portfolio scanning workflow
- **Reporting Agent**: [`reporting_agent.py`](financial_portfolio_scanner/agents/reporting_agent.py:1) generates detailed financial reports with insights
- **Tool Functions**: [`tool_functions.py`](financial_portfolio_scanner/agents/tool_functions.py:1) provides utility functions for portfolio data retrieval, market news scanning, and risk analysis

### 3. Configuration Layer
- **Settings Management**: [`settings.py`](financial_portfolio_scanner/config/settings.py:1) handles all configuration settings
- **Environment Variables**: `.env` file for secure API key storage and configuration
- **Template Configuration**: [`.env.template`](financial_portfolio_scanner/config/.env.template:1) for easy setup

## Key Agents and Their Responsibilities

### PortfolioScanOrchestrator
The [`PortfolioScanOrchestrator`](financial_portfolio_scanner/agents/orchestrator_agent.py:22) class coordinates the entire portfolio scanning workflow:

- **Portfolio Data Retrieval**: Fetches portfolio holdings using [`get_portfolio_holdings()`](financial_portfolio_scanner/agents/tool_functions.py:58)
- **Market News Scanning**: Scans relevant market news for portfolio tickers using [`scan_market_news()`](financial_portfolio_scanner/agents/tool_functions.py:154)
- **Risk Analysis**: Analyzes risk exposure based on portfolio data and market news using [`analyze_risk_exposure()`](financial_portfolio_scanner/agents/tool_functions.py:295)
- **Report Generation**: Coordinates with the ReportingAgent to generate comprehensive reports
- **Summary Generation**: Provides quick portfolio summaries without full scans
- **Risk Assessment**: Delivers focused risk analysis for portfolio holdings

### ReportingAgent
The [`ReportingAgent`](financial_portfolio_scanner/agents/reporting_agent.py:177) class is responsible for generating detailed financial reports:

- **Comprehensive Reports**: Generates in-depth portfolio analysis with actionable insights
- **Market Insights**: Analyzes market news and its potential impact on portfolio holdings
- **Risk Assessment**: Provides detailed risk analysis and exposure metrics
- **Recommendations**: Offers actionable recommendations for portfolio optimization
- **Data-Driven Analysis**: Uses AI-powered analysis to support all insights and recommendations

## Technical Requirements

### System Requirements
- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: Minimum 100MB free disk space

### Python Dependencies
All required packages are listed in [`requirements.txt`](financial_portfolio_scanner/requirements.txt:1):

```
# Microsoft Agent Framework for building AI agents
agent-framework>=1.0.0b251016

# OpenAI API integration for AI capabilities
openai>=1.54.0

# Environment variable management for configuration
python-dotenv>=1.0.0

# Data manipulation and CSV export functionality
pandas>=2.1.0

# Rate limiting for API calls
asyncio-throttle>=1.0.2

# HTTP requests for API integration
requests>=2.31.0

# For optional visualizations and charts
matplotlib>=3.7.0

# For console output formatting
tabulate>=0.9.0

# Testing framework
pytest>=6.2.5
pytest-cov>=2.12.0
```

### API Requirements
- **OpenAI API Key**: Required for AI-powered analysis and report generation
- **Optional Financial Data APIs**: 
  - Finnhub API (optional)
  - Bloomberg API (optional)
  - FactSet API (optional)

## Installation Instructions

### Prerequisites
Before installing the Financial Portfolio Scanner, ensure you have Python 3.10 or higher installed on your system. You can check your Python version with:

```bash
python --version
```

### Step 1: Clone the Repository
Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/financial-portfolio-scanner.git
cd financial-portfolio-scanner
```

### Step 2: Create and Activate a Virtual Environment
Create a virtual environment to isolate the project dependencies:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file from the template and configure your API keys:

```bash
cp config/.env.template config/.env
```

Then edit the `.env` file to add your API keys (see Configuration Guide section below).

### Step 5: Verify Installation
Run the demo script to verify that the installation was successful:

```bash
python demo_portfolio_holdings.py
```

If the installation was successful, you should see sample portfolio holdings displayed.

## Configuration Guide

### Setting Up the .env File
The system uses environment variables for configuration. Copy the [`.env.template`](financial_portfolio_scanner/config/.env.template:1) to create a `.env` file:

```bash
cp config/.env.template config/.env
```

### Required Configuration
The following configuration parameters are required:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_CHAT_MODEL_ID=gpt-4o

# Application Configuration
DEBUG_MODE=true

# Logging Configuration
LOG_LEVEL=INFO
```

### Optional Configuration
The following parameters are optional but recommended for enhanced functionality:

```bash
# Optional Financial Data API Keys
FINNHUB_API_KEY=your_finnhub_api_key_here
BLOOMBERG_API_KEY=your_bloomberg_api_key_here
FACTSET_API_KEY=your_factset_api_key_here

# API Configuration
API_KEY=your_api_key_here
API_BASE_URL=https://api.example.com

# Database Configuration
DATABASE_URL=sqlite:///portfolio.db

# Portfolio Configuration
PORTFOLIO_UPDATE_INTERVAL=3600  # seconds

# Reporting Configuration
REPORT_FORMAT=pdf
REPORT_OUTPUT_DIR=./reports

# Logging Configuration
LOG_FILE=portfolio_scanner.log
```

### Obtaining and Setting Up OpenAI API Key
To use the AI-powered features of the Financial Portfolio Scanner, you need an OpenAI API key:

1. **Sign Up for OpenAI**: If you don't already have an account, sign up at [OpenAI's website](https://openai.com/)

2. **Get Your API Key**: 
   - Log in to your OpenAI account
   - Navigate to the API keys section
   - Create a new API key
   - Copy the key for use in the configuration

3. **Add API Key to .env File**:
   ```bash
   OPENAI_API_KEY=sk-your-api-key-here
   ```

4. **Verify API Key Setup**:
   Run a test scan to verify that your API key is working correctly:
   ```bash
   python main.py --test
   ```

## Usage Examples

### Basic Usage
Run the main application to perform a comprehensive portfolio scan with the default "Tech Growth Fund":

```bash
python main.py
```

This will:
1. Scan a sample portfolio (Tech Growth Fund)
2. Generate a comprehensive report
3. Provide a portfolio summary
4. Perform a risk assessment

### Single Portfolio Scan
Scan a specific portfolio by providing the fund name:

```bash
python main.py --fund "Your Fund Name"
```

Example:
```bash
python main.py --fund "Growth Equity Fund"
```

### Batch Processing
Process multiple portfolios in batch by providing multiple fund names:

```bash
python main.py --funds "Fund 1" "Fund 2" "Fund 3"
```

Example:
```bash
python main.py --funds "Tech Growth Fund" "Value Equity Fund" "Balanced Portfolio"
```

### Exporting Results to CSV
Export scan results to a CSV file for further analysis:

```bash
python main.py --fund "Your Fund Name" --export results.csv
```

For batch processing:
```bash
python main.py --funds "Fund 1" "Fund 2" --export batch_results.csv
```

### Test Mode
Run a test portfolio scan to verify system functionality:

```bash
python main.py --test
```

### Programmatic Usage
You can also use the orchestrator agent programmatically:

```python
import asyncio
from agents.orchestrator_agent import PortfolioScanOrchestrator

async def main():
    # Initialize the orchestrator
    orchestrator = PortfolioScanOrchestrator()
    
    # Perform a comprehensive portfolio scan
    scan_result = await orchestrator.scan_portfolio("Your Fund Name")
    
    # Get a portfolio summary (without full scan)
    summary = orchestrator.get_portfolio_summary("Your Fund Name")
    
    # Get a risk assessment (without full scan)
    risk_assessment = orchestrator.get_portfolio_risk_assessment("Your Fund Name")

asyncio.run(main())
```

## Project Structure

```
financial_portfolio_scanner/
├── agents/                    # Agent implementations
│   ├── __init__.py
│   ├── orchestrator_agent.py  # Main orchestrator agent
│   ├── reporting_agent.py     # Report generation agent
│   └── tool_functions.py     # Utility functions for agents
├── config/                    # Configuration files
│   ├── settings.py            # Settings management
│   ├── .env                   # Environment variables (API keys, etc.)
│   └── .env.template          # Template for .env file
├── tests/                     # Test files
│   ├── __init__.py
│   ├── test_tool_functions.py
│   └── test_orchestrator_agent.py
├── demo_portfolio_holdings.py # Demo data generator
├── main.py                    # Entry point
├── run_tests.py               # Test runner script
└── requirements.txt           # Project dependencies
```

### Key Components

#### Agents Directory
- **[`orchestrator_agent.py`](financial_portfolio_scanner/agents/orchestrator_agent.py:1)**: Contains the `PortfolioScanOrchestrator` class that coordinates the entire portfolio scanning workflow
- **[`reporting_agent.py`](financial_portfolio_scanner/agents/reporting_agent.py:1)**: Contains the `ReportingAgent` class that generates detailed financial reports
- **[`tool_functions.py`](financial_portfolio_scanner/agents/tool_functions.py:1)**: Contains utility functions for portfolio data retrieval, market news scanning, and risk analysis

#### Config Directory
- **[`settings.py`](financial_portfolio_scanner/config/settings.py:1)**: Manages all configuration settings and provides validation
- **[`.env`](financial_portfolio_scanner/config/.env:1)**: Stores environment variables including API keys
- **[`.env.template`](financial_portfolio_scanner/config/.env.template:1)**: Template for creating the .env file

#### Tests Directory
- **[`test_tool_functions.py`](financial_portfolio_scanner/tests/test_tool_functions.py:1)**: Tests for utility functions
- **[`test_orchestrator_agent.py`](financial_portfolio_scanner/tests/test_orchestrator_agent.py:1)**: Tests for the orchestrator agent

#### Test Runner
- **[`run_tests.py`](financial_portfolio_scanner/run_tests.py:1)**: Comprehensive test runner script with various options for test configuration, including verbose output, coverage reporting, and CI/CD integration

## Testing Instructions

### Using the Test Runner Script
The project includes a comprehensive test runner script ([`run_tests.py`](financial_portfolio_scanner/run_tests.py:1)) that simplifies test execution and provides various options for test configuration.

#### Basic Usage
Run all tests with the default settings:

```bash
python run_tests.py
```

#### Verbose Output
Enable verbose output for more detailed test information:

```bash
python run_tests.py --verbose
```

#### Running Tests with Coverage
Generate a coverage report to analyze test coverage:

```bash
python run_tests.py --coverage
```

You can specify the coverage report format:
```bash
python run_tests.py --coverage --cov-report html
```

Available coverage report formats:
- `term` (default): Terminal output
- `html`: HTML report
- `xml`: XML report for CI/CD integration

#### Running Specific Tests
Run tests matching a specific keyword expression:

```bash
python run_tests.py --keyword "test_get_portfolio_holdings"
```

#### Stop on First Failure
Stop test execution on the first failure:

```bash
python run_tests.py --stop-on-fail
```

#### Custom Test Path
Specify a custom path for the test directory:

```bash
python run_tests.py --test-path custom_tests/
```

#### All Available Options
```bash
python run_tests.py --help
```

### Direct pytest Usage
You can also use pytest directly if you prefer:

#### Running the Test Suite
Execute the test suite using pytest:

```bash
python -m pytest tests/ -v
```

#### Running Specific Tests
To run tests for a specific file:

```bash
python -m pytest tests/test_tool_functions.py -v
```

or

```bash
python -m pytest tests/test_orchestrator_agent.py -v
```

#### Running Tests with Coverage
To run tests with coverage report:

```bash
python -m pytest tests/ --cov=agents --cov-report=html
```

### Test Coverage
The test suite covers:
- Tool functions for portfolio data retrieval
- Market news scanning functionality
- Risk analysis calculations
- Orchestrator agent workflows
- Error handling and edge cases

## Production Integration Points

### API Integration
The system is designed to integrate with various financial data APIs:

1. **OpenAI API**: For AI-powered analysis and report generation
2. **Financial Data APIs**: Optional integration with:
   - Finnhub for real-time market data
   - Bloomberg for financial news and analytics
   - FactSet for portfolio analytics

### Database Integration
The system supports database integration for storing portfolio data and analysis results:

```python
# Example database configuration
DATABASE_URL=postgresql://username:password@localhost/portfolio_db
```

### Web Service Integration
The system can be integrated with web services for:

1. **Real-time Data Feeds**: Continuous portfolio monitoring
2. **Notification Systems**: Email/SMS alerts for critical portfolio changes
3. **Dashboard Integration**: Web-based portfolio visualization

### Batch Processing Integration
For large-scale portfolio management, the system supports:

1. **Scheduled Scans**: Automated portfolio analysis at regular intervals
2. **Batch Processing**: Efficient processing of multiple portfolios
3. **Result Export**: Automated export of results to various formats

### Cloud Deployment
The system can be deployed to cloud platforms:

1. **Containerization**: Docker support for easy deployment
2. **Cloud Services**: AWS, Azure, or GCP deployment
3. **Scalability**: Horizontal scaling for handling large volumes of portfolios

## Troubleshooting

### Common Issues and Solutions

#### 1. OpenAI API Key Issues
**Problem**: Error messages related to API authentication or quota limits.

**Solution**:
- Verify your OpenAI API key is correctly set in the `.env` file
- Check your OpenAI account for quota limits and billing status
- Ensure your API key has the necessary permissions

```bash
# Check if API key is set correctly
echo $OPENAI_API_KEY
```

#### 2. Python Version Compatibility
**Problem**: Import errors or compatibility issues with Python versions.

**Solution**:
- Ensure you're using Python 3.10 or higher
- Create a fresh virtual environment with the correct Python version
- Reinstall dependencies in the new environment

```bash
# Check Python version
python --version

# Create new virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Missing Dependencies
**Problem**: Module not found errors when running the application.

**Solution**:
- Install all required dependencies from requirements.txt
- Check for any conflicting packages in your environment

```bash
# Install dependencies
pip install -r requirements.txt

# Check for conflicting packages
pip list
```

#### 4. Configuration Issues
**Problem**: Application fails to start or behaves unexpectedly due to configuration issues.

**Solution**:
- Verify your `.env` file is correctly formatted
- Check for missing required configuration parameters
- Validate settings using the built-in validation

```bash
# Validate settings
python -c "from config.settings import Settings; Settings.validate_settings()"
```

#### 5. Portfolio Data Issues
**Problem**: Errors when retrieving or analyzing portfolio data.

**Solution**:
- Check the format of your portfolio data
- Verify that required fields are present in your data
- Review error logs for specific issues

```bash
# Run demo to check basic functionality
python demo_portfolio_holdings.py
```

#### 6. Export Issues
**Problem**: Problems when exporting results to CSV or other formats.

**Solution**:
- Ensure you have write permissions in the output directory
- Check that the output file path is valid
- Verify that pandas is correctly installed

```bash
# Test pandas installation
python -c "import pandas as pd; print('Pandas version:', pd.__version__)"
```

### Debug Mode
Enable debug mode for more detailed error messages and logging:

```bash
# Set debug mode in .env file
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

### Logging
Check the log files for detailed error information:

```bash
# View log file
tail -f portfolio_scanner.log
```

### Getting Help
If you encounter issues not covered in this troubleshooting guide:

1. Check the project documentation and issue tracker
2. Review the code comments for additional context
3. Enable debug logging for more detailed error information
4. Contact the development team with details about your issue

## Interpreting Results

### Understanding Portfolio Scan Results
The portfolio scan results include several key components:

#### 1. Fund Information
- **Fund Name**: The name of the analyzed fund
- **Total Value**: The total value of the portfolio
- **Holdings Count**: The number of holdings in the portfolio
- **Last Updated**: When the portfolio data was last updated

#### 2. Holdings Analysis
- **Ticker**: The stock ticker symbol
- **Name**: The full name of the holding
- **Weight**: The percentage weight of the holding in the portfolio
- **Value**: The monetary value of the holding

#### 3. Sector Allocation
- **Sector**: The sector classification
- **Weight**: The percentage weight of the sector in the portfolio

#### 4. Risk Assessment
- **Overall Risk Level**: Categorical risk assessment (Low, Medium, High, Critical)
- **Risk Score**: Numerical risk score (0-100)
- **Key Findings**: Important observations from the risk analysis
- **Action Items**: Recommended actions to mitigate risk

#### 5. Market Insights
- **News Alerts**: Relevant news items for portfolio holdings
- **Sentiment Analysis**: Sentiment assessment of news items
- **Impact Score**: Estimated impact of news on portfolio performance

### Understanding CSV Export Format
The CSV export includes the following columns:

- **Fund Name**: The name of the analyzed fund
- **Report Length**: The length of the generated report in characters
- **Action Item Number**: The sequential number of the action item
- **Action Item**: The specific action item recommendation

### Using Results for Portfolio Management
The scan results provide actionable insights for portfolio management:

1. **Risk Mitigation**: Address high-risk holdings and concentration issues
2. **Diversification**: Improve portfolio diversification based on sector allocation
3. **Opportunity Identification**: Capitalize on positive market sentiment and news
4. **Performance Optimization**: Rebalance portfolio based on recommendations

## Future Enhancements

The Financial Portfolio Scanner is designed for continuous improvement and expansion. Planned enhancements include:

### Feature Enhancements
- Integration with real financial data APIs
- Support for multiple portfolio types and structures
- Advanced risk modeling and simulation
- Real-time portfolio monitoring and alerts
- Web-based dashboard for portfolio visualization
- Email/SMS notifications for critical alerts

### Technical Improvements
- Enhanced AI models for more accurate analysis
- Improved performance for large-scale portfolio processing
- Expanded database support for portfolio data storage
- Cloud-native deployment options
- Advanced security features for sensitive financial data

### Integration Opportunities
- Integration with popular trading platforms
- API endpoints for third-party applications
- Plugin architecture for custom analysis modules
- Support for international markets and currencies
- Multi-language support for global users

## Contributing

We welcome contributions to the Financial Portfolio Scanner project. If you're interested in contributing:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

Please ensure all contributions follow the project's coding standards and include appropriate documentation.

## License

This project is licensed under the MIT License. See the LICENSE file for details.