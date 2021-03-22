def get_account_info():
    return {
        "makerCommission": 15,
        "takerCommission": 15,
        "buyerCommission": 0,
        "sellerCommission": 0,
        "canTrade": True,
        "canWithdraw": True,
        "canDeposit": True,
        "updateTime": 123456789,
        "accountType": "SPOT",
        "balances": get_balances(),
        "permissions": [
            "SPOT"
        ]
    }


def get_balances():
    return [
        {
            "asset": "BTC",
            "free": "4723846.89208129",
            "locked": "0.00000000"
        },
        {
            "asset": "LTC",
            "free": "4763368.68006011",
            "locked": "0.00000000"
        },
        {
            "asset": "BNB",
            "free": "0.00000000",
            "locked": "10.250"
        }
    ]


def get_full_order_limit():
    return {
        "symbol": "LTCBTC",
        "orderId": 44588,
        "orderListId": -1,
        "clientOrderId": "Xxv5X3sWh6wxIPtlZxkKmS",
        "transactTime": 1616029165071,
        "price": "0.00362100",
        "origQty": "1.00000000",
        "executedQty": "0.00000000",
        "cummulativeQuoteQty": "0.00000000",
        "status": "NEW",
        "timeInForce": "GTC",
        "type": "LIMIT",
        "side": "BUY",
        "fills": []
    }


def get_full_order_market():
    return {
        "symbol": "LTCBTC",
        "orderId": 44589,
        "orderListId": -1,
        "clientOrderId": "6lcsZpGiMMwCQlwVLtfMXz",
        "transactTime": 1616029239160,
        "price": "0.00000000",
        "origQty": "1.00000000",
        "executedQty": "0.00000000",
        "cummulativeQuoteQty": "0.00000000",
        "status": "EXPIRED",
        "timeInForce": "GTC",
        "type": "MARKET",
        "side": "BUY",
        "fills": []
    }


def get_ack_order_stop_loss_limit():
    return {
        "symbol": "LTCBTC",
        "orderId": 44590,
        "orderListId": -1,
        "clientOrderId": "oM1oUenAxizVURTgnsG3pU",
        "transactTime": 1616030090950
    }


def get_ack_order_take_profit_limit():
    return {
        "symbol": "LTCBTC",
        "orderId": 44591,
        "orderListId": -1,
        "clientOrderId": "WHnGqkVEOYf6aIcJTuHfJa",
        "transactTime": 1616031609028
    }


def get_ack_order_limit_maker():
    return {
        "symbol": "LTCBTC",
        "orderId": 44592,
        "orderListId": -1,
        "clientOrderId": "iuq4RTzy2HHjw0LZp19JoT",
        "transactTime": 1616031749054
    }


def get_cancel_order():
    return {
        "symbol": "LTCBTC",
        "origClientOrderId": "oM1oUenAxizVURTgnsG3pU",
        "orderId": 44590,
        "orderListId": -1,
        "clientOrderId": "vmITMP7NPf3EfSmcyzX6JF",
        "price": "0.00362100",
        "origQty": "1.00000000",
        "executedQty": "0.00000000",
        "cummulativeQuoteQty": "0.00000000",
        "status": "CANCELED",
        "timeInForce": "GTC",
        "type": "STOP_LOSS_LIMIT",
        "side": "SELL",
        "stopPrice": "0.00100000"
    }


def get_open_orders():
    return [
        {
            "symbol": "LTCBTC",
            "orderId": 44590,
            "orderListId": -1,
            "clientOrderId": "oM1oUenAxizVURTgnsG3pU",
            "price": "0.00362100",
            "origQty": "1.00000000",
            "executedQty": "0.00000000",
            "cummulativeQuoteQty": "0.00000000",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "STOP_LOSS_LIMIT",
            "side": "SELL",
            "stopPrice": "0.00100000",
            "icebergQty": "0.00000000",
            "time": 1616030090950,
            "updateTime": 1616301810266,
            "isWorking": true,
            "origQuoteOrderQty": "0.00000000"
        }
    ]
