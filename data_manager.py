import yfinance as yf
import pandas as pd
import streamlit as st

def fetch_data_and_clean(tickers, start_date, end_date):
    """
    Descarga precios ajustados de Yahoo Finance y limpia los datos.
    """
    try:
        data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)['Adj Close']
        
        if isinstance(data, pd.Series):
            data = data.to_frame()
            data.columns = tickers

        data = data.ffill() 
        data = data.dropna()
        
        return data
    except Exception as e:
        raise ValueError(f"Error al descargar datos: {e}")

def get_currency_info(ticker):
    """
    Intenta obtener la moneda del activo.
    Retorna ('USD', 'Información extra') por defecto si falla.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        currency = ticker_obj.fast_info.get('currency', 'USD')
        return currency, "OK"
    except:
        return 'USD', "No info"