import System.Threading


class ApartmentState(object):
    STA = System.Threading.ApartmentState.STA


class Thread(object):
    def __init__(self, Func):
        self.Class = System.Threading.Thread(Func.Class)

    def SetApartmentState(self, ApartmentState):
        self.Class.ApartmentState = ApartmentState

    def Start(self):
        self.Class.Start()

    def Join(self):
        self.Class.Join()


class ThreadStart(object):
    def __init__(self, Main):
        self.Class = System.Threading.ThreadStart(Main)