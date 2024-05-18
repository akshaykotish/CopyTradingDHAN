from APIs.API import DhanAPI
import threading
import time


class Master:
    def __init__(self, clientId, APIToken):
        self.DHANAPI = DhanAPI(clientId, APIToken)
        self.PlacedOrders = []
        self.LastUpdate = []
        self.PendingList = []


    def TrackOrders(self):
        self.OrderResponse = self.DHANAPI.GetOrders()
        return self.OrderResponse
    
    def GetOrderIndex(self, OrderID):
        if OrderID not in self.PlacedOrders:
            return -1
        else:
            index = self.PlacedOrders.index(OrderID)
            return index

    def RemoveIndexOrder(self, Index):
        self.PlacedOrders.pop(Index)

