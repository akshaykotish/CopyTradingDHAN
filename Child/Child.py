from APIs.API import DhanAPI


class Child:
    def __init__(self, clientId, APIToken, multiplyvalue = 1):
        self.clientId = clientId
        self.multiplyvalue = multiplyvalue
        self.DHANAPI = DhanAPI(clientId, APIToken)
        self.PlacedOrders = []

        
    def LoadPrePlacedOrder(self):
        m_res = self.DHANAPI.GetOrders()
        for ordr in m_res["data"]:
            #lastupdate = ordr["updateTime"]
            orderid = ordr["orderId"]
            #orderstatus = ordr["orderStatus"]

            if orderid not in self.PlacedOrders:
                self.PlacedOrders.append(orderid)

    def AddOrdersIndex(self, orderIndex):
        if orderIndex not in self.PlacedOrders:
            self.PlacedOrders.append(orderIndex)

    def ExecuteCopyOrder(self, data):
        #print("Executed Copy Order", data)
        self.OrderResponse = self.DHANAPI.PlaceOrder(
            security_id = data["securityId"],
            exchange_segment = data["exchangeSegment"],
            transaction_type = data["transactionType"],
            quantity = int(data["quantity"]) * self.multiplyvalue, 
            order_type = data["orderType"],
            product_type = data["productType"],
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
            tag=""
        )
        
        if len(self.OrderResponse["data"]) > 0:
            orderid = self.OrderResponse["data"][0]["orderId"]
            if orderid not in self.PlacedOrders:
                self.PlacedOrders.append(orderid)
        else:
            print("Order Not Executed for Client Id ", self.clientId)

    def ModifyOrder(self, data, index):
        print("Order Modified")
        if index < len(self.PlacedOrders):
            self.OrderResponse = self.DHANAPI.ModifyOrder(
                order_id = self.PlacedOrders[index],
                order_type = data["orderType"],
                leg_name = data["legName"],
                quantity = data["quantity"] * self.multiplyvalue,
                price = data["price"],
                trigger_price = data["triggerPrice"],
                disclosed_quantity = data["disclosedQuantity"],
                validity = data["validity"]
        )

    def CancelOrder(self, orderIndex):
        print("Order Canceled")
        if orderIndex < len(self.PlacedOrders):
            orderid = self.PlacedOrders[orderIndex]
            self.OrderResponse = self.DHANAPI.CancelOrder(orderid)
            self.PlacedOrders.remove(orderid)
    
    def RemoveOrderIndex(self, orderIndex):
        if orderIndex < len(self.PlacedOrders): 
            orderid = self.PlacedOrders[orderIndex]
            self.PlacedOrders.remove(orderid)

    def TradedOrder(self, orderIndex):
        print("Order Traded")
        if orderIndex < len(self.PlacedOrders):
            orderid = self.PlacedOrders[orderIndex]
            self.PlacedOrders.remove(orderid)

        

#'dhanClientId': '1100284759', 'orderId': '252405148427', 'exchangeOrderId': '0', 'correlationId': '1100284759-1715659348311', 'orderStatus': 'PENDING', 'transactionType': 'BUY', 'exchangeSegment': 'NSE_EQ', 'productType': 'CNC', 'orderType': 'MARKET', 'validity': 'DAY', 'tradingSymbol': 'EXCEL', 'securityId': '17376', 'quantity': 10, 'disclosedQuantity': 0, 'price': 0.0, 'triggerPrice': 0.0, 'afterMarketOrder': True, 'boProfitValue': 0.0, 'boStopLossValue': 0.0, 'legName': 'NA', 'createTime': '2024-05-14 09:32:28', 'updateTime': '2024-05-14 09:32:28', 'exchangeTime': '0001-01-01 00:00:00', 'drvExpiryDate': '0001-01-01', 'drvOptionType': 'NA', 'drvStrikePrice': 0.0, 'omsErrorCode': '0', 'omsErrorDescription': '', 'filled_qty': 0, 'algoId': '0'