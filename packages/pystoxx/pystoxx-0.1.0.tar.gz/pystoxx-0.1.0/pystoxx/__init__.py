import pandas as pd 
import numpy as np 
import requests
import json

class Stoxx:
    def __init__(self):
        self.x_rapidapi_key = ""
        self.x_rapidapi_host = "stoxx-by-recursiv.p.rapidapi.com"

    def get_key(self):
        return self.x_rapidapi_key

    def RapidAPI(self, x_rapidapi_key):
        """ Authenticates a user using their RapidAPI key. 
        Sign up for a free account by navigating to https://rapidapi.com/recursivllc/api/stoxx1.

        Keyword Arguments:
        x_rapidapi_key -- A character string obtainable from RapidAPI.

        Examples:

        from pystoxx import Stoxx
    
        stoxx = Stoxx()
        stoxx.RapidAPI("enter-long-api-character-string-here")

        """
        self.x_rapidapi_key = x_rapidapi_key
        self.x_rapidapi_host = "stoxx-by-recursiv.p.rapidapi.com"

    def get_historical_prices(self, ticker="msft", months=1):
        """ Returns historical prices for a given ticker.

        Keyword Arguments:
        ticker -- Company ticker symbol like 'amzn' or 'aapl' (default amzn)
        months -- Range of time in months 1, 2, 12, etc... (default 1)

        Examples:
    
        prices = stoxx.get_historical_prices("amzn", 3) # Returns 3 months of data
        prices = stoxx.get_historical_prices("msft", 12) # Returns 1 year of data

        """
        url = "https://stoxx1.p.rapidapi.com/api/v1/stoxx/company/{ticker}/history/prices/{months}".format(ticker=ticker,months=months)
        headers = {
            'x-rapidapi-key': self.x_rapidapi_key,
            'x-rapidapi-host': self.x_rapidapi_host
            }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def get_historical_news(self, ticker="msft", months=1):
        """ Returns historical news and sentiment for a given ticker.

        Keyword Arguments:
        ticker -- Company ticker symbol like 'amzn' or 'aapl' (default amzn)
        months -- Range of time in months 1, 2, 3, etc... (default 1)

        Examples:
        prices = stoxx.get_historical_prices("amzn", 1) # Returns 1 month of data
        prices = stoxx.get_historical_prices("msft", 3) # Returns 3 months of data

        """
        url = "https://stoxx1.p.rapidapi.comapi/v1/stoxx/company/{ticker}/history/articles/{months}".format(ticker=ticker,months=months)
        headers = {
            'x-rapidapi-key': self.x_rapidapi_key,
            'x-rapidapi-host': self.x_rapidapi_host
            }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def get_public_companies(self):
        """ Returns a list of all publicly traded companies.

        Keyword Arguments:
        None

        Examples:
        companies = stoxx.get_public_companies() # Returns list of all public companies.

        """
        url = "https://stoxx1.p.rapidapi.com/api/v1/stoxx/companies"
        headers = {
            'x-rapidapi-key': self.x_rapidapi_key,
            'x-rapidapi-host': self.x_rapidapi_host
            }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def get_company_data(self, ticker='amzn'):
        """ Returns a company information such as name, location, website, and ticker.

        Keyword Arguments:
        ticker -- Company ticker symbol like 'amzn' or 'aapl' (default amzn)

        Examples:
        amzn_data = stoxx.get_company_data(ticker='amzn') # Returns data relating to ticker 'amzn'.
        msft_data = stoxx.get_company_data(ticker='msft') # Returns data relating to ticker 'msft'.

        """
        url = "https://stoxx1.p.rapidapi.com/api/v1/stoxx/company/{ticker}/info".format(ticker=ticker)
        headers = {
            'x-rapidapi-key': self.x_rapidapi_key,
            'x-rapidapi-host': self.x_rapidapi_host
            }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def get_price_quote(self, ticker):
        """ Returns a price quote for a given ticker.

        Keyword Arguments:
        ticker -- Company ticker symbol like 'amzn' or 'aapl' (default amzn)

        Examples:
        price_quote = stoxx.get_price_quote("msft") # Returns a price quote for 'msft'
        price_quote = stoxx.get_price_quote("amzn") # Returns a price quote for 'amzn'

        """
        url = "https://stoxx1.p.rapidapi.com/api/v1/stoxx/company/{ticker}/quote".format(ticker=ticker)
        headers = {
            'x-rapidapi-key': self.x_rapidapi_key,
            'x-rapidapi-host': self.x_rapidapi_host
            }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def get_company_competition(self, ticker):
        """ Returns a list of known competitors based on news articles.

        Keyword Arguments:
        ticker -- Company ticker symbol like 'amzn' or 'aapl' (default amzn)

        Examples:
        competition = stoxx.get_company_competition("amzn") # Returns a list of known competitors for 'amzn'
        competition = stoxx.get_company_competition("msft") # Returns a list of known competitors for 'msft'

        """
        url = "https://stoxx1.p.rapidapi.com/api/v1/stoxx/company/{ticker}/competition".format(ticker=ticker)
        headers = {
            'x-rapidapi-key': self.x_rapidapi_key,
            'x-rapidapi-host': self.x_rapidapi_host
            }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def get_market_performance(self):
        """ Returns a list of sectors and their current performances in the US stock market.

        Keyword Arguments:
        None

        Examples:
    
        market = stoxx.get_market_performance() # Returns a list sectors and their current performances.

        """
        url = "https://stoxx1.p.rapidapi.com/api/v1/stoxx/market/performance"
        headers = {
            'x-rapidapi-key': self.x_rapidapi_key,
            'x-rapidapi-host': self.x_rapidapi_host
            }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def calculate_sentiment(self, text):
        """ Returns a comprehensive list of sentiment calculations for a given text.

        Keyword Arguments:
        None

        Examples:
        article_text = "Oracle stock shoots up to a record after Barclays says buy, citing ‘good’ cloud products and IT spending recovery"
        amzn_sentiment = stoxx.calculate_sentiment({"content" : text_data}) # Returns a list sectors and their current performances.

        """
        url = "https://stoxx1.p.rapidapi.com/api/v1/stoxx/calculate/sentiment"
        payload = json.dumps({"content" : "This is a wonderful and amazing API!"})
        headers = {
            'content-type': "application/json",
            'x-rapidapi-key': self.x_rapidapi_key,
            'x-rapidapi-host': self.x_rapidapi_host
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return response.json()