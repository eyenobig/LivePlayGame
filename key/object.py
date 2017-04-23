import json
class DanmuRecord:
    def __init__(self,*args):
        self.user = args[0]
        self.press = args[1]
        try:
            self.vote = args[2]
        except Exception:
            pass

    def json(self):
        txt = self.__dict__
        return txt

class VoteRecord:
    def __init__(self,result,setlist):
        self.result = result
        self.set = str(setlist)
        print(self.set)
    def json(self):
        txt = self.__dict__
        return txt

