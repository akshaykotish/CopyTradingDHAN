from APIs.API import DhanAPI
import threading
import time


class Master:
    def __init__(self, clientId, APIToken):
        self.DHANAPI = DhanAPI(clientId, APIToken)
        self.ExecutedOrders = []
        self.LastUpdate = []

    def TrackOrders(self):
        self.OrderResponse = self.DHANAPI.GetOrders()
        return self.OrderResponse
    
    def GetOrderIndex(self, OrderID):
        if OrderID not in self.ExecutedOrders:
            return -1
        else:
            index = self.ExecutedOrders.index(OrderID)
            return index

    def RemoveIndexOrder(self, Index):
        self.ExecutedOrders.pop(Index)

