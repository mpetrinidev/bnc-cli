def get_exchange_info():
    return {
        "timezone": "UTC",
        "serverTime": 1616520211238,
        "rateLimits": [
            {
                "rateLimitType": "REQUEST_WEIGHT",
                "interval": "MINUTE",
                "intervalNum": 1,
                "limit": 1200
            },
            {
                "rateLimitType": "ORDERS",
                "interval": "SECOND",
                "intervalNum": 10,
                "limit": 100
            },
            {
                "rateLimitType": "ORDERS",
                "interval": "DAY",
                "intervalNum": 1,
                "limit": 200000
            }
        ],
        "exchangeFilters": [],
        "symbols": [
            {
                "symbol": "BNBBUSD",
                "status": "TRADING",
                "baseAsset": "BNB",
                "baseAssetPrecision": 8,
                "quoteAsset": "BUSD",
                "quotePrecision": 8,
                "quoteAssetPrecision": 8,
                "baseCommissionPrecision": 8,
                "quoteCommissionPrecision": 8,
                "orderTypes": [
                    "LIMIT",
                    "LIMIT_MAKER",
                    "MARKET",
                    "STOP_LOSS_LIMIT",
                    "TAKE_PROFIT_LIMIT"
                ],
                "icebergAllowed": True,
                "ocoAllowed": True,
                "quoteOrderQtyMarketAllowed": True,
                "isSpotTradingAllowed": True,
                "isMarginTradingAllowed": False,
                "filters": [
                    {
                        "filterType": "PRICE_FILTER",
                        "minPrice": "0.00010000",
                        "maxPrice": "10000.00000000",
                        "tickSize": "0.00010000"
                    },
                    {
                        "filterType": "PERCENT_PRICE",
                        "multiplierUp": "5",
                        "multiplierDown": "0.2",
                        "avgPriceMins": 1
                    },
                    {
                        "filterType": "LOT_SIZE",
                        "minQty": "0.01000000",
                        "maxQty": "9000.00000000",
                        "stepSize": "0.01000000"
                    },
                    {
                        "filterType": "MIN_NOTIONAL",
                        "minNotional": "10.00000000",
                        "applyToMarket": True,
                        "avgPriceMins": 1
                    },
                    {
                        "filterType": "ICEBERG_PARTS",
                        "limit": 10
                    },
                    {
                        "filterType": "MARKET_LOT_SIZE",
                        "minQty": "0.00000000",
                        "maxQty": "1000.00000000",
                        "stepSize": "0.00000000"
                    },
                    {
                        "filterType": "MAX_NUM_ORDERS",
                        "maxNumOrders": 200
                    },
                    {
                        "filterType": "MAX_NUM_ALGO_ORDERS",
                        "maxNumAlgoOrders": 5
                    }
                ],
                "permissions": [
                    "SPOT"
                ]
            },
            {
                "symbol": "BTCBUSD",
                "status": "TRADING",
                "baseAsset": "BTC",
                "baseAssetPrecision": 8,
                "quoteAsset": "BUSD",
                "quotePrecision": 8,
                "quoteAssetPrecision": 8,
                "baseCommissionPrecision": 8,
                "quoteCommissionPrecision": 8,
                "orderTypes": [
                    "LIMIT",
                    "LIMIT_MAKER",
                    "MARKET",
                    "STOP_LOSS_LIMIT",
                    "TAKE_PROFIT_LIMIT"
                ],
                "icebergAllowed": True,
                "ocoAllowed": True,
                "quoteOrderQtyMarketAllowed": True,
                "isSpotTradingAllowed": True,
                "isMarginTradingAllowed": False,
                "filters": [
                    {
                        "filterType": "PRICE_FILTER",
                        "minPrice": "0.01000000",
                        "maxPrice": "1000000.00000000",
                        "tickSize": "0.01000000"
                    },
                    {
                        "filterType": "PERCENT_PRICE",
                        "multiplierUp": "5",
                        "multiplierDown": "0.2",
                        "avgPriceMins": 1
                    },
                    {
                        "filterType": "LOT_SIZE",
                        "minQty": "0.00000100",
                        "maxQty": "900.00000000",
                        "stepSize": "0.00000100"
                    },
                    {
                        "filterType": "MIN_NOTIONAL",
                        "minNotional": "10.00000000",
                        "applyToMarket": True,
                        "avgPriceMins": 1
                    },
                    {
                        "filterType": "ICEBERG_PARTS",
                        "limit": 10
                    },
                    {
                        "filterType": "MARKET_LOT_SIZE",
                        "minQty": "0.00000000",
                        "maxQty": "100.00000000",
                        "stepSize": "0.00000000"
                    },
                    {
                        "filterType": "MAX_NUM_ALGO_ORDERS",
                        "maxNumAlgoOrders": 5
                    },
                    {
                        "filterType": "MAX_NUM_ORDERS",
                        "maxNumOrders": 200
                    }
                ],
                "permissions": [
                    "SPOT"
                ]
            }
        ]
    }


def get_trades():
    return [
        {
            "id": 1035,
            "price": "0.00346000",
            "qty": "0.08203000",
            "quoteQty": "0.00028382",
            "time": 1616520055355,
            "isBuyerMaker": True,
            "isBestMatch": True
        },
        {
            "id": 1036,
            "price": "0.00341200",
            "qty": "0.06255000",
            "quoteQty": "0.00021342",
            "time": 1616520055355,
            "isBuyerMaker": True,
            "isBestMatch": True
        }
    ]


def get_klines():
    return [
        [
            1616702100000,
            "0.00348400",
            "0.00348400",
            "0.00348400",
            "0.00348400",
            "0.00000000",
            1616702159999,
            "0.00000000",
            0,
            "0.00000000",
            "0.00000000",
            "0"
        ]
    ]


def get_current_avg_price():
    return {
        "mins": 1,
        "price": "0.00331289"
    }


def get_ticker_24hr():
    return {
        "symbol": "LTCBTC",
        "priceChange": "-0.00017500",
        "priceChangePercent": "-5.023",
        "weightedAvgPrice": "0.00348384",
        "prevClosePrice": "0.00348400",
        "lastPrice": "0.00330900",
        "lastQty": "0.03272000",
        "bidPrice": "0.00000000",
        "bidQty": "0.00000000",
        "askPrice": "0.00348400",
        "askQty": "94.50899000",
        "openPrice": "0.00348400",
        "highPrice": "0.00348400",
        "lowPrice": "0.00330900",
        "volume": "149.58702000",
        "quoteVolume": "0.52113708",
        "openTime": 1616616213627,
        "closeTime": 1616702613627,
        "firstId": 1072,
        "lastId": 1103,
        "count": 32
    }
