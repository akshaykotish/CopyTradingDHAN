from Master.Master import Master
from Child.Child import Child
import threading
import time

class Control:
    def __init__(self):
        self.master = Master("1100284759", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE4MjA5MzI4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDI4NDc1OSJ9.YKgzsfDimqekJBjbN34txp6-NE5KFiFNeFdVAA6TZ5-ETCwZrBchEs6-lvepTJWXXiGlevKbLsQqJ1ME-x5BhA")
        self.childs = [Child("", "")]

    def RunThread(self, chld, ordr):
        thread = threading.Thread(target=chld.ExecuteCopyOrder, args=(ordr))
        thread.start()
        thread.join()

    def Execute(self):

        nini = 1
        while(nini < 10):
            nini += 1
            m_res = self.master.TrackOrders()
            for ordr in m_res["data"]:
                lastupdate = ordr["updateTime"]
                orderid = ordr["orderId"]
                orderstatus = ordr["orderStatus"]

                if orderid not in self.master.ExecutedOrders:
                    if orderstatus == "TRANSIT" or orderstatus == "PENDING":
                        self.master.ExecutedOrders.append(orderid)
                        self.master.LastUpdate.append(lastupdate)
                
                print(orderid, orderstatus)
                indexoforder = self.master.GetOrderIndex(orderid)
                print(indexoforder)
                if indexoforder == -1:
                    continue

                if indexoforder != -1 and self.master.LastUpdate[indexoforder] != lastupdate:
                    if orderstatus == "TRANSIT":
                        print("Did not reach the exchange server")
                        for chld in self.childs:
                            self.RunThread(chld, ordr)


                    elif orderstatus == "PENDING":
                        print("Reached at exchange end, awaiting execution")
                        for chld in self.childs:
                            self.RunThread(chld, ordr)


                    elif orderstatus == "REJECTED":
                        print("Rejected at exchange/broker’s end")

                    elif orderstatus == "CANCELLED":
                        print("Cancelled by user")

                    elif orderstatus == "TRADED":
                        print("Executed")

                    elif orderstatus == "EXPIRED":
                        print("Validity of order is expired")

                
                self.master.LastUpdate[indexoforder] = lastupdate
