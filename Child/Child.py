from APIs.API import DhanAPI


class Child:
    def __init__(self, clientId, APIToken):
        self.DHANAPI = DhanAPI(clientId, APIToken)
        self.ExecutedOrders = []

    def ExecuteCopyOrder(self, data):
        self.OrderResponse = self.DHANAPI.PlaceOrder(
            security_id = data["securityId"],
            exchange_segment = data["exchangeSegment"],
            transaction_type = data["transactionType "],
            quantity = data["quantity"], 
            order_type = data["order_type"],
            product_type = data["product_type"],
            price = data["price"],
            trigger_price = data["triggerPrice"],
            disclosed_quantity= data["disclosedQuantity"], 
            after_market_order=data["afterMarketOrder"],
            validity=data["validity"],
            amo_time='OPEN', 
            bo_profit_value=data["boProfitValue"],
            bo_stop_loss_Value=data["boStopLossValue"], 
            drv_expiry_date= data["drvExpiryDate"],
            drv_options_type=data["drvOptionType"],
            drv_strike_price=data["drvStrikePrice"],
            tag="Order Created by Akshay Kotish's API"
        )
        orderid = self.OrderResponse["data"][0]["orderId"]
        if orderid not in self.ExecutedOrders:
            self.ExecutedOrders.append(orderid)

    def ModifyOrder(self, data):
        self.OrderResponse = self.DHANAPI.ModifyOrder(
            order_id = data["orderId"],
            order_type = data["orderType"],
            leg_name = data["legName"],
            quantity = data["quantity"],
            price = data["price"],
            trigger_price = data["triggerPrice"],
            disclosed_quantity = data["disclosedQuantity"],
            validity = data["validity"]
        )

    def CancelOrder(self, orderIndex):
        orderid = self.ExecutedOrders[orderIndex]
        self.OrderResponse = self.DHANAPI.CancelOrder(orderid)
        self.ExecutedOrders.remove(orderid)

        

#'dhanClientId': '1100284759', 'orderId': '252405148427', 'exchangeOrderId': '0', 'correlationId': '1100284759-1715659348311', 'orderStatus': 'PENDING', 'transactionType': 'BUY', 'exchangeSegment': 'NSE_EQ', 'productType': 'CNC', 'orderType': 'MARKET', 'validity': 'DAY', 'tradingSymbol': 'EXCEL', 'securityId': '17376', 'quantity': 10, 'disclosedQuantity': 0, 'price': 0.0, 'triggerPrice': 0.0, 'afterMarketOrder': True, 'boProfitValue': 0.0, 'boStopLossValue': 0.0, 'legName': 'NA', 'createTime': '2024-05-14 09:32:28', 'updateTime': '2024-05-14 09:32:28', 'exchangeTime': '0001-01-01 00:00:00', 'drvExpiryDate': '0001-01-01', 'drvOptionType': 'NA', 'drvStrikePrice': 0.0, 'omsErrorCode': '0', 'omsErrorDescription': '', 'filled_qty': 0, 'algoId': '0'