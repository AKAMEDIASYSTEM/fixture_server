class ResponseObject():

    def __init__(self, status=500, msg="Unknown Error", data=None):
        self.status = status
        self.msg = msg
        if data:
            self.data = data
        else:
            self.data = {}

        self.response = { "status" : self.status, "msg" : self.msg, "data" : self.data }
