"""
Tests for the tool functions module.
"""

import json
import pytest
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.tool_functions import get_portfolio_holdings, scan_market_news, analyze_risk_exposure


def test_get_portfolio_holdings_valid_fund():
    """Test get_portfolio_holdings with a valid fund name."""
    fund_name = "Test Fund"
    result = get_portfolio_holdings(fund_name)
    
    # Verify the result is a string
    assert isinstance(result, str)
    
    # Verify the result can be parsed as JSON
    parsed_data = json.loads(result)
    
    # Verify the structure of the parsed data
    assert "fund_name" in parsed_data
    assert "total_value" in parsed_data
    assert "holdings" in parsed_data
    assert "sector_allocation" in parsed_data
    assert "last_updated" in parsed_data
    
    # Verify the fund name matches
    assert parsed_data["fund_name"] == fund_name
    
    # Verify holdings structure
    assert isinstance(parsed_data["holdings"], list)
    for holding in parsed_data["holdings"]:
        assert "ticker" in holding
        assert "name" in holding
        assert "weight" in holding
        assert "value" in holding
    
    # Verify sector allocation structure
    assert isinstance(parsed_data["sector_allocation"], list)
    for sector in parsed_data["sector_allocation"]:
        assert "sector" in sector
        assert "weight" in sector


def test_get_portfolio_holdings_empty_fund_name():
    """Test get_portfolio_holdings with an empty fund name."""
    with pytest.raises(ValueError, match="fund_name cannot be empty or contain only whitespace"):
        get_portfolio_holdings("")


def test_get_portfolio_holdings_whitespace_fund_name():
    """Test get_portfolio_holdings with a whitespace-only fund name."""
    with pytest.raises(ValueError, match="fund_name cannot be empty or contain only whitespace"):
        get_portfolio_holdings("   ")


def test_get_portfolio_holdings_non_string_input():
    """Test get_portfolio_holdings with a non-string input."""
    with pytest.raises(TypeError, match="fund_name must be a string"):
        get_portfolio_holdings(123)


def test_get_portfolio_holdings_none_input():
    """Test get_portfolio_holdings with None input."""
    with pytest.raises(TypeError, match="fund_name must be a string"):
        get_portfolio_holdings(None)


def test_scan_market_news_valid_tickers():
    """Test scan_market_news with valid tickers."""
    tickers = ["AAPL", "MSFT"]
    result = scan_market_news(tickers)
    
    # Verify the result is a string
    assert isinstance(result, str)
    
    # Verify the result can be parsed as JSON
    parsed_data = json.loads(result)
    
    # Verify the structure of the parsed data
    assert "scan_timestamp" in parsed_data
    assert "alerts" in parsed_data
    
    # Verify alerts structure
    assert isinstance(parsed_data["alerts"], list)
    for alert in parsed_data["alerts"]:
        assert "ticker" in alert
        assert "alert_type" in alert
        assert "severity" in alert
        assert "headline" in alert
        assert "sentiment" in alert
        assert "impact_score" in alert
        assert "source" in alert
    
    # Verify that alerts are generated for each ticker
    alert_tickers = {alert["ticker"] for alert in parsed_data["alerts"]}
    for ticker in tickers:
        assert ticker in alert_tickers


def test_scan_market_news_single_ticker():
    """Test scan_market_news with a single ticker."""
    tickers = ["AAPL"]
    result = scan_market_news(tickers)
    
    # Verify the result can be parsed as JSON
    parsed_data = json.loads(result)
    
    # Verify that alerts are generated for the ticker
    alert_tickers = {alert["ticker"] for alert in parsed_data["alerts"]}
    assert "AAPL" in alert_tickers
    
    # Verify specific AAPL alerts
    aapl_alerts = [alert for alert in parsed_data["alerts"] if alert["ticker"] == "AAPL"]
    assert len(aapl_alerts) == 2  # AAPL should have 2 mock alerts
    
    # Verify alert types for AAPL
    alert_types = {alert["alert_type"] for alert in aapl_alerts}
    assert "Earnings Report" in alert_types
    assert "Product Launch" in alert_types


def test_scan_market_news_unknown_ticker():
    """Test scan_market_news with an unknown ticker."""
    tickers = ["UNKNOWN"]
    result = scan_market_news(tickers)
    
    # Verify the result can be parsed as JSON
    parsed_data = json.loads(result)
    
    # Verify that alerts are generated for the ticker
    alert_tickers = {alert["ticker"] for alert in parsed_data["alerts"]}
    assert "UNKNOWN" in alert_tickers
    
    # Verify generic alert for unknown ticker
    unknown_alerts = [alert for alert in parsed_data["alerts"] if alert["ticker"] == "UNKNOWN"]
    assert len(unknown_alerts) == 1
    assert unknown_alerts[0]["alert_type"] == "Market Movement"
    assert unknown_alerts[0]["sentiment"] == "Neutral"


def test_scan_market_news_empty_list():
    """Test scan_market_news with an empty list."""
    with pytest.raises(ValueError, match="tickers list cannot be empty"):
        scan_market_news([])


def test_scan_market_news_non_list_input():
    """Test scan_market_news with a non-list input."""
    with pytest.raises(TypeError, match="tickers must be a list"):
        scan_market_news("AAPL")


def test_scan_market_news_list_with_non_string():
    """Test scan_market_news with a list containing non-string elements."""
    with pytest.raises(TypeError, match="All ticker symbols must be strings"):
        scan_market_news(["AAPL", 123])


def test_scan_market_news_list_with_empty_string():
    """Test scan_market_news with a list containing empty strings."""
    with pytest.raises(ValueError, match="Ticker symbols cannot be empty or contain only whitespace"):
        scan_market_news(["AAPL", ""])


def test_scan_market_news_list_with_whitespace_string():
    """Test scan_market_news with a list containing whitespace-only strings."""
    with pytest.raises(ValueError, match="Ticker symbols cannot be empty or contain only whitespace"):
        scan_market_news(["AAPL", "   "])


def test_analyze_risk_exposure_valid_inputs():
    """Test analyze_risk_exposure with valid portfolio and news data."""
    # Create mock portfolio data
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
    
    # Create mock news data
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
    
    # Convert to JSON strings
    portfolio_json = json.dumps(portfolio_data)
    news_json = json.dumps(news_data)
    
    # Call the function
    result = analyze_risk_exposure(portfolio_json, news_json)
    
    # Verify the result is a string
    assert isinstance(result, str)
    
    # Verify the result can be parsed as JSON
    parsed_data = json.loads(result)
    
    # Verify the structure of the parsed data
    assert "analysis_timestamp" in parsed_data
    assert "overall_risk_level" in parsed_data
    assert "risk_score" in parsed_data
    assert "key_findings" in parsed_data
    assert "action_items" in parsed_data
    assert "exposure_metrics" in parsed_data
    
    # Verify data types
    assert isinstance(parsed_data["overall_risk_level"], str)
    assert isinstance(parsed_data["risk_score"], (int, float))
    assert isinstance(parsed_data["key_findings"], list)
    assert isinstance(parsed_data["action_items"], list)
    assert isinstance(parsed_data["exposure_metrics"], dict)
    
    # Verify risk score is within expected range
    assert 0 <= parsed_data["risk_score"] <= 100
    
    # Verify overall risk level is one of the expected values
    assert parsed_data["overall_risk_level"] in ["Low", "Medium", "High", "Critical"]
    
    # Verify exposure metrics structure
    exposure_metrics = parsed_data["exposure_metrics"]
    assert "concentration_risk" in exposure_metrics
    assert "news_sentiment_impact" in exposure_metrics
    assert "volatility_exposure" in exposure_metrics
    assert "liquidity_risk" in exposure_metrics
    assert "market_risk" in exposure_metrics


def test_analyze_risk_exposure_empty_portfolio_data():
    """Test analyze_risk_exposure with empty portfolio data."""
    news_data = {
        "scan_timestamp": "2023-01-01T00:00:00",
        "alerts": []
    }
    news_json = json.dumps(news_data)
    
    with pytest.raises(ValueError, match="portfolio_data cannot be empty or contain only whitespace"):
        analyze_risk_exposure("", news_json)


def test_analyze_risk_exposure_whitespace_portfolio_data():
    """Test analyze_risk_exposure with whitespace-only portfolio data."""
    news_data = {
        "scan_timestamp": "2023-01-01T00:00:00",
        "alerts": []
    }
    news_json = json.dumps(news_data)
    
    with pytest.raises(ValueError, match="portfolio_data cannot be empty or contain only whitespace"):
        analyze_risk_exposure("   ", news_json)


def test_analyze_risk_exposure_empty_news_data():
    """Test analyze_risk_exposure with empty news data."""
    portfolio_data = {
        "fund_name": "Test Fund",
        "total_value": 1000000.00,
        "holdings": [],
        "sector_allocation": [],
        "last_updated": "2023-01-01T00:00:00"
    }
    portfolio_json = json.dumps(portfolio_data)
    
    with pytest.raises(ValueError, match="news_data cannot be empty or contain only whitespace"):
        analyze_risk_exposure(portfolio_json, "")


def test_analyze_risk_exposure_whitespace_news_data():
    """Test analyze_risk_exposure with whitespace-only news data."""
    portfolio_data = {
        "fund_name": "Test Fund",
        "total_value": 1000000.00,
        "holdings": [],
        "sector_allocation": [],
        "last_updated": "2023-01-01T00:00:00"
    }
    portfolio_json = json.dumps(portfolio_data)
    
    with pytest.raises(ValueError, match="news_data cannot be empty or contain only whitespace"):
        analyze_risk_exposure(portfolio_json, "   ")


def test_analyze_risk_exposure_non_string_portfolio_data():
    """Test analyze_risk_exposure with non-string portfolio data."""
    news_data = {
        "scan_timestamp": "2023-01-01T00:00:00",
        "alerts": []
    }
    news_json = json.dumps(news_data)
    
    with pytest.raises(TypeError, match="portfolio_data must be a string"):
        analyze_risk_exposure(123, news_json)


def test_analyze_risk_exposure_non_string_news_data():
    """Test analyze_risk_exposure with non-string news data."""
    portfolio_data = {
        "fund_name": "Test Fund",
        "total_value": 1000000.00,
        "holdings": [],
        "sector_allocation": [],
        "last_updated": "2023-01-01T00:00:00"
    }
    portfolio_json = json.dumps(portfolio_data)
    
    with pytest.raises(TypeError, match="news_data must be a string"):
        analyze_risk_exposure(portfolio_json, 123)


def test_analyze_risk_exposure_invalid_json_portfolio_data():
    """Test analyze_risk_exposure with invalid JSON portfolio data."""
    news_data = {
        "scan_timestamp": "2023-01-01T00:00:00",
        "alerts": []
    }
    news_json = json.dumps(news_data)
    
    with pytest.raises(RuntimeError, match="Failed to parse JSON input"):
        analyze_risk_exposure("{invalid json", news_json)


def test_analyze_risk_exposure_invalid_json_news_data():
    """Test analyze_risk_exposure with invalid JSON news data."""
    portfolio_data = {
        "fund_name": "Test Fund",
        "total_value": 1000000.00,
        "holdings": [],
        "sector_allocation": [],
        "last_updated": "2023-01-01T00:00:00"
    }
    portfolio_json = json.dumps(portfolio_data)
    
    with pytest.raises(RuntimeError, match="Failed to parse JSON input"):
        analyze_risk_exposure(portfolio_json, "{invalid json")


def test_analyze_risk_exposure_high_risk_scenario():
    """Test analyze_risk_exposure with a high-risk scenario."""
    # Create portfolio with few holdings (concentration risk)
    portfolio_data = {
        "fund_name": "High Risk Fund",
        "total_value": 1000000.00,
        "holdings": [
            {
                "ticker": "AAPL",
                "name": "Apple Inc.",
                "weight": 50.0,
                "value": 500000.00
            }
        ],
        "sector_allocation": [
            {
                "sector": "Technology",
                "weight": 100.0
            }
        ],
        "last_updated": "2023-01-01T00:00:00"
    }
    
    # Create news with negative sentiment
    news_data = {
        "scan_timestamp": "2023-01-01T00:00:00",
        "alerts": [
            {
                "ticker": "AAPL",
                "alert_type": "Regulatory",
                "severity": "High",
                "headline": "Apple Faces Major Regulatory Challenges",
                "sentiment": "Negative",
                "impact_score": -0.9,
                "source": "Financial Times"
            },
            {
                "ticker": "AAPL",
                "alert_type": "Legal",
                "severity": "High",
                "headline": "Apple Hit with Record Fine in EU Antitrust Case",
                "sentiment": "Negative",
                "impact_score": -0.85,
                "source": "Wall Street Journal"
            },
            {
                "ticker": "AAPL",
                "alert_type": "Market",
                "severity": "High",
                "headline": "Apple Stock Plummets on Earnings Miss",
                "sentiment": "Negative",
                "impact_score": -0.8,
                "source": "Bloomberg"
            }
        ]
    }
    
    # Convert to JSON strings
    portfolio_json = json.dumps(portfolio_data)
    news_json = json.dumps(news_data)
    
    # Call the function
    result = analyze_risk_exposure(portfolio_json, news_json)
    
    # Verify the result can be parsed as JSON
    parsed_data = json.loads(result)
    
    # Verify high risk level
    assert parsed_data["overall_risk_level"] in ["High", "Critical"]
    assert parsed_data["risk_score"] >= 50
    
    # Verify key findings include risk indicators
    key_findings = parsed_data["key_findings"]
    assert any("risk exposure" in finding for finding in key_findings)
    
    # Verify action items include risk mitigation
    action_items = parsed_data["action_items"]
    assert any("risk mitigation" in item for item in action_items)


def test_analyze_risk_exposure_low_risk_scenario():
    """Test analyze_risk_exposure with a low-risk scenario."""
    # Create portfolio with many holdings (well-diversified)
    portfolio_data = {
        "fund_name": "Low Risk Fund",
        "total_value": 1000000.00,
        "holdings": [
            {
                "ticker": "AAPL",
                "name": "Apple Inc.",
                "weight": 8.0,
                "value": 80000.00
            },
            {
                "ticker": "MSFT",
                "name": "Microsoft Corporation",
                "weight": 7.5,
                "value": 75000.00
            },
            {
                "ticker": "GOOGL",
                "name": "Alphabet Inc.",
                "weight": 7.0,
                "value": 70000.00
            },
            {
                "ticker": "AMZN",
                "name": "Amazon.com Inc.",
                "weight": 6.5,
                "value": 65000.00
            },
            {
                "ticker": "JPM",
                "name": "JPMorgan Chase & Co.",
                "weight": 6.0,
                "value": 60000.00
            },
            {
                "ticker": "V",
                "name": "Visa Inc.",
                "weight": 5.5,
                "value": 55000.00
            },
            {
                "ticker": "JNJ",
                "name": "Johnson & Johnson",
                "weight": 5.0,
                "value": 50000.00
            },
            {
                "ticker": "PG",
                "name": "Procter & Gamble Co.",
                "weight": 4.5,
                "value": 45000.00
            }
        ],
        "sector_allocation": [
            {
                "sector": "Technology",
                "weight": 25.0
            },
            {
                "sector": "Financials",
                "weight": 15.0
            },
            {
                "sector": "Healthcare",
                "weight": 12.0
            },
            {
                "sector": "Consumer Staples",
                "weight": 10.0
            },
            {
                "sector": "Industrials",
                "weight": 8.0
            },
            {
                "sector": "Energy",
                "weight": 7.0
            },
            {
                "sector": "Utilities",
                "weight": 6.0
            },
            {
                "sector": "Real Estate",
                "weight": 5.0
            },
            {
                "sector": "Materials",
                "weight": 4.0
            },
            {
                "sector": "Communication Services",
                "weight": 8.0
            }
        ],
        "last_updated": "2023-01-01T00:00:00"
    }
    
    # Create news with positive sentiment
    news_data = {
        "scan_timestamp": "2023-01-01T00:00:00",
        "alerts": [
            {
                "ticker": "AAPL",
                "alert_type": "Earnings",
                "severity": "Medium",
                "headline": "Apple Reports Record Quarterly Revenue",
                "sentiment": "Positive",
                "impact_score": 0.8,
                "source": "Financial Times"
            },
            {
                "ticker": "MSFT",
                "alert_type": "Product",
                "severity": "Medium",
                "headline": "Microsoft Launches Innovative Cloud Solution",
                "sentiment": "Positive",
                "impact_score": 0.75,
                "source": "TechCrunch"
            },
            {
                "ticker": "JNJ",
                "alert_type": "Regulatory",
                "severity": "Medium",
                "headline": "Johnson & Johnson Receives FDA Approval for New Drug",
                "sentiment": "Positive",
                "impact_score": 0.7,
                "source": "Reuters"
            }
        ]
    }
    
    # Convert to JSON strings
    portfolio_json = json.dumps(portfolio_data)
    news_json = json.dumps(news_data)
    
    # Call the function
    result = analyze_risk_exposure(portfolio_json, news_json)
    
    # Verify the result can be parsed as JSON
    parsed_data = json.loads(result)
    
    # Verify low risk level
    assert parsed_data["overall_risk_level"] in ["Low", "Medium"]
    assert parsed_data["risk_score"] < 50
    
    # Verify key findings include low risk indicators
    key_findings = parsed_data["key_findings"]
    assert any("Low risk exposure" in finding or "adequate diversification" in finding for finding in key_findings)
    
    # Verify action items include growth opportunities
    action_items = parsed_data["action_items"]
    assert any("strategic growth" in item for item in action_items)