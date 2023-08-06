metaapi.cloud SDK for Python
############################

MetaApi is a powerful, fast, cost-efficient, easy to use and standards-driven cloud forex trading API for MetaTrader 4 and MetaTrader 5 platform designed for traders, investors and forex application developers to boost forex application development process. MetaApi can be used with any broker and does not require you to be a brokerage.

CopyFactory is a simple yet powerful copy-trading API which is a part of MetaApi. See below for CopyFactory readme section.

MetaApi is a paid service, but API access to one MetaTrader account is free of charge.

The `MetaApi pricing <https://metaapi.cloud/#pricing>`_ was developed with the intent to make your charges less or equal to what you would have to pay
for hosting your own infrastructure. This is possible because over time we managed to heavily optimize
our MetaTrader infrastructure. And with MetaApi you can save significantly on application development and
maintenance costs and time thanks to high-quality API, open-source SDKs and convenience of a cloud service.

Official REST and websocket API documentation: https://metaapi.cloud/docs/client/

This SDK requires a 3.8+ version of Python to run.

Please note that this SDK provides an abstraction over REST and websocket API to simplify your application logic.

For more information about SDK APIs please check docstring documentation in source codes located inside lib folder of this package.

Working code examples
=====================
Please check `this short video <https://youtu.be/LIqFOOOLP-g>`_ to see how you can download samples via our web application.

You can find code examples at `examples folder of our github repo <https://github.com/agiliumtrade-ai/metaapi-python-sdk/tree/master/examples>`_ or in the examples folder of the pip package.

We have composed a `short guide explaining how to use the example code <https://metaapi.cloud/docs/client/usingCodeExamples/>`_

Installation
============
.. code-block:: bash

    pip install metaapi-cloud-sdk

Connecting to MetaApi
=====================
Please use one of these ways:

1. https://app.metaapi.cloud/token web UI to obtain your API token.
2. An account access token which grants access to a single account. See section below on instructions on how to retrieve account access token.

Supply token to the MetaApi class constructor.

.. code-block:: python

    from metaapi_cloud_sdk import MetaApi

    token = '...'
    api = MetaApi(token=token)

Retrieving account access token
===============================
Account access token grants access to a single account. You can retrieve account access token via API:

.. code-block:: python

    account_id = '...'
    account = await api.metatrader_account_api.get_account(account_id=account_id)
    account_access_token = account.access_token
    print(account_access_token)

Alternatively, you can retrieve account access token via web UI on https://app.metaapi.cloud/accounts page (see `this video <https://youtu.be/PKYiDns6_xI>`_).

Managing MetaTrader accounts (API servers for MT accounts)
==========================================================
Before you can use the API you have to add an MT account to MetaApi and start an API server for it.

Managing MetaTrader accounts (API servers) via web UI
-----------------------------------------------------
You can manage MetaTrader accounts here: https://app.metaapi.cloud/accounts

Create a MetaTrader account (API server) via API
------------------------------------------------

Creating an account using automatic broker settings detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To create an account, supply a request with account data and the platform field indicating the MetaTrader version.
Provisioning profile id must not be included in the request for automatic broker settings detection.

.. code-block:: python

    try:
        account = await api.metatrader_account_api.create_account(account={
          'name': 'Trading account #1',
          'type': 'cloud',
          'login': '1234567',
          'platform': 'mt4',
          # password can be investor password for read-only access
          'password': 'qwerty',
          'server': 'ICMarketsSC-Demo',
          'application': 'MetaApi',
          'magic': 123456,
          'quoteStreamingIntervalInSeconds': 2.5, # set to 0 to receive quote per tick
          'reliability': 'regular' # set this field to 'high' value if you want to increase uptime of your account (recommended for production environments)
        })
    except Exception as err:
        # process errors
        if hasattr(err, 'details'):
            # returned if the server file for the specified server name has not been found
            # recommended to check the server name or create the account using a provisioning profile
            if err.details == 'E_SRV_NOT_FOUND':
                print(err)
            # returned if the server has failed to connect to the broker using your credentials
            # recommended to check your login and password
            elif err.details == 'E_AUTH':
                print(err)
            # returned if the server has failed to detect the broker settings
            # recommended to try again later or create the account using a provisioning profile
            elif err.details == 'E_SERVER_TIMEZONE':
                print(err)

If the settings have not yet been detected for the broker, the server will begin the process of detection, and you will receive a response with wait time:

.. code-block:: python

    Retrying request in 60 seconds because request returned message: Automatic broker settings detection is in progress, please retry in 60 seconds

The client will automatically retry the request when the recommended time passes.

Error handling
^^^^^^^^^^^^^^
Several types of errors are possible during the request:

- Server file not found
- Authentication error
- Settings detection error

Server file not found
"""""""""""""""""""""
This error is returned if the server file for the specified server name has not been found. In case of this error it
is recommended to check the server name. If the issue persists, it is recommended to create the account using a
provisioning profile.

.. code-block:: python

    {
        "id": 3,
        "error": "ValidationError",
        "message": "We were unable to retrieve the server file for this broker. Please check the server name or configure the provisioning profile manually.",
        "details": "E_SRV_NOT_FOUND"
    }

Authentication error
""""""""""""""""""""
This error is returned if the server has failed to connect to the broker using your credentials. In case of this
error it is recommended to check your login and password, and try again.

.. code-block:: python

    {
        "id": 3,
        "error": "ValidationError",
        "message": "We failed to authenticate to your broker using credentials provided. Please check that your MetaTrader login, password and server name are correct.",
        "details": "E_AUTH"
    }

Settings detection error
""""""""""""""""""""""""
This error is returned if the server has failed to detect the broker settings. In case of this error it is recommended
to retry the request later, or create the account using a provisioning profile.

.. code-block:: python

    {
        "id": 3,
        "error": "ValidationError",
        "message": "We were not able to retrieve server settings using credentials provided. Please try again later or configure the provisioning profile manually.",
        "details": "E_SERVER_TIMEZONE"
    }

Creating an account using a provisioning profile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If creating the account with automatic broker settings detection has failed, you can create it using a `provisioning profile. <#managing-provisioning-profiles>`_
To create an account using a provisioning profile, create a provisioning profile for the MetaTrader server, and then add the provisioningProfileId field to the request:

.. code-block:: python

    account = await api.metatrader_account_api.create_account(account={
      'name': 'Trading account #1',
      'type': 'cloud',
      'login': '1234567',
      # password can be investor password for read-only access
      'password': 'qwerty',
      'server': 'ICMarketsSC-Demo',
      'provisioningProfileId': provisioningProfile.id,
      'application': 'MetaApi',
      'magic': 123456,
      'quoteStreamingIntervalInSeconds': 2.5, # set to 0 to receive quote per tick
      'reliability': 'regular' # set this field to 'high' value if you want to increase uptime of your account (recommended for production environments)
    })

Retrieving existing accounts via API
------------------------------------
.. code-block:: python

    # filter and paginate accounts, see doc for full list of filter options available
    accounts = await api.metatrader_account_api.get_accounts(accounts_filter={
        'limit': 10,
        'offset': 0,
        'query': 'ICMarketsSC-MT5',
        'state': ['DEPLOYED']
    })
    # get accounts without filter (returns 1000 accounts max)
    accounts = await api.metatrader_account_api.get_accounts();

    account = await api.metatrader_account_api.get_account(account_id='accountId')

Updating an existing account via API
------------------------------------
.. code-block:: python

    await account.update(account={
        'name': 'Trading account #1',
        'login': '1234567',
        # password can be investor password for read-only access
        'password': 'qwerty',
        'server': 'ICMarketsSC-Demo',
        'quoteStreamingIntervalInSeconds': 2.5
    })

Removing an account
-------------------
.. code-block:: python

    await account.remove()

Deploying, undeploying and redeploying an account (API server) via API
----------------------------------------------------------------------
.. code-block:: python

    await account.deploy()
    await account.undeploy()
    await account.redeploy()

Manage custom experts (EAs)
---------------------------
Custom expert advisors can only be used for MT4 accounts on g1 infrastructure. EAs which use DLLs are not supported.

Creating an expert advisor via API
----------------------------------
You can use the code below to create an EA. Please note that preset field is a base64-encoded preset file.

.. code-block:: python

    expert = await account.create_expert_advisor(expert_id='expertId', expert={
        'period': '1h',
        'symbol': 'EURUSD',
        'preset': 'a2V5MT12YWx1ZTEKa2V5Mj12YWx1ZTIKa2V5Mz12YWx1ZTMKc3VwZXI9dHJ1ZQ'
    })
    await expert.upload_file('/path/to/custom-ea')

Retrieving existing experts via API
-----------------------------------

.. code-block:: python

    experts = await account.get_expert_advisors()

Retrieving existing expert by id via API
----------------------------------------

.. code-block:: python

    expert = await account.get_expert_advisor(expert_id='expertId')

Updating existing expert via API
--------------------------------
You can use the code below to update an EA. Please note that preset field is a base64-encoded preset file.

.. code-block:: python

    await expert.update(expert={
        'period': '4h',
        'symbol': 'EURUSD',
        'preset': 'a2V5MT12YWx1ZTEKa2V5Mj12YWx1ZTIKa2V5Mz12YWx1ZTMKc3VwZXI9dHJ1ZQ'
    })
    await expert.upload_file('/path/to/custom-ea')

Removing expert via API
-----------------------

.. code-block:: python

    await expert.remove()

Managing provisioning profiles
==============================
Provisioning profiles can be used as an alternative way to create MetaTrader accounts if the automatic broker settings
detection has failed.

Managing provisioning profiles via web UI
-----------------------------------------
You can manage provisioning profiles here: https://app.metaapi.cloud/provisioning-profiles

Creating a provisioning profile via API
---------------------------------------
.. code-block:: python

    # if you do not have created a provisioning profile for your broker,
    # you should do it before creating an account
    provisioningProfile = await api.provisioning_profile_api.create_provisioning_profile(profile={
        'name': 'My profile',
        'version': 5,
        'brokerTimezone': 'EET',
        'brokerDSTSwitchTimezone': 'EET'
    })
    # servers.dat file is required for MT5 profile and can be found inside
    # config directory of your MetaTrader terminal data folder. It contains
    # information about available broker servers
    await provisioningProfile.upload_file(file_name='servers.dat', file='/path/to/servers.dat')
    # for MT4, you should upload an .srv file instead
    await provisioningProfile.upload_file(file_name='broker.srv', file='/path/to/broker.srv')

Retrieving existing provisioning profiles via API
-------------------------------------------------
.. code-block:: python

    provisioningProfiles = await api.provisioning_profile_api.get_provisioning_profiles()
    provisioningProfile = await api.provisioning_profile_api.get_provisioning_profile(provisioning_profile_id='profileId')

Updating a provisioning profile via API
---------------------------------------
.. code-block:: python

    await provisioningProfile.update(profile={'name': 'New name'})
    # for MT5, you should upload a servers.dat file
    await provisioningProfile.upload_file(file_name='servers.dat', file='/path/to/servers.dat')
    # for MT4, you should upload an .srv file instead
    await provisioningProfile.upload_file(file_name='broker.srv', file='/path/to/broker.srv')

Removing a provisioning profile
-------------------------------
.. code-block:: python

    await provisioningProfile.remove()

Access MetaTrader account via RPC API
=====================================
RPC API let you query the trading terminal state. You should use
RPC API if you develop trading monitoring apps like myfxbook or other
simple trading apps.

Query account information, positions, orders and history via RPC API
--------------------------------------------------------------------
.. code-block:: python

    connection = account.get_rpc_connection()

    await connection.connect()
    await connection.wait_synchronized()

    # retrieve balance and equity
    print(await connection.get_account_information())
    # retrieve open positions
    print(await connection.get_positions())
    # retrieve a position by id
    print(await connection.get_position(position_id='1234567'))
    # retrieve pending orders
    print(await connection.get_orders())
    # retrieve a pending order by id
    print(await connection.get_order(order_id='1234567'))
    # retrieve history orders by ticket
    print(await connection.get_history_orders_by_ticket(ticket='1234567'))
    # retrieve history orders by position id
    print(await connection.get_history_orders_by_position(position_id='1234567'))
    # retrieve history orders by time range
    print(await connection.get_history_orders_by_time_range(start_time=start_time, end_time=end_time))
    # retrieve history deals by ticket
    print(await connection.get_deals_by_ticket(ticket='1234567'))
    # retrieve history deals by position id
    print(await connection.get_deals_by_position(position_id='1234567'))
    # retrieve history deals by time range
    print(await connection.get_deals_by_time_range(start_time=start_time, end_time=end_time))

Query contract specifications and quotes via RPC API
----------------------------------------------------
.. code-block:: python

    connection = account.get_rpc_connection()

    await connection.connect()
    await connection.wait_synchronized()

    # first, subscribe to market data
    await connection.subscribe_to_market_data(symbol='GBPUSD')

    # read symbols available
    print(await connection.get_symbols())
    # read contract specification
    print(await connection.get_symbol_specification(symbol='GBPUSD'))
    # read current price
    print(await connection.get_symbol_price(symbol='GBPUSD'))

    # unsubscribe from market data when no longer needed
    await connection.unsubscribe_from_market_data(symbol='GBPUSD')

Query historical market data via RPC API
----------------------------------------
Currently this API is supported on G1 only.

.. code-block:: python

    from datetime import datetime

    # retrieve 1000 candles before the specified time
    candles = await account.get_historical_candles(symbol='EURUSD', timeframe='1m',
                                                   start_time=datetime.fromisoformat('2021-05-01'), limit=1000)

    # retrieve 1000 ticks after the specified time
    ticks = await account.get_historical_ticks(symbol='EURUSD', start_time=datetime.fromisoformat('2021-05-01'),
                                               offset=5, limit=1000)

    # retrieve 1000 latest ticks
    ticks = await account.get_historical_ticks(symbol='EURUSD', start_time=None, offset=0, limit=1000)

Use real-time streaming API
---------------------------
Real-time streaming API is good for developing trading applications like trade copiers or automated trading strategies.
The API synchronizes the terminal state locally so that you can query local copy of the terminal state really fast.

Synchronizing and reading terminal state
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    from datetime import datetime

    account = await api.metatrader_account_api.get_account(account_id='accountId')
    connection = account.get_streaming_connection()
    await connection.connect()

    # access local copy of terminal state
    terminalState = connection.terminal_state

    # wait until synchronization completed
    await connection.wait_synchronized()

    print(terminalState.connected)
    print(terminalState.connected_to_broker)
    print(terminalState.account_information)
    print(terminalState.positions)
    print(terminalState.orders)
    # symbol specifications
    print(terminalState.specifications)
    print(terminalState.specification(symbol='EURUSD'))
    print(terminalState.price(symbol='EURUSD'))

    # access history storage
    historyStorage = connection.history_storage

    # both orderSynchronizationFinished and dealSynchronizationFinished
    # should be true once history synchronization have finished
    print(historyStorage.order_synchronization_finished)
    print(historyStorage.deal_synchronization_finished)

    print(historyStorage.deals)
    print(historyStorage.get_deals_by_ticket('1'))
    print(historyStorage.get_deals_by_position('1'))
    print(historyStorage.get_deals_by_time_range(
        datetime.fromtimestamp(datetime.now().timestamp() - 24 * 60 * 60), datetime.now())

    print(historyStorage.history_orders)
    print(historyStorage.get_history_orders_by_ticket('1'))
    print(historyStorage.get_history_orders_by_position('1'))
    print(historyStorage.get_history_orders_by_time_range(
        datetime.fromtimestamp(datetime.now().timestamp() - 24 * 60 * 60), datetime.now())

Overriding local history storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default history is stored in memory only. You can override history storage to save trade history to a persistent storage like MongoDB database.

.. code-block:: python

    from metaapi_cloud_sdk import HistoryStorage

    class MongodbHistoryStorage(HistoryStorage):
        # implement the abstract methods, see MemoryHistoryStorage for sample
        # implementation

    historyStorage = MongodbHistoryStorage()

    # Note: if you will not specify history storage, then in-memory storage
    # will be used (instance of MemoryHistoryStorage)
    connection = account.get_streaming_connection(history_storage=historyStorage)
    await connection.connect()

    # access history storage
    historyStorage = connection.history_storage;

    # invoke other methods provided by your history storage implementation
    print(await historyStorage.yourMethod())

Receiving synchronization events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can override SynchronizationListener in order to receive synchronization event notifications, such as account/position/order/history updates or symbol quote updates.

.. code-block:: python

    from metaapi_cloud_sdk import SynchronizationListener

    # receive synchronization event notifications
    # first, implement your listener
    class MySynchronizationListener(SynchronizationListener):
        # override abstract methods you want to receive notifications for

    # retrieving a connection
    connection = account.get_streaming_connection(history_storage=historyStorage)

    # now add the listener
    listener = MySynchronizationListener()
    connection.add_synchronization_listener(listener=listener)

    # remove the listener when no longer needed
    connection.remove_synchronization_listener(listener=listener)

    # open the connection after adding listeners
    await connection.connect()

Retrieve contract specifications and quotes via streaming API
-------------------------------------------------------------
.. code-block:: python

    connection = account.get_streaming_connection()
    await connection.connect()

    await connection.wait_synchronized()

    # first, subscribe to market data
    await connection.subscribe_to_market_data(symbol='GBPUSD')

    # read contract specification
    print(terminalState.specification(symbol='EURUSD'))

    # read current price
    print(terminalState.price(symbol='EURUSD'))

    # unsubscribe from market data when no longer needed
    await connection.unsubscribe_from_market_data(symbol='GBPUSD')

Execute trades (both RPC and streaming APIs)
--------------------------------------------
.. code-block:: python

    connection = account.get_rpc_connection()
    # or
    connection = account.get_streaming_connection()

    await connection.connect()
    await connection.wait_synchronized()

    # trade
    print(await connection.create_market_buy_order(symbol='GBPUSD', volume=0.07, stop_loss=0.9, take_profit=2.0,
        options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_market_sell_order(symbol='GBPUSD', volume=0.07, stop_loss=2.0, take_profit=0.9,
        options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_limit_buy_order(symbol='GBPUSD', volume=0.07, open_price=1.0, stop_loss=0.9,
        take_profit=2.0, options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_limit_sell_order(symbol='GBPUSD', volume=0.07, open_price=1.5, stop_loss=2.0,
        take_profit=0.9, options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_stop_buy_order(symbol='GBPUSD', volume=0.07, open_price=1.5, stop_loss=2.0,
        take_profit=0.9, options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_stop_sell_order(symbol='GBPUSD', volume=0.07, open_price=1.0, stop_loss=2.0,
        take_profit=0.9, options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_stop_limit_buy_order(symbol='GBPUSD', volume=0.07, open_price=1.5,
        stop_limit_price=1.4, stop_loss=0.9, take_profit=2.0, options={'comment': 'comment',
        'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.create_stop_limit_sell_order(symbol='GBPUSD', volume=0.07, open_price=1.0,
        stop_limit_price=1.1, stop_loss=2.0, take_profit=0.9, options={'comment': 'comment',
        'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print(await connection.modify_position(position_id='46870472', stop_loss=2.0, take_profit=0.9))
    print(await connection.close_position_partially(position_id='46870472', volume=0.9))
    print(await connection.close_position(position_id='46870472'))
    print(await connection.close_by(position_id='46870472', opposite_position_id='46870482'))
    print(await connection.close_positions_by_symbol(symbol='EURUSD'))
    print(await connection.modify_order(order_id='46870472', open_price=1.0, stop_loss=2.0, take_profit=0.9))
    print(await connection.cancel_order(order_id='46870472'))

    # if you need to, check the extra result information in stringCode and numericCode properties of the response
    result = await connection.create_market_buy_order(symbol='GBPUSD', volume=0.07, stop_loss=0.9, take_profit=2.0,
        options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'}))
    print('Trade successful, result code is ' + result['stringCode'])

    # catch and output exception
    try:
        await connection.create_market_buy_order(symbol='GBPUSD', volume=0.07, stop_loss=0.9, take_profit=2.0,
            options={'comment': 'comment', 'clientId': 'TE_GBPUSD_7hyINWqAl'})
    except Exception as err:
        print(api.format_error(err))

Trailing stop loss
^^^^^^^^^^^^^^^^^^
Trailing stop loss is a trade option that allows you to automatically configure and change the order/position stop loss
based on the current price of the symbol. The specified settings are run on the server and modify the stop loss
regardless of your connection to the account. The stop loss can be modified no more often than once in 15 seconds. Two
types of trailing stop loss are available: distance stop loss and threshold stop loss, but both can be specified at the
same time. You can find the full description here:
`https://metaapi.cloud/docs/client/models/trailingStopLoss/ <https://metaapi.cloud/docs/client/models/trailingStopLoss/>`_

.. code-block:: python

    # distance trailing stop loss
    print(await connection.create_market_buy_order('GBPUSD', 0.07, 0.9, 2.0, {
        'trailingStopLoss': {
            'distance': {
                'distance': 200,
                'units': 'RELATIVE_POINTS'
            }
        }
    }))

    # threshold trailing stop loss
    print(await connection.create_market_buy_order('GBPUSD', 0.07, 0.9, 2.0, {
        'trailingStopLoss': {
            'thresholds': [
                {
                    'threshold": 50,
                    'stopLoss": 100
                },
                {
                    'threshold": 100,
                    'stopLoss": 50
                }
            ],
            'units': 'RELATIVE_POINTS'
        }
    }))

Monitoring account connection health and uptime
===============================================
You can monitor account connection health using MetaApiConnection.health_monitor API.

.. code-block:: python

    monitor = connection.health_monitor
    # retrieve server-side app health status
    print(monitor.server_health_status)
    # retrieve detailed connection health status
    print(monitor.health_status)
    # retrieve account connection update measured over last 7 days
    print(monitor.uptime)

Tracking latencies
==================
You can track latencies using MetaApi.latency_monitor API. Client-side latencies include network communication delays, thus the lowest client-side latencies are achieved if you host your app in AWS Ohio region.

.. code-block:: python

    api = MetaApi('token', {'enableLatencyMonitor': True})
    monitor = api.latency_monitor
    # retrieve trade latency stats
    print(monitor.trade_latencies)
    # retrieve update streaming latency stats
    print(monitor.update_latencies)
    # retrieve quote streaming latency stats
    print(monitor.price_latencies)
    # retrieve request latency stats
    print(monitor.request_latencies)

Managing MetaTrader accounts via API
=========================================
Please note that not all MT4/MT5 servers allows you to create demo accounts using the method below.

Create a MetaTrader 4 demo account
----------------------------------
.. code-block:: python

    demo_account = await api.metatrader_account_generator_api.create_mt4_demo_account(
        account={
            'balance': 100000,
            'accountType': 'type',
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901'
        })

    # optionally specify a provisioning profile id if servers file is not found by server name
    demo_account = await api.metatrader_account_generator_api.create_mt4_demo_account(
        account={
            'balance': 100000,
            'accountType': 'type',
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901'
        }, profile_id=provisioningProfile.id)

Create a MetaTrader 4 live account
----------------------------------
.. code-block:: python

    live_account = await api.metatrader_account_generator_api.create_mt4_live_account(
        account={
            'balance': 100000,
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901',
            'country': 'Unites States',
            'zip': '12345',
            'state': 'New York',
            'city': 'New York',
            'address': 'customer address'
        })

    # optionally specify a provisioning profile id if servers file is not found by server name
    live_account = await api.metatrader_account_generator_api.create_mt4_live_account(
        account={
            'balance': 100000,
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901',
            'country': 'Unites States',
            'zip': '12345',
            'state': 'New York',
            'city': 'New York',
            'address': 'customer address'
        }, profile_id=provisioningProfile.id)

Create a MetaTrader 5 demo account
----------------------------------
.. code-block:: python

    demo_account = await api.metatrader_demo_account_api.create_mt5_demo_account(
        account={
            'accountType': 'type',
            'balance': 100000,
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'ICMarketsSC-Demo'
        })

    # optionally specify a provisioning profile id if servers file is not found by server name
    demo_account = await api.metatrader_account_generator_api.create_mt5_demo_account(
        account={
            'accountType': 'type',
            'balance': 100000,
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901'
        }, profile_id=provisioningProfile.id)

Create a MetaTrader 5 live account
----------------------------------
.. code-block:: python

    live_account = await api.metatrader_account_generator_api.create_mt5_live_account(
        account={
            'accountType': 'type',
            'balance': 100000,
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901',
            'country': 'Unites States',
            'zip': '12345',
            'state': 'New York',
            'city': 'New York',
            'address': 'customer address'
        })

    # optionally specify a provisioning profile id if servers file is not found by server name
    live_account = await api.metatrader_account_generator_api.create_mt5_live_account(
        account={
            'accountType': 'type',
            'balance': 100000,
            'email': 'example@example.com',
            'leverage': 100,
            'serverName': 'Exness-Trial4',
            'name': 'Test User',
            'phone': '+12345678901',
            'country': 'Unites States',
            'zip': '12345',
            'state': 'New York',
            'city': 'New York',
            'address': 'customer address'
        }, profile_id=provisioningProfile.id)

Enable Logging logging
===========================================
By default SDK logs messages to console. You can select the SDK to use `logging <https://docs.python.org/3/library/logging.html>`_ logging
library by calling `MetaApi.enable_logging()` static method before creating MetaApi instances.
.. code-block:: python

    from metaapi_cloud_sdk import MetaApi

    MetaApi.enable_logging()

    meta_api = MetaApi(token)

Please note that the SDK does not configure logging automatically. If you decide to use logging, then your application
is still responsible to configuring logging appenders and categories. Please refer to logging documentation for details.

Rate limits & quotas
===========================================
API calls you make are subject to rate limits. See `MT account management API <https://metaapi.cloud/docs/provisioning/rateLimiting/>`_ and `MetaApi API <https://metaapi.cloud/docs/client/rateLimiting/>`_ for details.

MetaApi applies quotas to the number of accounts and provisioning profiles, for more details see the `MT account management API quotas <https://metaapi.cloud/docs/provisioning/userQuota/>`_

CopyFactory copy trading API
===========================================

CopyFactory is a powerful trade copying API which makes developing forex
trade copying applications as easy as writing few lines of code.

You can find CopyFactory Python SDK documentation here: `https://github.com/agiliumtrade-ai/copyfactory-python-sdk <https://github.com/agiliumtrade-ai/copyfactory-python-sdk>`_

MetaStats trading statistics API
===========================================

MetaStats is a powerful trade statistics API which makes it possible to add forex trading metrics into forex
applications.

You can find MetaStats Python SDK documentation here:
`https://github.com/agiliumtrade-ai/metastats-python-sdk <https://github.com/agiliumtrade-ai/metastats-python-sdk>`_

MetaApi MT manager API
======================

MetaApi MT manager API is a cloud REST API which can be used to access and manage MT4 and MT5 servers.

You can find MT manager API documentation here: `https://metaapi.cloud/docs/manager/ <https://metaapi.cloud/docs/manager/>`_

MetaApi risk management API
===========================

MetaApi risk management API is a cloud API for executing trading challenges and competitions.
You can use this API for e.g. if you want to launch a proprietary trading company like FTMO.
The API is also useful for trading firms/teams which have to enforce trading risk restrictions.

You can find MetaApi risk management Python SDK documentation here: `https://github.com/agiliumtrade-ai/risk-management-python-sdk <https://github.com/agiliumtrade-ai/risk-management-python-sdk>`_
