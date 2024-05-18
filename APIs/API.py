from dhanhq import dhanhq
import json

# dhan = dhanhq("1100284759","eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE4MjA5MzI4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDI4NDc1OSJ9.YKgzsfDimqekJBjbN34txp6-NE5KFiFNeFdVAA6TZ5-ETCwZrBchEs6-lvepTJWXXiGlevKbLsQqJ1ME-x5BhA")


# all_orders = dhan.get_order_list()
# #jsondata = json.dumps(all_orders)
# print(all_orders["status"])


class DhanAPI:

    def __init__(self, clientId, APIToken):
        self.dhan = dhanhq(clientId, APIToken)
    
    def PlaceOrder(self,security_id,exchange_segment,transaction_type,quantity, order_type,product_type,price,trigger_price=0,disclosed_quantity=0, after_market_order=False,validity='DAY',amo_time='OPEN', bo_profit_value=None,bo_stop_loss_Value=None, drv_expiry_date=None,drv_options_type=None,drv_strike_price=None,tag=None):
        res = self.dhan.place_order(
            security_id=security_id,
            exchange_segment=exchange_segment,
            transaction_type=transaction_type,
            quantity=quantity,
            order_type=order_type,
            product_type=product_type,
            after_market_order=after_market_order,
            price=price,
            trigger_price=trigger_price,
            disclosed_quantity=disclosed_quantity,
            validity=validity,
            amo_time=amo_time,
            bo_profit_value=bo_profit_value,
            bo_stop_loss_Value=bo_stop_loss_Value,
            drv_expiry_date=drv_expiry_date,
            drv_options_type=drv_options_type,
            drv_strike_price=drv_strike_price,
            tag=tag
        )

        print(res)
        return res
    
    def ModifyOrder(self,order_id,order_type,leg_name,quantity,price,trigger_price,disclosed_quantity,validity):
        res = self.dhan.modify_order(
            order_id = order_id,
            order_type = order_type,
            leg_name = leg_name,
            quantity = quantity,
            price = price,
            trigger_price = trigger_price,
            disclosed_quantity = disclosed_quantity,
            validity = validity
            )

        print(res)
        return res
        

    def GetOrders(self):
        self.all_orders = self.dhan.get_order_list()
        return self.all_orders
    
    def CancelOrder(self, OrderID):
        respose = self.dhan.cancel_order(OrderID)
        return respose
    

