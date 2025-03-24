import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf

# Set page configuration
st.set_page_config(
    page_title="DAJANIII Portfolio Manager",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #6200ee;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 1rem;
        color: #666;
    }
    .positive {
        color: #4caf50;
    }
    .negative {
        color: #f44336;
    }
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
    }
    .stButton>button {
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("# 🧠 DAJANIII")
st.sidebar.markdown("## Portfolio Manager")

# Navigation options
page = st.sidebar.radio(
    "Navigate to",
    ["Dashboard", "Holdings", "Charts", "Stock Analysis", "AI Assistant", "Upload"]
)

# Mock data for demonstration
def generate_mock_portfolio_data():
    accounts = ["Schwab", "Interactive Brokers", "Robinhood", "Combined"]
    
    portfolio_data = {
        "Schwab": {
            "symbols": 12,
            "cost_basis": 45000,
            "market_value": 52000,
            "day_change_pct": 1.2,
            "unrealized_gain": 7000,
            "realized_gain": 3500,
            "holdings": [
                {"ticker": "AAPL", "quantity": 25, "cost_basis": 3750, "market_value": 4385, "day_change_pct": 1.35, "total_gain_loss": 635},
                {"ticker": "MSFT", "quantity": 15, "cost_basis": 4500, "market_value": 4878, "day_change_pct": 1.32, "total_gain_loss": 378},
                {"ticker": "GOOGL", "quantity": 10, "cost_basis": 2800, "market_value": 2768, "day_change_pct": -0.86, "total_gain_loss": -32},
                {"ticker": "AMZN", "quantity": 8, "cost_basis": 2400, "market_value": 2680, "day_change_pct": 0.95, "total_gain_loss": 280},
                {"ticker": "TSLA", "quantity": 12, "cost_basis": 3000, "market_value": 2880, "day_change_pct": -1.25, "total_gain_loss": -120}
            ]
        },
        "Interactive Brokers": {
            "symbols": 8,
            "cost_basis": 35000,
            "market_value": 38500,
            "day_change_pct": 0.8,
            "unrealized_gain": 3500,
            "realized_gain": 1800,
            "holdings": [
                {"ticker": "NVDA", "quantity": 20, "cost_basis": 5000, "market_value": 5800, "day_change_pct": 2.1, "total_gain_loss": 800},
                {"ticker": "AMD", "quantity": 30, "cost_basis": 3600, "market_value": 3900, "day_change_pct": 1.5, "total_gain_loss": 300},
                {"ticker": "INTC", "quantity": 40, "cost_basis": 2000, "market_value": 1920, "day_change_pct": -0.8, "total_gain_loss": -80},
                {"ticker": "META", "quantity": 15, "cost_basis": 4500, "market_value": 4950, "day_change_pct": 1.2, "total_gain_loss": 450}
            ]
        },
        "Robinhood": {
            "symbols": 5,
            "cost_basis": 10000,
            "market_value": 10800,
            "day_change_pct": 1.5,
            "unrealized_gain": 800,
            "realized_gain": 500,
            "holdings": [
                {"ticker": "DIS", "quantity": 15, "cost_basis": 2250, "market_value": 2400, "day_change_pct": 0.9, "total_gain_loss": 150},
                {"ticker": "NFLX", "quantity": 5, "cost_basis": 2500, "market_value": 2650, "day_change_pct": 1.2, "total_gain_loss": 150},
                {"ticker": "SBUX", "quantity": 20, "cost_basis": 1800, "market_value": 1880, "day_change_pct": 0.7, "total_gain_loss": 80}
            ]
        }
    }
    
    # Create combined portfolio
    combined_holdings = []
    for account in ["Schwab", "Interactive Brokers", "Robinhood"]:
        for holding in portfolio_data[account]["holdings"]:
            holding_copy = holding.copy()
            holding_copy["account"] = account
            combined_holdings.append(holding_copy)
    
    portfolio_data["Combined"] = {
        "symbols": sum(portfolio_data[account]["symbols"] for account in ["Schwab", "Interactive Brokers", "Robinhood"]),
        "cost_basis": sum(portfolio_data[account]["cost_basis"] for account in ["Schwab", "Interactive Brokers", "Robinhood"]),
        "market_value": sum(portfolio_data[account]["market_value"] for account in ["Schwab", "Interactive Brokers", "Robinhood"]),
        "day_change_pct": 1.1,  # Average
        "unrealized_gain": sum(portfolio_data[account]["unrealized_gain"] for account in ["Schwab", "Interactive Brokers", "Robinhood"]),
        "realized_gain": sum(portfolio_data[account]["realized_gain"] for account in ["Schwab", "Interactive Brokers", "Robinhood"]),
        "holdings": combined_holdings
    }
    
    return portfolio_data

# Generate performance data for charts
def generate_performance_data(timerange="1Y"):
    dates = []
    portfolio_values = []
    spy_values = []
    nasdaq_values = []
    
    if timerange == "5D":
        start_date = datetime.now() - timedelta(days=5)
        for i in range(5):
            dates.append((start_date + timedelta(days=i)).strftime("%Y-%m-%d"))
        portfolio_values = [100, 101.2, 100.8, 102.5, 103.7]
        spy_values = [100, 100.5, 100.2, 101.3, 101.8]
        nasdaq_values = [100, 101.8, 101.2, 103.1, 104.2]
    elif timerange == "1M":
        start_date = datetime.now() - timedelta(days=30)
        for i in range(0, 30, 7):
            dates.append((start_date + timedelta(days=i)).strftime("%Y-%m-%d"))
        portfolio_values = [100, 103.5, 105.2, 108.7]
        spy_values = [100, 101.8, 103.2, 104.5]
        nasdaq_values = [100, 104.2, 106.5, 109.8]
    elif timerange == "6M":
        start_date = datetime.now() - timedelta(days=180)
        for i in range(0, 180, 30):
            dates.append((start_date + timedelta(days=i)).strftime("%Y-%m-%d"))
        portfolio_values = [100, 105, 103, 107, 110, 115]
        spy_values = [100, 102, 104, 103, 106, 108]
        nasdaq_values = [100, 106, 104, 109, 112, 118]
    elif timerange == "1Y":
        start_date = datetime.now() - timedelta(days=365)
        for i in range(0, 365, 30):
            dates.append((start_date + timedelta(days=i)).strftime("%Y-%m-%d"))
        portfolio_values = [100, 103, 107, 110, 112, 115, 113, 118, 122, 125, 128, 132]
        spy_values = [100, 102, 104, 105, 107, 108, 106, 109, 111, 113, 115, 117]
        nasdaq_values = [100, 104, 108, 112, 115, 119, 116, 122, 126, 130, 134, 138]
    
    return dates, portfolio_values, spy_values, nasdaq_values

# Dashboard page
def show_dashboard():
    st.markdown('<div class="main-header">Portfolio Dashboard</div>', unsafe_allow_html=True)
    
    # Get portfolio data
    portfolio_data = generate_mock_portfolio_data()
    
    # Account selection
    account_options = list(portfolio_data.keys())
    selected_account = st.selectbox("Select Account", account_options, index=account_options.index("Combined"))
    
    account_data = portfolio_data[selected_account]
    
    # Key statistics
    st.markdown('<div class="sub-header">Key Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="stat-label">Number of Symbols</div>
            <div class="stat-value">{account_data["symbols"]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="stat-label">Cost Basis</div>
            <div class="stat-value">${account_data["cost_basis"]:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="stat-label">Market Value</div>
            <div class="stat-value">${account_data["market_value"]:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        gain_loss = account_data["market_value"] - account_data["cost_basis"]
        gain_loss_pct = (gain_loss / account_data["cost_basis"]) * 100
        color_class = "positive" if gain_loss >= 0 else "negative"
        sign = "+" if gain_loss >= 0 else ""
        
        st.markdown(f"""
        <div class="card">
            <div class="stat-label">Unrealized Gain/Loss</div>
            <div class="stat-value {color_class}">{sign}${gain_loss:,.2f} ({sign}{gain_loss_pct:.2f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance chart
    st.markdown('<div class="sub-header">Performance</div>', unsafe_allow_html=True)
    
    timerange_options = ["5D", "1M", "6M", "1Y"]
    timerange = st.select_slider("Time Period", options=timerange_options, value="1M")
    
    dates, portfolio_values, spy_values, nasdaq_values = generate_performance_data(timerange)
    
    # Create performance chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=portfolio_values,
        mode='lines',
        name='Your Portfolio',
        line=dict(color='#6200ee', width=3),
        fill='tozeroy',
        fillcolor='rgba(98, 0, 238, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=spy_values,
        mode='lines',
        name='S&P 500',
        line=dict(color='#03dac6', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=nasdaq_values,
        mode='lines',
        name='NASDAQ',
        line=dict(color='#ff9800', width=2)
    ))
    
    fig.update_layout(
        title='Portfolio Performance vs. Benchmarks',
        xaxis_title='Date',
        yaxis_title='Value (Indexed to 100)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        template='plotly_white',
        height=500,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top holdings
    st.markdown('<div class="sub-header">Top Holdings</div>', unsafe_allow_html=True)
    
    holdings = account_data["holdings"]
    holdings_df = pd.DataFrame(holdings)
    
    if not holdings_df.empty:
        # Sort by market value
        holdings_df = holdings_df.sort_values(by="market_value", ascending=False)
        
        # Display top 5 holdings
        top_holdings = holdings_df.head(5)
        
        # Create columns for each holding
        cols = st.columns(len(top_holdings))
        
        for i, (_, holding) in enumerate(top_holdings.iterrows()):
            ticker = holding["ticker"]
            market_value = holding["market_value"]
            day_change = holding["day_change_pct"]
            total_gain_loss = holding["total_gain_loss"]
            total_gain_loss_pct = (total_gain_loss / (market_value - total_gain_loss)) * 100
            
            day_change_color = "positive" if day_change >= 0 else "negative"
            total_gl_color = "positive" if total_gain_loss >= 0 else "negative"
            
            day_change_sign = "+" if day_change >= 0 else ""
            total_gl_sign = "+" if total_gain_loss >= 0 else ""
            
            with cols[i]:
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">{ticker}</div>
                    <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">${market_value:,.2f}</div>
                    <div class="{day_change_color}" style="margin-bottom: 0.3rem;">{day_change_sign}{day_change:.2f}% Today</div>
                    <div class="{total_gl_color}">{total_gl_sign}${total_gain_loss:,.2f} ({total_gl_sign}{total_gain_loss_pct:.2f}%)</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Holdings table
    st.markdown('<div class="sub-header">Holdings Breakdown</div>', unsafe_allow_html=True)
    
    if not holdings_df.empty:
        # Format the dataframe for display
        display_df = holdings_df.copy()
        
        # Add % gain/loss column
        display_df["gain_loss_pct"] = (display_df["total_gain_loss"] / (display_df["market_value"] - display_df["total_gain_loss"])) * 100
        
        # Format columns
        display_df["cost_basis"] = display_df["cost_basis"].map("${:,.2f}".format)
        display_df["market_value"] = display_df["market_value"].map("${:,.2f}".format)
        display_df["day_change_pct"] = display_df["day_change_pct"].map("{:+.2f}%".format)
        display_df["total_gain_loss"] = display_df["total_gain_loss"].map("${:+,.2f}".format)
        display_df["gain_loss_pct"] = display_df["gain_loss_pct"].map("{:+.2f}%".format)
        
        # Rename columns for display
        display_df = display_df.rename(columns={
            "ticker": "Ticker",
            "quantity": "Quantity",
            "cost_basis": "Cost Basis",
            "market_value": "Market Value",
            "day_change_pct": "Day Change",
            "total_gain_loss": "Total Gain/Loss",
            "gain_loss_pct": "Gain/Loss %"
        })
        
        if "account" in display_df.columns:
            display_df = display_df.rename(columns={"account": "Account"})
        
        st.dataframe(display_df, use_container_width=True)

# Holdings page
def show_holdings():
    st.markdown('<div class="main-header">Holdings Breakdown</div>', unsafe_allow_html=True)
    
    # Get portfolio data
    portfolio_data = generate_mock_portfolio_data()
    
    # Use combined portfolio data for holdings
    holdings = portfolio_data["Combined"]["holdings"]
    holdings_df = pd.DataFrame(holdings)
    
    # Filters
    st.markdown('<div class="sub-header">Filters</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        account_filter = st.multiselect(
            "Account",
            options=["Schwab", "Interactive Brokers", "Robinhood"],
            default=["Schwab", "Interactive Brokers", "Robinhood"]
        )
    
    with col2:
        search_term = st.text_input("Search by Ticker or Name", "")
    
    # Apply filters
    filtered_df = holdings_df.copy()
    
    if "account" in filtered_df.columns and account_filter:
        filtered_df = filtered_df[filtered_df["account"].isin(account_filter)]
    
    if search_term:
        filtered_df = filtered_df[filtered_df["ticker"].str.contains(search_term, case=False)]
    
    # Summary statistics
    total_market_value = filtered_df["market_value"].sum()
    total_cost_basis = filtered_df["cost_basis"].sum()
    total_gain_loss = filtered_df["total_gain_loss"].sum()
    total_gain_loss_pct = (total_gain_loss / total_cost_basis) * 100 if total_cost_basis > 0 else 0
    
    st.markdown('<div class="sub-header">Summary</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="stat-label">Total Market Value</div>
            <div class="stat-value">${total_market_value:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="stat-label">Total Cost Basis</div>
            <div class="stat-value">${total_cost_basis:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color_class = "positive" if total_gain_loss >= 0 else "negative"
        sign = "+" if total_gain_loss >= 0 else ""
        
        st.markdown(f"""
        <div class="card">
            <div class="stat-label">Total Gain/Loss</div>
            <div class="stat-value {color_class}">{sign}${total_gain_loss:,.2f} ({sign}{total_gain_loss_pct:.2f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Holdings table
    st.markdown('<div class="sub-header">Holdings</div>', unsafe_allow_html=True)
    
    if not filtered_df.empty:
        # Format the dataframe for display
        display_df = filtered_df.copy()
        
        # Add % gain/loss column
        display_df["gain_loss_pct"] = (display_df["total_gain_loss"] / (display_df["market_value"] - display_df["total_gain_loss"])) * 100
        
        # Format columns
        display_df["cost_basis"] = display_df["cost_basis"].map("${:,.2f}".format)
        display_df["market_value"] = display_df["market_value"].map("${:,.2f}".format)
        display_df["day_change_pct"] = display_df["day_change_pct"].map("{:+.2f}%".format)
        display_df["total_gain_loss"] = display_df["total_gain_loss"].map("${:+,.2f}".format)
        display_df["gain_loss_pct"] = display_df["gain_loss_pct"].map("{:+.2f}%".format)
        
        # Rename columns for display
        display_df = display_df.rename(columns={
            "ticker": "Ticker",
            "quantity": "Quantity",
            "cost_basis": "Cost Basis",
            "market_value": "Market Value",
            "day_change_pct": "Day Change",
            "total_gain_loss": "Total Gain/Loss",
            "gain_loss_pct": "Gain/Loss %",
            "account": "Account"
        })
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No holdings match the selected filters.")

# Charts page
def show_charts():
    st.markdown('<div class="main-header">Charts & Index Comparisons</div>', unsafe_allow_html=True)
    
    # Tabs for different chart types
    tab1, tab2, tab3 = st.tabs(["Performance", "Returns", "Correlation"])
    
    with tab1:
        # Time range selection
        timerange_options = ["5D", "1M", "6M", "1Y"]
        timerange = st.select_slider("Time Period", options=timerange_options, value="1M")
        
        # Benchmark selection
        benchmark_options = st.multiselect(
            "Benchmarks",
            options=["S&P 500", "NASDAQ", "Russell 2000"],
            default=["S&P 500", "NASDAQ"]
        )
        
        # Get performance data
        dates, portfolio_values, spy_values, nasdaq_values = generate_performance_data(timerange)
        
        # Create performance chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=portfolio_values,
            mode='lines',
            name='Your Portfolio',
            line=dict(color='#6200ee', width=3),
            fill='tozeroy',
            fillcolor='rgba(98, 0, 238, 0.1)'
        ))
        
        if "S&P 500" in benchmark_options:
            fig.add_trace(go.Scatter(
                x=dates,
                y=spy_values,
                mode='lines',
                name='S&P 500',
                line=dict(color='#03dac6', width=2)
            ))
        
        if "NASDAQ" in benchmark_options:
            fig.add_trace(go.Scatter(
                x=dates,
                y=nasdaq_values,
                mode='lines',
                name='NASDAQ',
                line=dict(color='#ff9800', width=2)
            ))
        
        fig.update_layout(
            title='Portfolio Performance vs. Benchmarks',
            xaxis_title='Date',
            yaxis_title='Value (Indexed to 100)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            template='plotly_white',
            height=500,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="sub-header">Performance Statistics</div>', unsafe_allow_html=True)
            
            stats_data = {
                "Metric": ["Annualized Return", "Volatility", "Sharpe Ratio", "Max Drawdown", "Alpha", "Beta"],
                "Value": ["18.5%", "12.3%", "1.42", "-15.2%", "5.3%", "1.15"]
            }
            
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown('<div class="sub-header">Benchmark Comparison</div>', unsafe_allow_html=True)
            
            benchmark_data = {
                "Benchmark": ["S&P 500", "NASDAQ", "Russell 2000", "Dow Jones"],
                "Return": ["+15.0%", "+20.2%", "+12.5%", "+13.8%"],
                "Difference": ["+3.5%", "-1.7%", "+6.0%", "+4.7%"]
            }
            
            benchmark_df = pd.DataFrame(benchmark_data)
            st.dataframe(benchmark_df, use_container_width=True, hide_index=True)
    
    with tab2:
        # Returns comparison chart
        returns_data = {
            "Period": ["1 Month", "3 Months", "6 Months", "YTD", "1 Year", "3 Years", "5 Years"],
            "Your Portfolio": [3.5, 8.7, 15.0, 8.0, 32.0, 65.0, 85.0],
            "S&P 500": [1.8, 4.5, 8.0, 4.0, 17.0, 40.0, 50.0]
        }
        
        returns_df = pd.DataFrame(returns_data)
        
        fig = px.bar(
            returns_df, 
            x="Period", 
            y=["Your Portfolio", "S&P 500"],
            barmode="group",
            title="Returns Comparison",
            color_discrete_map={"Your Portfolio": "#6200ee", "S&P 500": "#03dac6"}
        )
        
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Return (%)",
            legend_title="",
            template="plotly_white",
            height=500,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown('<div class="sub-header">Correlation Matrix</div>', unsafe_allow_html=True)
        
        # Mock correlation data
        correlation_data = {
            "": ["Portfolio", "S&P 500", "NASDAQ", "Russell 2000", "Dow Jones"],
            "Portfolio": [1.00, 0.85, 0.88, 0.72, 0.80],
            "S&P 500": [0.85, 1.00, 0.92, 0.78, 0.95],
            "NASDAQ": [0.88, 0.92, 1.00, 0.75, 0.85],
            "Russell 2000": [0.72, 0.78, 0.75, 1.00, 0.70],
            "Dow Jones": [0.80, 0.95, 0.85, 0.70, 1.00]
        }
        
        correlation_df = pd.DataFrame(correlation_data)
        correlation_df = correlation_df.set_index("")
        
        fig = px.imshow(
            correlation_df,
            text_auto=True,
            color_continuous_scale="Viridis",
            aspect="auto"
        )
        
        fig.update_layout(
            title="Correlation Matrix",
            height=500,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Stock Analysis page
def show_stock_analysis():
    st.markdown('<div class="main-header">Stock Drill-Down</div>', unsafe_allow_html=True)
    
    # Stock selection
    ticker_input = st.text_input("Enter Stock Ticker", "AAPL")
    
    if ticker_input:
        ticker = ticker_input.upper()
        
        try:
            # Try to get real data from Yahoo Finance
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check if we got valid data
            if "longName" not in info:
                raise Exception("Could not retrieve stock data")
            
            company_name = info.get("longName", ticker)
            current_price = info.get("currentPrice", 0)
            previous_close = info.get("previousClose", 0)
            price_change = current_price - previous_close
            price_change_pct = (price_change / previous_close) * 100 if previous_close > 0 else 0
            
            # Display stock header
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f'<div class="sub-header">{ticker} - {company_name}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color: #666;">{info.get("sector", "N/A")} | {info.get("industry", "N/A")}</div>', unsafe_allow_html=True)
            
            with col2:
                price_color = "positive" if price_change >= 0 else "negative"
                price_sign = "+" if price_change >= 0 else ""
                
                st.markdown(f'<div style="text-align: right; font-size: 1.8rem; font-weight: 700;">${current_price:,.2f}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align: right;" class="{price_color}">{price_sign}${price_change:,.2f} ({price_sign}{price_change_pct:.2f}%)</div>', unsafe_allow_html=True)
            
            # Tabs for different information
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Chart", "Financials", "News"])
            
            with tab1:
                # Overview layout
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Price chart
                    st.markdown('<div class="sub-header">Price Chart</div>', unsafe_allow_html=True)
                    
                    # Get historical data
                    hist = stock.history(period="1y")
                    
                    if not hist.empty:
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=hist.index,
                            y=hist['Close'],
                            mode='lines',
                            name='Price',
                            line=dict(color='#6200ee', width=2),
                            fill='tozeroy',
                            fillcolor='rgba(98, 0, 238, 0.1)'
                        ))
                        
                        fig.update_layout(
                            title=f'{ticker} Price History',
                            xaxis_title='Date',
                            yaxis_title='Price ($)',
                            template='plotly_white',
                            height=400,
                            margin=dict(l=20, r=20, t=50, b=20)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No historical data available")
                
                with col2:
                    # Analyst ratings
                    st.markdown('<div class="sub-header">Analyst Ratings</div>', unsafe_allow_html=True)
                    
                    recommendation = info.get("recommendationMean", 0)
                    target_price = info.get("targetMeanPrice", 0)
                    
                    # Create a rating visualization
                    if recommendation > 0:
                        rating_fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = recommendation,
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Analyst Rating (1-5)"},
                            gauge = {
                                'axis': {'range': [1, 5], 'tickwidth': 1},
                                'bar': {'color': "#6200ee"},
                                'steps': [
                                    {'range': [1, 2], 'color': "#4caf50"},
                                    {'range': [2, 3], 'color': "#8bc34a"},
                                    {'range': [3, 4], 'color': "#ffeb3b"},
                                    {'range': [4, 5], 'color': "#f44336"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': recommendation
                                }
                            }
                        ))
                        
                        rating_fig.update_layout(
                            height=200,
                            margin=dict(l=20, r=20, t=30, b=20)
                        )
                        
                        st.plotly_chart(rating_fig, use_container_width=True)
                    
                    # Target price
                    if target_price > 0:
                        target_diff = target_price - current_price
                        target_diff_pct = (target_diff / current_price) * 100
                        
                        target_color = "positive" if target_diff > 0 else "negative"
                        target_sign = "+" if target_diff > 0 else ""
                        
                        st.markdown(f"""
                        <div class="card">
                            <div class="stat-label">Price Target</div>
                            <div class="stat-value">${target_price:,.2f}</div>
                            <div class="{target_color}">{target_sign}${target_diff:,.2f} ({target_sign}{target_diff_pct:.2f}%)</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Sentiment analysis
                    st.markdown('<div class="sub-header">Sentiment</div>', unsafe_allow_html=True)
                    
                    # Mock sentiment data
                    sentiment = "positive" if price_change_pct > 0 else "negative" if price_change_pct < 0 else "neutral"
                    sentiment_icon = "😀" if sentiment == "positive" else "😞" if sentiment == "negative" else "😐"
                    sentiment_color = "positive" if sentiment == "positive" else "negative" if sentiment == "negative" else ""
                    
                    st.markdown(f"""
                    <div class="card">
                        <div style="font-size: 2rem; text-align: center; margin-bottom: 0.5rem;">{sentiment_icon}</div>
                        <div style="text-align: center; font-weight: 600;" class="{sentiment_color}">
                            {sentiment.capitalize()} Sentiment
                        </div>
                        <div style="text-align: center; color: #666; font-size: 0.9rem;">
                            Based on news, social media, and analyst reports
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Key statistics
                st.markdown('<div class="sub-header">Key Statistics</div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    market_cap = info.get("marketCap", 0)
                    market_cap_str = f"${market_cap/1e9:.2f}B" if market_cap >= 1e9 else f"${market_cap/1e6:.2f}M"
                    
                    st.markdown(f"""
                    <div class="card">
                        <div class="stat-label">Market Cap</div>
                        <div class="stat-value">{market_cap_str}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    pe_ratio = info.get("trailingPE", 0)
                    
                    st.markdown(f"""
                    <div class="card">
                        <div class="stat-label">P/E Ratio</div>
                        <div class="stat-value">{pe_ratio:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    dividend_yield = info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0
                    
                    st.markdown(f"""
                    <div class="card">
                        <div class="stat-label">Dividend Yield</div>
                        <div class="stat-value">{dividend_yield:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    beta = info.get("beta", 0)
                    
                    st.markdown(f"""
                    <div class="card">
                        <div class="stat-label">Beta</div>
                        <div class="stat-value">{beta:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                # Advanced chart
                st.markdown('<div class="sub-header">Advanced Chart</div>', unsafe_allow_html=True)
                
                # Time period selection
                period_options = ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"]
                selected_period = st.select_slider("Time Period", options=period_options, value="1y")
                
                # Interval selection
                interval_options = ["1d", "5d", "1wk", "1mo", "3mo"]
                selected_interval = st.select_slider("Interval", options=interval_options, value="1d")
                
                # Get historical data
                hist = stock.history(period=selected_period, interval=selected_interval)
                
                if not hist.empty:
                    # Create candlestick chart
                    fig = go.Figure(data=[go.Candlestick(
                        x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        increasing_line_color='#4caf50',
                        decreasing_line_color='#f44336'
                    )])
                    
                    fig.update_layout(
                        title=f'{ticker} Price History',
                        xaxis_title='Date',
                        yaxis_title='Price ($)',
                        template='plotly_white',
                        height=600,
                        margin=dict(l=20, r=20, t=50, b=20),
                        xaxis_rangeslider_visible=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No historical data available for the selected period and interval")
            
            with tab3:
                # Financials
                st.markdown('<div class="sub-header">Financial Information</div>', unsafe_allow_html=True)
                
                # Get financial data
                income_stmt = stock.income_stmt
                balance_sheet = stock.balance_sheet
                cash_flow = stock.cashflow
                
                if not income_stmt.empty:
                    # Revenue and earnings chart
                    st.markdown('<div class="sub-header">Revenue and Earnings</div>', unsafe_allow_html=True)
                    
                    # Extract revenue and net income
                    revenue = income_stmt.loc['Total Revenue']
                    net_income = income_stmt.loc['Net Income']
                    
                    # Create dataframe for plotting
                    financials_df = pd.DataFrame({
                        'Revenue': revenue.values,
                        'Net Income': net_income.values
                    }, index=revenue.index)
                    
                    # Create bar chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=financials_df.index,
                        y=financials_df['Revenue'],
                        name='Revenue',
                        marker_color='#6200ee'
                    ))
                    
                    fig.add_trace(go.Bar(
                        x=financials_df.index,
                        y=financials_df['Net Income'],
                        name='Net Income',
                        marker_color='#03dac6'
                    ))
                    
                    fig.update_layout(
                        title='Revenue and Net Income',
                        xaxis_title='Date',
                        yaxis_title='Amount ($)',
                        barmode='group',
                        template='plotly_white',
                        height=400,
                        margin=dict(l=20, r=20, t=50, b=20)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Financial ratios
                    st.markdown('<div class="sub-header">Financial Ratios</div>', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Profitability ratios
                        st.markdown('<div style="font-weight: 600; margin-bottom: 0.5rem;">Profitability</div>', unsafe_allow_html=True)
                        
                        profit_margin = info.get("profitMargins", 0) * 100
                        roe = info.get("returnOnEquity", 0) * 100
                        roa = info.get("returnOnAssets", 0) * 100
                        
                        ratios_data = {
                            "Ratio": ["Profit Margin", "Return on Equity", "Return on Assets"],
                            "Value": [f"{profit_margin:.2f}%", f"{roe:.2f}%", f"{roa:.2f}%"]
                        }
                        
                        ratios_df = pd.DataFrame(ratios_data)
                        st.dataframe(ratios_df, use_container_width=True, hide_index=True)
                    
                    with col2:
                        # Valuation ratios
                        st.markdown('<div style="font-weight: 600; margin-bottom: 0.5rem;">Valuation</div>', unsafe_allow_html=True)
                        
                        pe = info.get("trailingPE", 0)
                        pb = info.get("priceToBook", 0)
                        ps = info.get("priceToSalesTrailing12Months", 0)
                        
                        ratios_data = {
                            "Ratio": ["P/E Ratio", "P/B Ratio", "P/S Ratio"],
                            "Value": [f"{pe:.2f}", f"{pb:.2f}", f"{ps:.2f}"]
                        }
                        
                        ratios_df = pd.DataFrame(ratios_data)
                        st.dataframe(ratios_df, use_container_width=True, hide_index=True)
                    
                    with col3:
                        # Growth ratios
                        st.markdown('<div style="font-weight: 600; margin-bottom: 0.5rem;">Growth</div>', unsafe_allow_html=True)
                        
                        earnings_growth = info.get("earningsGrowth", 0) * 100
                        revenue_growth = info.get("revenueGrowth", 0) * 100
                        
                        ratios_data = {
                            "Ratio": ["Earnings Growth", "Revenue Growth", "EPS Growth"],
                            "Value": [f"{earnings_growth:.2f}%", f"{revenue_growth:.2f}%", "N/A"]
                        }
                        
                        ratios_df = pd.DataFrame(ratios_data)
                        st.dataframe(ratios_df, use_container_width=True, hide_index=True)
                else:
                    st.warning("Financial data not available for this stock")
            
            with tab4:
                # News
                st.markdown('<div class="sub-header">Latest News & Headlines</div>', unsafe_allow_html=True)
                
                # Get news data
                news = stock.news
                
                if news:
                    for article in news[:5]:
                        title = article.get('title', 'No title')
                        publisher = article.get('publisher', 'Unknown source')
                        link = article.get('link', '#')
                        publish_time = datetime.fromtimestamp(article.get('providerPublishTime', 0))
                        time_ago = (datetime.now() - publish_time).days
                        time_str = f"{time_ago}d ago" if time_ago > 0 else "Today"
                        
                        st.markdown(f"""
                        <div class="card" style="margin-bottom: 1rem;">
                            <div style="font-weight: 600; margin-bottom: 0.5rem;">{title}</div>
                            <div style="display: flex; justify-content: space-between;">
                                <div style="color: #666;">{publisher}</div>
                                <div style="color: #666;">{time_str}</div>
                            </div>
                            <div style="margin-top: 0.5rem;">
                                <a href="{link}" target="_blank">Read more</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No recent news available for this stock")
        
        except Exception as e:
            st.error(f"Error retrieving data for {ticker}. Please check the ticker symbol and try again.")
            st.exception(e)

# AI Assistant page
def show_ai_assistant():
    st.markdown('<div class="main-header">AI Assistant</div>', unsafe_allow_html=True)
    
    # Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="sub-header">How the AI Assistant Can Help You</div>', unsafe_allow_html=True)
        
        # Features
        feature_col1, feature_col2, feature_col3 = st.columns(3)
        
        with feature_col1:
            st.markdown("""
            <div class="card" style="background-color: rgba(98, 0, 238, 0.1); height: 100%;">
                <div style="text-align: center; font-size: 2rem; margin-bottom: 1rem;">❓</div>
                <div style="text-align: center; font-weight: 600; margin-bottom: 0.5rem;">Explain Financial Terms</div>
                <div style="text-align: center; color: #666;">
                    Get clear explanations of complex financial concepts, ratios, and investment terminology.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with feature_col2:
            st.markdown("""
            <div class="card" style="background-color: rgba(3, 218, 198, 0.1); height: 100%;">
                <div style="text-align: center; font-size: 2rem; margin-bottom: 1rem;">📊</div>
                <div style="text-align: center; font-weight: 600; margin-bottom: 0.5rem;">Portfolio Analysis</div>
                <div style="text-align: center; color: #666;">
                    Ask "what if" questions about your portfolio and get insights on potential outcomes and strategies.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with feature_col3:
            st.markdown("""
            <div class="card" style="background-color: rgba(255, 152, 0, 0.1); height: 100%;">
                <div style="text-align: center; font-size: 2rem; margin-bottom: 1rem;">💡</div>
                <div style="text-align: center; font-weight: 600; margin-bottom: 0.5rem;">Investment Strategies</div>
                <div style="text-align: center; color: #666;">
                    Learn about different investment approaches and get personalized strategy suggestions.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Suggested questions
        st.markdown('<div class="sub-header" style="margin-top: 2rem;">Try asking:</div>', unsafe_allow_html=True)
        
        questions = [
            "What is a P/E ratio?",
            "Explain dividend yield",
            "What is dollar cost averaging?",
            "What if I invest $10000 in Apple?",
            "How can I diversify my portfolio?"
        ]
        
        question_cols = st.columns(3)
        
        for i, question in enumerate(questions):
            with question_cols[i % 3]:
                st.markdown(f"""
                <div class="card" style="margin-bottom: 1rem; cursor: pointer;" onclick="console.log('{question}')">
                    {question}
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="sub-header">Chat with AI</div>', unsafe_allow_html=True)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your DAJANIII AI Assistant. I can help explain financial terms, suggest investment strategies, or answer questions about your portfolio. What would you like to know?"}
            ]
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response based on prompt
            response = ""
            
            # Simple keyword-based responses
            prompt_lower = prompt.lower()
            
            if "p/e ratio" in prompt_lower or "pe ratio" in prompt_lower:
                response = "The Price-to-Earnings (P/E) ratio is a valuation metric that compares a company's current share price to its earnings per share (EPS). A high P/E ratio could suggest that a stock's price is high relative to earnings, indicating that investors expect high growth rates in the future."
            
            elif "dividend yield" in prompt_lower:
                response = "Dividend Yield is a financial ratio that shows how much a company pays out in dividends each year relative to its stock price. It's calculated as the annual dividend per share divided by the stock price per share."
            
            elif "dollar cost averaging" in prompt_lower:
                response = "Dollar-Cost Averaging (DCA) is an investment strategy where you divide the total amount to be invested across periodic purchases of a target asset to reduce the impact of volatility on the overall purchase. The purchases occur regardless of the asset's price and at regular intervals."
            
            elif "invest" in prompt_lower and "apple" in prompt_lower:
                response = "If you invest in Apple (AAPL) today, based on historical average annual returns of around 25% over the past decade, your investment could potentially grow significantly over time. However, past performance doesn't guarantee future results, and the technology sector can be volatile. It's important to consider your investment goals, time horizon, and risk tolerance."
            
            elif "diversify" in prompt_lower:
                response = "Diversifying your portfolio involves spreading your investments across different asset classes, sectors, and geographic regions to reduce risk. This strategy helps protect against significant losses if one particular investment or sector performs poorly. Consider adding a mix of stocks, bonds, real estate, and possibly alternative investments based on your risk tolerance and investment goals."
            
            else:
                response = "I don't have specific information about that. Would you like me to help you with understanding financial terms, suggesting investment strategies, or analyzing your portfolio?"
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)

# Upload page
def show_upload():
    st.markdown('<div class="main-header">Upload Portfolio</div>', unsafe_allow_html=True)
    
    # Main card
    st.markdown("""
    <div class="card">
        <div style="font-weight: 600; font-size: 1.2rem; margin-bottom: 1rem;">Import Your Portfolio</div>
        <div style="margin-bottom: 1rem;">
            Upload your brokerage statement or portfolio export file to automatically create a portfolio in DAJANIII. 
            We support PDF statements and CSV files from major brokerages.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Alert info
    st.info("Each new upload will create a new portfolio. A combined portfolio with all positions from every account will be automatically created.")
    
    # Upload steps
    st.markdown('<div class="sub-header">Upload Process</div>', unsafe_allow_html=True)
    
    # Stepper
    steps = ["Select File", "Upload & Process", "Create Portfolio"]
    current_step = 0  # Default to first step
    
    cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with cols[i]:
            if i < current_step:
                # Completed step
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="background-color: #4caf50; color: white; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; margin: 0 auto; margin-bottom: 0.5rem;">✓</div>
                    <div style="color: #4caf50; font-weight: 600;">{step}</div>
                </div>
                """, unsafe_allow_html=True)
            elif i == current_step:
                # Current step
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="background-color: #6200ee; color: white; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; margin: 0 auto; margin-bottom: 0.5rem;">{i+1}</div>
                    <div style="color: #6200ee; font-weight: 600;">{step}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Future step
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="background-color: #e0e0e0; color: #666; border-radius: 50%; width: 30px; height: 30px; line-height: 30px; margin: 0 auto; margin-bottom: 0.5rem;">{i+1}</div>
                    <div style="color: #666;">{step}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "pdf"])
    
    if uploaded_file is not None:
        # Display file details
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        
        st.json(file_details)
        
        # Process button
        if st.button("Process File"):
            with st.spinner("Processing file..."):
                # Simulate processing
                import time
                time.sleep(2)
                
                # Show success message
                st.success("File processed successfully! Portfolio created.")
                
                # Show portfolio summary
                st.markdown('<div class="sub-header">Portfolio Summary</div>', unsafe_allow_html=True)
                
                summary_data = {
                    "Account": "Schwab",
                    "Symbols": 15,
                    "Total Value": "$125,000.00",
                    "Cost Basis": "$110,000.00",
                    "Gain/Loss": "+$15,000.00 (+13.64%)"
                }
                
                summary_df = pd.DataFrame([summary_data])
                st.dataframe(summary_df, use_container_width=True, hide_index=True)
                
                # View portfolio button
                st.button("View Portfolio")
    
    # How it works section
    st.markdown('<div class="sub-header" style="margin-top: 2rem;">How It Works</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card" style="background-color: rgba(98, 0, 238, 0.1); height: 100%;">
            <div style="text-align: center; font-size: 2rem; font-weight: 700; margin-bottom: 1rem; color: #6200ee;">1</div>
            <div style="text-align: center; font-weight: 600; margin-bottom: 0.5rem;">Upload Your File</div>
            <div style="text-align: center; color: #666;">
                Drag and drop or select your brokerage statement (PDF) or portfolio export (CSV) file.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="background-color: rgba(3, 218, 198, 0.1); height: 100%;">
            <div style="text-align: center; font-size: 2rem; font-weight: 700; margin-bottom: 1rem; color: #03dac6;">2</div>
            <div style="text-align: center; font-weight: 600; margin-bottom: 0.5rem;">Automatic Processing</div>
            <div style="text-align: center; color: #666;">
                Our system automatically detects your brokerage and extracts all holdings and positions.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="background-color: rgba(255, 152, 0, 0.1); height: 100%;">
            <div style="text-align: center; font-size: 2rem; font-weight: 700; margin-bottom: 1rem; color: #ff9800;">3</div>
            <div style="text-align: center; font-weight: 600; margin-bottom: 0.5rem;">Portfolio Creation</div>
            <div style="text-align: center; color: #666;">
                A new portfolio is created for each upload, plus a combined portfolio with all your holdings.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Supported brokerages
    st.markdown('<div class="sub-header" style="margin-top: 2rem;">Supported Brokerages</div>', unsafe_allow_html=True)
    
    brokerages = ["Charles Schwab", "Interactive Brokers", "Robinhood", "TD Ameritrade", "Fidelity", "E*TRADE"]
    
    brokerage_cols = st.columns(3)
    
    for i, brokerage in enumerate(brokerages):
        with brokerage_cols[i % 3]:
            st.markdown(f"""
            <div class="card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center;">
                    <div style="background-color: #f5f5f5; border-radius: 50%; width: 40px; height: 40px; line-height: 40px; text-align: center; margin-right: 1rem;">🏦</div>
                    <div>{brokerage}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Main app logic
if page == "Dashboard":
    show_dashboard()
elif page == "Holdings":
    show_holdings()
elif page == "Charts":
    show_charts()
elif page == "Stock Analysis":
    show_stock_analysis()
elif page == "AI Assistant":
    show_ai_assistant()
elif page == "Upload":
    show_upload()

# Add footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 1rem; border-top: 1px solid #e0e0e0; color: #666;">
    DAJANIII Portfolio Manager & Private Equity Consultant © 2025
</div>
""", unsafe_allow_html=True)
