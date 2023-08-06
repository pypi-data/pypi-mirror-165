from Winstree.DotNet.System.Windows.Forms import *
from Winstree.DotNet.System.Drawing import *


class KApplication(Application):
    def __init__(self):
        super(KApplication, self).__init__()


class KWidget(Control):
    def __init__(self):
        super(KWidget, self).__init__()


class KLabel(Label):
    def __init__(self):
        super(KLabel, self).__init__()


class KButton(Button):
    def __init__(self):
        super(KButton, self).__init__()


class KCheckButton(CheckBox):
    def __init__(self):
        super(KCheckButton, self).__init__()


class KToolTip(ToolTip):
    def __init__(self):
        super(KToolTip, self).__init__()


class KWindow(Form):
    def __init__(self):
        super(KWindow, self).__init__()


class KTypeFormStartPosition(FormStartPosition):
    pass


class KTypeFormWindowState(FormWindowState):
    pass


class KTypeSizeGirpStyle(SizeGripStyle):
    pass


class KTypeDockStyle(DockStyle):
    pass


class KTypeToolTipIcon(ToolTipIcon):
    pass


class KTypeAppearance(Appearance):
    pass


class KTypeMDILayout(MDILayout):
    pass


def KPadding(Bottom: int, Top: int, Left: int, Right: int):
    return Padding(Bottom, Top, Left, Right)


def KPaddingE(Padding):
    return PaddingE(Padding)
