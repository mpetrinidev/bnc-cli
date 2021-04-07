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


def get_order_status():
    return {
        "symbol": "LTCBTC",
        "orderId": 44590,
        "orderListId": -1,
        "clientOrderId": "oM1oUenAxizVURTgnsG3pU",
        "price": "0.00362100",
        "origQty": "1.00000000",
        "executedQty": "0.00000000",
        "cummulativeQuoteQty": "0.00000000",
        "status": "CANCELED",
        "timeInForce": "GTC",
        "type": "STOP_LOSS_LIMIT",
        "side": "SELL",
        "stopPrice": "0.00100000",
        "icebergQty": "0.00000000",
        "time": 1616030090950,
        "updateTime": 1616376905442,
        "isWorking": True,
        "origQuoteOrderQty": "0.00000000"
    }
