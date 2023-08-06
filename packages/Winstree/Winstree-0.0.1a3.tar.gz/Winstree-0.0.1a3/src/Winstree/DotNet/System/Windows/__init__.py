from Winstree import AddReference, PresentationCore, PresentationFramework_Classic
from Winstree.DotNet.System.Threading import ApartmentState, Thread, ThreadStart

AddReference(PresentationFramework_Classic)
AddReference(PresentationCore)

import System.Windows


class Application(object):
    def __init__(self):
        self.Class = System.Windows.Application()

    def SetStartup(self, Func):
        self.Class.Startup = Func

    def AddStartup(self, Func):
        self.Class.Startup += Func

    def Run(self):
        self.Class.Run()


class Window(object):
    def __init__(self):
        self.Class = System.Windows.Window()

    def Show(self):
        self.Class.Show()


def MainWindow(MainFunc):
    Threads = Thread(ThreadStart(MainFunc))
    Threads.SetApartmentState(ApartmentState.STA)
    Threads.Start()
    Threads.Join()