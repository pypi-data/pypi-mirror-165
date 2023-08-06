## UAT Breeze Connect SDK

This is a package to integrate streaming of stocks or user's order-notification & call APIs through which you can fetch live/historical data, automate your trading strategies, and monitor your portfolio in real time.

## Setup virtual environment

You must install the virtualenv package via pip

```
pip install virtualenv
```

You should create breeze virtual environment via virtualenv

```
virtualenv -p python3 breeze_venv
```

And then, You can activate virtual environment via source

```
source breeze_venv/bin/activate
```

## Installing the client

You can install the latest release via pip

```
pip install --upgrade uat-breeze-connect
```

Or, You can also install the specific release version via pip

```
pip install uat-breeze-connect==1.0.14rc13
```

## Websocket Usage

```python
from breeze_connect import BreezeConnect

# Initialize SDK
breeze = BreezeConnect(api_key="your_api_key")

# Obtain your session key from https://uatapi.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
import urllib
print("https://uatapi.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze.generate_session(api_secret="your_secret_key",
                        session_token="your_api_session")

# Connect to websocket
breeze.ws_connect()

# Callback to receive ticks.
def on_ticks(ticks):
    print("Ticks: {}".format(ticks))

# Assign the callbacks.
breeze.on_ticks = on_ticks

# subscribe stocks feeds
breeze.subscribe_feeds(exchange_code="NFO", stock_code="ZEEENT", product_type="options", expiry_date="31-Mar-2022", strike_price="350", right="Call", get_exchange_quotes=True, get_market_depth=False)

# subscribe stocks feeds by stock-token
breeze.subscribe_feeds(stock_token="1.1!500780")

# unsubscribe stocks feeds
breeze.unsubscribe_feeds(exchange_code="NFO", stock_code="ZEEENT", product_type="options", expiry_date="31-Mar-2022", strike_price="350", right="Call", get_exchange_quotes=True, get_market_depth=False)

# unsubscribe stocks feeds by stock-token
breeze.unsubscribe_feeds(stock_token="1.1!500780")

# subscribe order notification feeds
breeze.subscribe_feeds(get_order_notification=True)
```
---
**NOTE**

Examples for stock_token are "4.1!38071" or "1.1!500780".

exchange_code must be 'BSE', 'NSE', 'NDX', 'MCX' or 'NFO'.

stock_code should not be an empty string. Examples for stock_code are "WIPRO" or "ZEEENT".

product_type can be either 'Futures', 'Options' or an empty string. product_type can not be an empty string for exchange_code 'NDX', 'MCX' and 'NFO'. 

strike_date can be in DD-MMM-YYYY(Ex.: 01-Jan-2022) or an empty string. strike_date can not be an empty string for exchange_code 'NDX', 'MCX' and 'NFO'.

strike_price can be float-value in string or an empty string. strike_price can not be an empty string for product_type 'Options'.

right can be either 'Put', 'Call' or an empty string. right can not be an empty string for product_type 'Options'.

Either get_exchange_quotes must be True or get_market_depth must be True. Both get_exchange_quotes and get_market_depth can be True, But both must not be False.

---

## API Usage

```python
from breeze_connect import BreezeConnect

# Initialize SDK
breeze = BreezeConnect(api_key="your_api_key")

# Obtain your session key from https://uatapi.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
import urllib
print("https://uatapi.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze.generate_session(api_secret="your_secret_key",
                        session_token="your_api_session")

# Generate ISO8601 Date/DateTime String
import datetime
iso_date_string = datetime.datetime.strptime("28/02/2021","%d/%m/%Y").isoformat()[:10] + 'T05:30:00.000Z'
iso_date_time_string = datetime.datetime.strptime("28/02/2021 23:59:59","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'
```

<head>
  <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.3/styles/default.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.0.3/highlight.min.js"></script>
  <script>hljs.initHighlightingOnLoad();</script>
</head>


# Following are the complete list of API method:

# Index Page


<ul style="top: 0;bottom:0;position:fixed;overflow-y:scroll;overflow-x:hidden;">
 <li><a href="#customer_detail">get_customer_details</a></li>
 <li><a href="#demat_holding">get_demat_holdings</a></li>
 <li><a href="#get_funds">get_funds</a></li>
 <li><a href="#set_funds">set_funds</a></li>
 <li><a href="#historical_data">get_historical_data</a></li>
 <li><a href="#add_margin">add_margin</a></li>
 <li><a href="#get_margin">get_margin</a></li>
 <li><a href="#place_order">place_order</a></li>
 <li><a href="#order_detail">order_detail</a></li>
 <li><a href="#order_list">order_list</a></li>
 <li><a href="#cancel_order">cancel_order</a></li>
 <li><a href="#modify_order">modify_order</a></li>
 <li><a href="#portfolio_holding">get_portfolio_holding</a></li>
 <li><a href="#portfolio_position">get_portfolio_position</a></li>
 <li><a href="#get_quotes">get_quotes</a></li>
 <li><a href="#get_option_chain">get_option_chain_quotes</a></li>
 <li><a href="#square_off1">square_off</a></li>
 <li><a href="#modify_order">modify_order</a></li>
 <li><a href="#trade_list">get_trade_list</a></li>
 <li><a href="#trade_detail">get_trade_detail</a></li>
</ul>

# Following are the complete list of API method:

# customer_detail

<h4 id="customer_detail"> Get Customer details by api-session value.</h4>
<pre><code class="python">breeze.get_customer_details(api_session="your_api_session") </code></pre>
<hr>

# demat_holding

<h4 id="demat_holding"> Get Demat Holding details of your account.</h4>
<pre><code class="python">breeze.get_demat_holdings()</code></pre>
<hr>

# get_funds

<h4 id="get_funds"> Get Funds details of your account.</h4>
<pre><code class="python">breeze.get_funds()</code></pre>
<hr>

# set_funds

<h4 id="set_funds"> Set Funds of your account by transaction-type as "Credit" or "Debit" with amount in numeric string as rupees and segment-type as "Equity" or "FNO".</h4>
<pre><code class="python">breeze.set_funds(transaction_type="debit", 
                    amount="200",
                    segment="Equity")</code></pre>
<hr>

# historical_data

<h4 id="historical_data">Get Historical Data for specific stock-code by mentioned interval either as "minute", "5minute", "30minutes" or as "day".</h4>
<pre><code class="python">breeze.get_historical_data(interval="1minute",
                            from_date= "2022-08-15T07:00:00.000Z",
                            to_date= "2022-08-17T07:00:00.000Z",
                            stock_code="ICIBAN",
                            exchange_code="NFO",
                            product_type="futures",
                            expiry_date="2022-08-25T07:00:00.000Z",
                            right="others",
                            strike_price="0")</code></pre>
<hr>

# add_margin

<h4 id="add_margin">Add Margin to your account.</h4>
<pre><code class="python">breeze.add_margin(product_type="margin", 
                    stock_code="ICIBAN", 
                    exchange_code="BSE", 
                    settlement_id="2021220", 
                    add_amount="100", 
                    margin_amount="3817.10", 
                    open_quantity="10", 
                    cover_quantity="0", 
                    category_index_per_stock="", 
                    expiry_date="", 
                    right="", 
                    contract_tag="", 
                    strike_price="", 
                    segment_code="")</code></pre>
<hr>

# get_margin

<h4 id="get_margin">Get Margin of your account.</h4>
<pre><code class="python">breeze.get_margin(exchange_code="NSE")</code></pre>
<hr>

# place_order

<h4 id="place_order">Place an order from your account.</h4>
<pre><code class="python">breeze.place_order(stock_code="ICIBAN",
                    exchange_code="NFO",
                    product="futures",
                    action="buy",
                    order_type="limit",
                    stoploss="0",
                    quantity="3200",
                    price="200",
                    validity="day",
                    validity_date="2022-08-22T06:00:00.000Z",
                    disclosed_quantity="0",
                    expiry_date="2022-08-25T06:00:00.000Z",
                    right="others",
                    strike_price="0",
                    user_remark="Test")
</code></pre>
<hr>

# get_order_detail

<h4 id="order_detail">Get an order details by exchange-code and order-id from your account.</h4>
<pre><code class="python">breeze.get_order_detail(exchange_code="NSE",
                        order_id="20220819N100000001")</code></pre>
<hr>

# get_order_list

<h4 id="order_list">Get order list of your account.</h4>
<pre><code class="python">breeze.get_order_list(exchange_code="NSE",
                        from_date="2022-08-01T10:00:00.000Z",
                        to_date="2022-08-19T10:00:00.000Z")</code></pre>
<hr>

# cancel_order

<h4 id="cancel_order">Cancel an order from your account whose status are not Executed.</h4> 
<pre><code class="python">breeze.cancel_order(exchange_code="NSE",
                    order_id="20220819N100000001")</code></pre>
<hr>

# modify_order

<h4 id="modify_order">Modify an order from your account whose status are not Executed.</h4> 
<pre><code class="python">breeze.modify_order(order_id="202208191100000001",
                    exchange_code="NFO",
                    order_type="limit",
                    stoploss="0",
                    quantity="250",
                    price="290100",
                    validity="day",
                    disclosed_quantity="0",
                    validity_date="2022-08-22T06:00:00.000Z")</code></pre>
<hr>

# get_portfolio_holding

<h4 id="portfolio_holding">Get Portfolio Holdings of your account.</h4>
<pre><code class="python">breeze.get_portfolio_holdings(exchange_code="NFO",
                                from_date="2022-08-01T06:00:00.000Z",
                                to_date="2022-08-19T06:00:00.000Z",
                                stock_code="",
                                portfolio_type="")</code></pre>
<hr>

# get_portfolio_position

<h4 id="portfolio_position">Get Portfolio Positions from your account.</h4>
<pre><code class="python">breeze.get_portfolio_positions()</code></pre>
<hr>

# get_quotes

<h4 id="get_quotes">Get quotes of mentioned stock-code </h4>
<pre><code class="python">breeze.get_quotes(stock_code="ICIBAN",
                    exchange_code="NFO",
                    expiry_date="2022-08-25T06:00:00.000Z",
                    product_type="futures",
                    right="others",
                    strike_price="0")</code></pre>
<hr>

# get_option_chain

<h4 id="get_option_chain">Get option-chain of mentioned stock-code for product-type Futures where input of expiry-date is not compulsory</h4>
<pre><code class="python">breeze.get_option_chain_quotes(stock_code="ICIBAN",
                    exchange_code="NFO",
                    product_type="futures",
                    expiry_date="2022-08-25T06:00:00.000Z")</code></pre>

<h4 id="get_option_chain2">Get option-chain of mentioned stock-code for product-type Options where atleast 2 input is required out of expiry-date, right and strike-price</h4>
<pre><code class="python">breeze.get_option_chain_quotes(stock_code="ICIBAN",
                    exchange_code="NFO",
                    product_type="options",
                    expiry_date="2022-08-25T06:00:00.000Z",
                    right="call",
                    strike_price="16850")</code></pre>
<hr>

# square_off

<h4 id="square_off1">Square off an Equity Margin Order</h4>
<pre><code class="python">breeze.square_off(exchange_code="NSE",
                    product="margin",
                    stock_code="NIFTY",
                    quantity="10",
                    price="0",
                    action="sell",
                    order_type="market",
                    validity="day",
                    stoploss="0",
                    disclosed_quantity="0",
                    protection_percentage="",
                    settlement_id="",
                    cover_quantity="",
                    open_quantity="",
                    margin_amount="")</code></pre>
# Note: Please refer get_portfolio_positions() for settlement id and margin_amount

<h4 id="square_off2">Square off an FNO Futures Order</h4>
<pre><code class="python">breeze.square_off(exchange_code="NFO",
                    product="futures",
                    stock_code="ICIBAN",
                    expiry_date="2022-08-25T06:00:00.000Z",
                    action="sell",
                    order_type="market",
                    validity="day",
                    stoploss="0",
                    quantity="50",
                    price="0",
                    validity_date="2022-08-12T06:00:00.000Z",
                    trade_password="",
                    disclosed_quantity="0")</code></pre>

<h4 id="square_off3">Square off an FNO Options Order</h4>
<pre><code class="python">breeze.square_off(exchange_code="NFO",
                    product="options",
                    stock_code="ICIBAN",
                    expiry_date="2022-08-25T06:00:00.000Z",
                    right="Call",
                    strike_price="16850",
                    action="sell",
                    order_type="market",
                    validity="day",
                    stoploss="0",
                    quantity="50",
                    price="0",
                    validity_date="2022-08-12T06:00:00.000Z",
                    trade_password="",
                    disclosed_quantity="0")</code></pre>
<hr>

# get_trade_list

<h4 id="trade_list">Get trade list of your account.</h4>
<pre><code class="python">breeze.get_trade_list(from_date="2022-08-01T06:00:00.000Z",
                        to_date="2022-08-19T06:00:00.000Z",
                        exchange_code="NSE",
                        product_type="",
                        action="",
                        stock_code="")</code></pre>
<hr>

# get_trade_detail

<h4 id="trade_detail">Get trade detail of your account.</h4>
<pre><code class="python">breeze.get_trade_detail(exchange_code="NSE",
                        order_id="20220819N100000005")</code></pre>

</body>