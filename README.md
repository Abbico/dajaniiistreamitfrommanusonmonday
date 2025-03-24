# DAJANIII Portfolio Manager - Streamlit Version

A comprehensive portfolio management application with advanced features for tracking investments, analyzing performance, and making informed financial decisions.

## Features

### 📊 Portfolio Dashboard
- Holdings by account (Schwab, IBKR, Robinhood, etc.)
- Key stats per account (number of symbols, cost basis, market value)
- Day change percentage tracking
- Unrealized and realized gain/loss calculations

### 🧾 Holdings Breakdown
- Detailed stock-level information
- Real-time prices and charts
- Filtering and sorting capabilities
- Performance metrics and analysis

### 📈 Charts & Index Comparisons
- Performance visualization over multiple time periods (5D, 1M, 6M, YTD, 1Y, All)
- Benchmark comparison with major indices (S&P 500, Nasdaq, Russell 2000)
- Technical analysis tools
- Returns analysis

### 📰 Stock Drill-Down
- Real-time price information
- Analyst ratings and price targets
- Latest headlines and news
- Financial metrics and ratios
- Sentiment analysis

### 💬 Built-in AI Assistant
- Financial term explanations
- Investment strategy suggestions
- Portfolio scenario analysis
- Personalized recommendations

### 📤 Uploads
- Unified upload area for portfolio files
- Support for CSV and PDF formats
- Automatic brokerage detection
- Combined portfolio creation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dajaniii-streamlit-app.git

# Navigate to the project directory
cd dajaniii-streamlit-app

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## Deployment to Streamlit Cloud

1. Push this repository to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/dajaniii-streamlit-app.git
   git push -u origin main
   ```

2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with your GitHub account.

3. Click "New app" and select this repository.

4. Configure the app:
   - Main file path: `app.py`
   - Python version: 3.9 or higher
   - Requirements: `requirements.txt` (already included)

5. Click "Deploy" and wait for the deployment to complete.

6. Your app will be available at a URL like: `https://yourusername-dajaniii-streamlit-app-app-xxxxx.streamlit.app`

## Local Development

To run the app locally:

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

## Dependencies

- streamlit: Web application framework
- pandas: Data manipulation and analysis
- numpy: Numerical computing
- plotly: Interactive visualizations
- yfinance: Yahoo Finance API wrapper
- matplotlib: Plotting library
- pillow: Image processing
- requests: HTTP library

## License

MIT

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Yahoo Finance API](https://finance.yahoo.com/)
- [Pandas](https://pandas.pydata.org/)
