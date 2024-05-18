from Master.Master import Master
from Child.Child import Child
import threading
import time
import csv


class Control:
    def __init__(self):
        self.master = Master("1100284759", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE4MjA5MzI4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDI4NDc1OSJ9.YKgzsfDimqekJBjbN34txp6-NE5KFiFNeFdVAA6TZ5-ETCwZrBchEs6-lvepTJWXXiGlevKbLsQqJ1ME-x5BhA")
        self.childs = []
        #self.childs = [Child("1100995950", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE4NDQ1MjczLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDk5NTk1MCJ9.avaar8KwZXH6MqdAK4R290RXsJ0DYon1jjQGdF-UEXk4cdNL-79yACHD8bQFshEKAcMBxA4bw1gQCC3a-dRZkw")]
        #Child("1100995950", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE4NDQ1MjczLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDk5NTk1MCJ9.avaar8KwZXH6MqdAK4R290RXsJ0DYon1jjQGdF-UEXk4cdNL-79yACHD8bQFshEKAcMBxA4bw1gQCC3a-dRZkw")
        self.LoadAPIsecrets()
        

    def LoadAPIsecrets(self):
        file_path = "./Childs.csv"
        try:
            with open(file_path, mode='r', newline='') as file:
                csv_reader = csv.reader(file)
                first_row = next(csv_reader, None)
                first_row = next(csv_reader, None)
                
                if first_row is None:
                    print("The CSV file is empty.")
                    return

                #print(f"Master: {first_row}")
                self.master = Master(first_row[2], first_row[3])

                
                for row in csv_reader:
                    #print(f"Child: {row}")
                    self.childs.append(Child(row[2], row[3], multiplyvalue=row[1]))
            
            #print(self.master)
            #print(self.childs)
                    
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def RunThread(self, chld, ordr):
        chld.ExecuteCopyOrder(ordr)
        # try:
        #     thread = threading.Thread(target=chld.ExecuteCopyOrder, args=(ordr))
        #     thread.start()
        #     thread.join()
        # finally:
        #     print("E")

    def Execute(self):

        nini = 1
        while(True):
            nini += 1
            m_res = self.master.TrackOrders()
            for ordr in m_res["data"]:
                lastupdate = ordr["updateTime"]
                orderid = ordr["orderId"]
                orderstatus = ordr["orderStatus"]

                if orderid not in self.master.PlacedOrders:
                    if orderstatus == "TRANSIT" or orderstatus == "PENDING" or orderstatus == "TRADED":
                        self.master.PlacedOrders.append(orderid)
                        self.master.LastUpdate.append("")
                        indexoforder = self.master.GetOrderIndex(orderid)
                        print("ORDER Added", orderid, lastupdate, indexoforder)
                
                #print(orderid, orderstatus)
                indexoforder = self.master.GetOrderIndex(orderid)
                #print(indexoforder, orderid)
                if indexoforder == -1:
                    #print("CELL")
                    continue
                # if indexoforder != -1:
                #     print("Roll")
                #     print(self.master.LastUpdate[indexoforder], lastupdate)
                    
                previousdate = self.master.LastUpdate[indexoforder]

                if indexoforder != -1 and previousdate != lastupdate:
                    print("Whole")
                    print(self.master.LastUpdate[indexoforder], lastupdate, indexoforder)

                    if orderstatus == "TRANSIT":
                        print("Did not reach the exchange server")

                        if orderid not in self.master.PendingList:
                            self.master.PendingList.append(orderid)


                        for chld in self.childs:
                            self.RunThread(chld, ordr)


                    elif orderstatus == "PENDING":
                        print("Reached at exchange end, awaiting execution")
                        if orderid not in self.master.PendingList:
                            self.master.PendingList.append(orderid)

                        for chld in self.childs:
                            if len(chld.PlacedOrders) > indexoforder:
                                print("Modify Order")
                                chld.ModifyOrder(ordr, indexoforder)
                            else:
                                print("Execute New Order")
                                self.RunThread(chld, ordr)


                    elif orderstatus == "REJECTED":
                        print("Rejected at exchange/broker’s end")
                        #self.master.
                        self.master.PlacedOrders.remove(orderid)
                        for chld in self.childs:
                            chld.CancelOrder(indexoforder)

                    elif orderstatus == "CANCELLED":
                        print("Cancelled by user")
                        self.master.PlacedOrders.remove(orderid)
                        for chld in self.childs:
                            chld.CancelOrder(indexoforder)

                    elif orderstatus == "TRADED":
                        print("Executed")
                        if orderid not in self.master.PendingList:
                            for chld in self.childs:
                                self.RunThread(chld, ordr)
                        

                    elif orderstatus == "EXPIRED":
                        print("Validity of order is expired")
                        self.master.PlacedOrders.remove(orderid)
                        for chld in self.childs:
                            chld.RemoveOrderIndex(indexoforder)

                
                self.master.LastUpdate[indexoforder] = lastupdate
