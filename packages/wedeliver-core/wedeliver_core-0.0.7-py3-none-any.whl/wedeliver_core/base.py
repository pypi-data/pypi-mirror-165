class WeDeliverCore:
    __app = None

    @staticmethod
    def getApp():
        """ Static access method. """
        if WeDeliverCore.__app == None:
            WeDeliverCore()
        return WeDeliverCore.__app

    def __init__(self, app=None):
        """ Virtually private constructor. """
        if WeDeliverCore.__app != None:
            raise Exception("This class is a singleton!")
        else:
            WeDeliverCore.__app = app
