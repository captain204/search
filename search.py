

class Search:

    def __init__(connection,keyword):
        self._connection = connection
        self._keyword = keyword

    def find_by_batch(self,keyword):
        return self.connectVoucher.find({batch:batchNO})


    def find_by_userID(self,UserID):
        return self.connectVoucher.find({id:UserID})

       
    def find_by_username(self,username):
        return self.connectVoucher.find({username:username})


    def find_by_pinNum(self,pinNum):
        return self.connectVoucher.find({pin:pinNum})


    def find_by_serial_num(self,serialNum):
        return self.connectVoucher.find({serial_no:serialNum})
     
    def fullSearch(self,keyword):
        self.connectVoucher({"$text": { "$search":keyword} } )

    def PartialSearch(self,keyword):
        self.connectVoucher.find({"$text": { "$search":keyword} } )




       
        
        


