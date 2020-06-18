# Finenhance
[![GitHub release](https://img.shields.io/github/v/release/Yyassin/Finenhance.svg?colorB=97CA00?label=version)](https://github.com/Yyassin/Finenhance/releases/latest) [![Github All Releases](https://img.shields.io/github/downloads/Yyassin/Finenhance/total.svg?colorB=97CA00)](https://github.com/Yyassin/Finenhance/releases) [![GitHub stars](https://img.shields.io/github/stars/Yyassin/Finenhance.svg?colorB=007EC6)](https://github.com/Yyassin/Finenhance/stargazers)  [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/Yyassin/Finenhance/master/LICENSE)

> **Finenhance** is a python-tkinter based application that aims to ease financial management. The desktop app boasts live stock market tracking, through the yahoo-finance API, and
analysis using numpy, pandas and matplotlib. Finenhance also features a simulated banking system which supports deposits and withdrawals along with a transaction history. Users can use the
money in their balance to invest in real stocks and make a profit!

<!--- Supports all major media players, including full **Spotify**, **Google Play Music Desktop Player** and **Chrome/Firefox webplayer** support (thanks to **[@tjhrulz](https://github.com/tjhrulz)** and **[@khanhas](https://github.com/khanhas)**)  for the amazing plugins used in this skin). --->

## Minimum Requirements:
 - Python 3.8 or later.
 - Yahoo Finance API
 - Matplotlib
 - Pandas & Pandas Datareader
 - Numpy
 
## Setup & Running Project
You will first need to clone the repository to your local machine:
```
https://github.com/Yyassin/Finenhance.git
```

* Install [Python 3.8](https://www.python.org/downloads/) or later.

* Then install the required modules: 

```
pip install matplotlib yahoo-fin pandas pandas-datareader numpy
```

* Navigate to the appropriate directory from terminal:
```
cd ~/Finenhance
```

* Run the main file:
```
python Finenhance.py
```


## Using Project

* Sign up using the sign up tool, then login with the same credentials.

* Navigate to the **Accounts** page where you can manage your simulated bank account. You can choose to deposit or withdraw credits, both being recorded in the transaction feed below.

* Navigating to the **Stocks** page is where the fun begins.

## Stocks & Investing

* Enter the stock ticker you are trying to view in the input field, make sure the ticker is in the NYSE market.

* Select one of the time ranges listed to determine the range of ticker history that will be fetched. Press 'Confirm'.

* A chart displaying the stock in the selecte time-range will be shown, in red if the stock is in loss for the day
and green in the case of a gain. The chart can be navigated using the options at the bottom of the window. Relevant information is also shown on the page.

* Select 'Detailed' for more information on the selected stock: Ask, Volume, Market Cap... A tab will appear.

* To invest, select the 'Invest' Option. Select the number of shares to purchase using the slider, press 'Confirm' then 'Save Portfolio'
to record the purchase. A list of invested stocks and profit will appear in the same tab, users can choose to sell shares here
by selecting the 'Sell' option.

## Extra Settings

* Navigating to the settings page will allow users to change the app preset theme to one of two dark modes. Notes that 
all currently open tabs must be refreshed to register the change.

 * Enjoy! 🎉


## Features
- User authentication and save-data using a local database.
- Real time stock data through Yahoo finance API.
- Plotting analysis of stock history in multiple time ranges using matplotlib, numpy and pandas.
- Banking system with user transaction history.
- Settings panel to change app theme.
