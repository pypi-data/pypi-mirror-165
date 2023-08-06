from Winstree import AddReference, System_Windows_Forms

AddReference(System_Windows_Forms)

import System.Windows.Forms


class Application(object):
    def __init__(self):
        self.Class = System.Windows.Forms.Application()

    def ApplicationExit(self, Func):
        self.Class.ApplicationExit += Func

    def Run(self, Window):
        self.Class.Run(Window.Class)

    def Restart(self):
        self.Class.Restart()

    def Exit(self):
        self.Class.Exit()


class CommonDialog(object):
    def __init__(self):
        try:
            self.Class = System.Windows.Forms.CommonDialog()
        except TypeError:
            pass

    def ShowDialog(self):
        self.Class.ShowDialog()


class Control(object):
    from Winstree.DotNet.System.Drawing import FontStyle

    def __init__(self):
        self.Class = System.Windows.Forms.Control()

    def GetClass(self):
        return self.Class

    def SetFontF(self, Value):
        self.Class.Font = Value

    def SetFont(self, Family: str = "Microsoft YaHei UI", Size: int = 9, Style=FontStyle.Regular):
        from src.Winstree.DotNet.System.Drawing import Font
        self.SetFontF(Font(Family, Size, Style))

    def SetPaddingF(self, Value):
        self.Class.Padding = Value

    def SetPadding(self, Bottom, Top, Left, Right):
        self.SetPaddingF(Padding(Bottom, Top, Left, Right))

    def GetPaddingF(self):
        return self.Class.Padding

    def GetPadding(self):
        return PaddingE(self.GetPaddingF())

    def SetMarginF(self, Value):
        self.Class.Margin = Value

    def SetMargin(self, Bottom, Top, Left, Right):
        self.SetMarginF(Padding(Bottom, Top, Left, Right))

    def SetDockF(self, Style):
        self.Class.Dock = Style

    def GetDockF(self):
        return self.Class.Dock

    def GetControls(self):
        return self.Class.Controls

    def Add(self, Widget):
        self.GetControls().Add(Widget.Class)

    def Clear(self):
        self.GetControls().Clear()

    def Remove(self, Widget):
        self.GetControls().Remove(Widget.Class)

    def Show(self):
        self.Class.Show()

    def Hide(self):
        self.Class.Hide()

    def BackColorChanged(self, Func):
        self.Class.BackColorChanged += Func

    def Click(self, Func):
        self.Class.Click += Func

    def ControlAdded(self, Func):
        self.Class.ControlAdded += Func

    def ControlRemoved(self, Func):
        self.Class.ControlRemoved += Func

    def EnabledChanged(self, Func):
        self.Class.EnabledChanged += Func

    def Enter(self, Func):
        self.Class.Enter += Func

    def Move(self, Func):
        self.Class.Move += Func

    def GetBackColorF(self):
        return self.Class.BackColor

    def GetBackColorRGB(self):
        from Winstree.DotNet.System.Drawing import ColorRGBE
        return ColorRGBE(self.GetBackColorF())

    def GetBackColorName(self):
        from Winstree.DotNet.System.Drawing import ColorNameE
        return ColorNameE(self.GetBackColorF())

    def GetCreated(self):
        return self.Class.Created

    def GetEnabled(self):
        return self.Class.Enabled

    def GetForeColorF(self):
        return self.Class.ForeColor

    def GetForeColorRGB(self):
        from Winstree.DotNet.System.Drawing import ColorRGBE
        return ColorRGBE(self.GetForeColorF())

    def GetForeColorName(self):
        from Winstree.DotNet.System.Drawing import ColorNameE
        return ColorNameE(self.GetForeColorF())

    def GetHandle(self):
        return self.Class.Handle

    def GetName(self):
        return self.Class.Name()

    def GetSizeF(self):
        """
        获取窗口大小，将返回System.Drawing.Size
        :return: System.Drawing.Size
        """
        return self.Class.Size

    def GetSize(self):
        """
        获取窗口大小，返回元组 (宽度, 高度)
        :return: 元组
        """
        from Winstree.DotNet.System.Drawing import SizeE
        return SizeE(self.GetSizeF())

    def GetSizeWidth(self):
        """
        获取窗口宽度，返回整数
        :return: 整数
        """
        from Winstree.DotNet.System.Drawing import SizeEWidth
        return SizeEWidth(self.GetSizeF())

    def GetSizeHeight(self):
        """
        获取窗口高度，返回整数
        :return: 整数
        """
        from Winstree.DotNet.System.Drawing import SizeEHeight
        return SizeEHeight(self.GetSizeF())

    def GetLocationF(self):
        return self.Class.Location

    def GetLocation(self):
        from Winstree.DotNet.System.Drawing import PointE
        return PointE(self.GetLocationF())

    def GetLocationX(self):
        from Winstree.DotNet.System.Drawing import PointEX
        return PointEX(self.GetSizeF())

    def GetLocationY(self):
        from Winstree.DotNet.System.Drawing import PointEY
        return PointEY(self.GetSizeF())

    def SetBackColorF(self, Color):
        self.Class.BackColor = Color

    def SetBackColorRGB(self, Red: int, Green: int, Blue: int):
        from Winstree.DotNet.System.Drawing import ColorRGB
        self.Class.BackColor = ColorRGB(Red, Green, Blue)

    def SetBackColorName(self, Name: str):
        from Winstree.DotNet.System.Drawing import ColorName
        self.Class.BackColor = ColorName(Name)

    def SetEnabled(self, Bool: bool):
        self.Class.Enabled = Bool

    def SetForeColorF(self, Color):
        self.Class.ForeColor = Color

    def SetForeColorRGB(self, Red: int, Green: int, Blue: int):
        from Winstree.DotNet.System.Drawing import ColorRGB
        self.Class.ForeColor = ColorRGB(Red, Green, Blue)

    def SetForeColorName(self, Name: str):
        from Winstree.DotNet.System.Drawing import ColorName
        self.Class.ForeColor = ColorName(Name)

    def SetName(self, Strings):
        self.Class.Name = Strings

    def SetSizeF(self, Size):
        """
        设置窗口大小，请使用System.Drawing.Size进行设置。
        :param Size: System.Drawing.Size
        :return:
        """
        self.Class.Size = Size

    def SetSize(self, Width, Height):
        """
        设置窗口大小，直接输入宽度和高度即可
        :param Width: 窗口的宽度
        :param Height: 窗口的高度
        :return:
        """
        from Winstree.DotNet.System.Drawing import Size
        self.SetSizeF(Size(Width, Height))

    def SetSizeWidth(self, Width):
        from Winstree.DotNet.System.Drawing import Size
        self.SetSizeF(Size(Width, self.GetSizeHeight()))

    def SetSizeHeight(self, Height):
        from Winstree.DotNet.System.Drawing import Size
        self.SetSizeF(Size(self.GetSizeWidth(), Height))

    def SetLocationF(self, Point):
        self.Class.Location = Point

    def SetLocation(self, X, Y):
        from Winstree.DotNet.System.Drawing import Point
        self.SetLocationF(Point(X, Y))

    def SetMaximizeBox(self, Bool: bool):
        """
        设置窗口是否有最大化按钮

        :param Bool: False取消最大化按钮，True加入最大化按钮
        :return:
        """
        self.Class.MaximizeBox = Bool

    def SetMinimizeBox(self, Bool: bool):
        """
        设置窗口是否有最小化按钮

        :param Bool: False取消最小化按钮，True加入最小化按钮
        :return:
        """
        self.Class.MinimizeBox = Bool

    def SetMinimumSizeF(self, Size):
        self.Class.MinimumSize = Size

    def SetMinimumSize(self, Width, Height):
        from Winstree.DotNet.System.Drawing import Size
        self.SetMinimumSizeF(Size(Width, Height))

    def SetMinimumSizeWidth(self, Width):
        from Winstree.DotNet.System.Drawing import Size
        self.SetMinimumSizeF(Size(Width, self.GetMinimumSizeHeight()))

    def SetMinimumSizeHeight(self, Height):
        from Winstree.DotNet.System.Drawing import Size
        self.SetMinimumSizeF(Size(self.GetMinimumSizeWidth(), Height))

    def SetMaximumSizeF(self, Size):
        self.Class.MaximumSize = Size

    def SetMaximumSize(self, Width, Height):
        from Winstree.DotNet.System.Drawing import Size
        self.SetMaximumSizeF(Size(Width, Height))

    def SetMaximumSizeWidth(self, Width):
        from Winstree.DotNet.System.Drawing import Size
        self.SetMaximumSizeF(Size(Width, self.GetMaximumSizeHeight()))

    def SetMaximumSizeHeight(self, Height):
        from Winstree.DotNet.System.Drawing import Size
        self.SetMaximumSizeF(Size(self.GetMaximumSizeWidth(), Height))

    def GetMaximumSizeF(self):
        return self.Class.MaximumSize

    def GetMaximumSize(self):
        from Winstree.DotNet.System.Drawing import SizeE
        return SizeE(self.GetMaximumSizeF())

    def GetMaximumSizeWidth(self):
        from Winstree.DotNet.System.Drawing import SizeEWidth
        return SizeEWidth(self.GetMaximumSizeF())

    def GetMaximumSizeHeight(self):
        from Winstree.DotNet.System.Drawing import SizeEHeight
        return SizeEHeight(self.GetMaximumSizeF())

    def GetMaximizeBox(self):
        """
        获取窗口是否有最大化按钮

        :return: 窗口是否有最大化按钮。返回布尔值
        """
        return self.Class.MaximizeBox

    def GetMinimizeBox(self):
        """
        获取窗口是否有最小化按钮

        :return: 窗口是否有最小化按钮。返回布尔值
        """
        return self.Class.MinimizeBox

    def GetMinimumSizeF(self):
        return self.Class.MinimumSize

    def GetMinimumSize(self):
        from Winstree.DotNet.System.Drawing import SizeE
        return SizeE(self.GetMinimumSizeF())

    def GetMinimumSizeWidth(self):
        from Winstree.DotNet.System.Drawing import SizeEWidth
        return SizeEWidth(self.GetMinimumSizeF())

    def GetMinimumSizeHeight(self):
        from Winstree.DotNet.System.Drawing import SizeEHeight
        return SizeEHeight(self.GetMinimumSizeF())

    def SuspendLayout(self):
        self.Class.SuspendLayout()

    def ResumeLayout(self, Bool: bool = None):
        if Bool:
            self.Class.ResumeLayout(Bool)
        else:
            self.Class.ResumeLayout()

    def PerformLayout(self):
        self.Class.PerformLayout()


class ButtonBase(Control):
    def __init__(self):
        super(ButtonBase, self).__init__()
        try:
            self.Class = System.Windows.Forms.ButtonBase()
        except TypeError:
            pass
        from Winstree.DotNet.System.Drawing import ContentAlignment
        self.SetTextAlign(ContentAlignment.MiddleCenter)
        self.SetFont()

    def GetText(self):
        return self.Class.Text

    def GetTextAlign(self):
        return self.Class.TextAlign

    def SetText(self, Strings: str):
        self.Class.Text = Strings

    def SetTextAlign(self, Value: int):
        self.Class.TextAlign = Value


class Button(ButtonBase):
    def __init__(self):
        super(Button, self).__init__()
        self.Class = System.Windows.Forms.Button()
        from Winstree.DotNet.System.Drawing import ContentAlignment
        self.SetTextAlign(ContentAlignment.MiddleCenter)
        self.SetFont()


class CheckBox(ButtonBase):
    def __init__(self):
        super(CheckBox, self).__init__()
        self.Class = System.Windows.Forms.CheckBox()
        from Winstree.DotNet.System.Drawing import ContentAlignment
        self.SetTextAlign(ContentAlignment.MiddleCenter)
        self.SetFont()

    def SetAppearance(self, Value):
        self.Class.Appearance = Value

    def SetAppearanceNormal(self):
        self.SetAppearance(Appearance.Normal)

    def SetAppearanceButton(self):
        self.SetAppearance(Appearance.Button)

    def GetAppearance(self):
        return self.Class.Appearance


class ComboBox(Control):
    def __init__(self):
        super(ComboBox, self).__init__()
        self.Class = System.Windows.Forms.ComboBox()


class Label(Control):
    def __init__(self):
        super(Label, self).__init__()
        self.Class = System.Windows.Forms.Label()
        self.SetFont()

    def GetText(self):
        return self.Class.Text

    def GetTextAlign(self):
        return self.Class.TextAlign

    def SetText(self, Strings: str):
        self.Class.Text = Strings

    def SetTextAlign(self, Value: int):
        self.Class.TextAlign = Value


class FileDialog(CommonDialog):
    def __init__(self):
        super(FileDialog, self).__init__()
        self.Class = System.Windows.Forms.FileDialog()

    def GetInitialDirectory(self):
        return self.Class.InitialDirectory()

    def GetShowHelp(self):
        return self.Class.ShowHelp

    def SetInitialDirectory(self, Path):
        self.Class.InitialDirectory = Path

    def SetShowHelp(self, Bool: bool):
        self.Class.ShowHelp = Bool


class ToolTip(Control):
    def __init__(self):
        super(ToolTip, self).__init__()
        self.Class = System.Windows.Forms.ToolTip()

    def SetUseFading(self, Bool: bool):
        self.Class.UseFading = Bool

    def GetUseFading(self):
        return self.Class.UseFading

    def Draw(self, Func):
        self.Class.Draw += Func

    def Popup(self, Func):
        self.Class.Popup += Func

    def SetToolTipIcon(self, Value):
        self.Class.ToolTipIcon = Value

    def SetIsBalloon(self, Bool: bool):
        self.Class.IsBalloon = Bool

    def GetIsBalloon(self):
        return self.Class.IsBalloon

    def SetAutomaticDelay(self, Int: int):
        self.Class.AutomaticDelay = Int

    def GetAutomaticDelay(self):
        return self.Class.AutomaticDelay

    def SetAutoPopDelay(self, Int: int):
        self.Class.AutoPopDelay = Int

    def GetAutoPopDelay(self):
        return self.Class.AutoPopDelay

    def SetToolTipTitle(self, Strings):
        self.Class.ToolTipTitle = Strings

    def GetToolTipTitle(self):
        return self.Class.ToolTipTitle

    def SetUseAnimation(self, Bool: bool):
        self.Class.UseAnimation = Bool

    def GetUseAnimation(self):
        return self.Class.UseAnimation

    def SetToolTip(self, Widget, Message):
        self.Class.SetToolTip(Widget.Class, Message)

    def GetToolTip(self, Widget):
        return self.Class.GetToolTip(Widget)


class Form(Control):
    def __init__(self, Title: str = "", Size: tuple = (300, 300)):
        super(Form, self).__init__()
        self.Class = System.Windows.Forms.Form()
        self.SetTitle(Title)
        self.SetSize(Size[0], Size[1])

    def LayoutMDI(self, Layout):
        self.Class.LayoutMdi(Layout)

    def SetIsMdiContainer(self, Bool: bool):
        self.Class.IsMdiContainer = Bool

    def GetIsMdiContainer(self):
        return self.Class.IsMdiContainer

    def SetControlBox(self, Bool: bool):
        self.Class.ControlBox = Bool

    def GetControlBox(self):
        return self.Class.ControlBox

    def Activate(self):
        self.Class.Activate()

    def Activated(self, Func):
        self.Class.Activated(Func)

    def Closed(self, Func):
        self.Class.Closed += Func

    def Closing(self, Func):
        self.Class.Closing += Func

    def CenterToParent(self):
        self.Class.CenterToParent()

    def CenterToScreen(self):
        self.Class.CenterToScreen()

    def Close(self):
        self.Class.Close()

    def CreateHandle(self):
        return self.Class.CreateHandle()

    def OnActivated(self, Event):
        self.Class.OnActivated(Event)

    def GetMdiParent(self):
        return self.Class.MdiParent

    def GetModal(self):
        return self.Class.Modal

    def GetOpacity(self):
        return self.Class.Opacity

    def GetShowIcon(self):
        return self.Class.ShowIcon

    def GetShowInTaskbar(self):
        return self.Class.ShowInTaskbar

    def GetClass(self):
        return self.Class

    def GetSizeF(self):
        """
        获取窗口大小，将返回System.Drawing.Size
        :return: System.Drawing.Size
        """
        return self.Class.Size

    def GetSize(self):
        """
        获取窗口大小，返回元组 (宽度, 高度)
        :return: 元组
        """
        from Winstree.DotNet.System.Drawing import SizeE
        return SizeE(self.GetSizeF())

    def GetSizeWidth(self):
        """
        获取窗口宽度，返回整数
        :return: 整数
        """
        from Winstree.DotNet.System.Drawing import SizeEWidth
        return SizeEWidth(self.GetSizeF())

    def GetSizeHeight(self):
        """
        获取窗口高度，返回整数
        :return: 整数
        """
        from Winstree.DotNet.System.Drawing import SizeEHeight
        return SizeEHeight(self.GetSizeF())

    def GetSizeGripStyle(self):
        return self.Class.SizeGripStyle

    def GetStartPosition(self):
        """
        设置窗口初始位置，请使用FormStartPosition的值设置
        :return:
        """
        self.Class.StartPosition = Value

    def GetTitle(self):
        """
        获取窗口的标题

        :return: 窗口的标题。返回字串符
        """
        return self.Class.Text

    def GetTopLevel(self):
        """
        获取窗口是否为顶级窗口
        :return: 窗口是否为顶级窗口。返回布尔值
        """
        return self.Class.TopLevel

    def GetTopMost(self):
        """
        获取窗口是否置顶

        :return: 窗口是否置顶。返回布尔值
        """
        return self.Class.TopMost

    def GetWindowState(self):
        """
        获取窗口状态，对应FormWindowState的值

        :return:
        """
        return self.Class.WindowState

    def SetHelpButton(self, Bool: bool):
        self.Class.HelpButton = Bool

    def SetMdiParent(self, Parent):
        self.Class.MdiParent = Parent.Class

    def SetModal(self, Bool: bool):
        self.Class.Modal = Bool

    def SetOpacity(self, Double: float):
        self.Class.Opacity = Double

    def SetShowIcon(self, Bool: bool):
        self.Class.ShowIcon = Bool

    def SetShowInTaskbar(self, Bool: bool):
        self.Class.ShowInTaskbar = Bool

    def SetSizeF(self, Size):
        """
        设置窗口大小，请使用System.Drawing.Size进行设置。
        :param Size: System.Drawing.Size
        :return:
        """
        self.Class.Size = Size

    def SetSize(self, Width, Height):
        """
        设置窗口大小，直接输入宽度和高度即可
        :param Width: 窗口的宽度
        :param Height: 窗口的高度
        :return:
        """
        from Winstree.DotNet.System.Drawing import Size
        self.SetSizeF(Size(Width, Height))

    def SetSizeWidth(self, Width):
        from Winstree.DotNet.System.Drawing import Size
        self.SetSizeF(Size(Width, self.GetSizeHeight()))

    def SetSizeHeight(self, Height):
        from Winstree.DotNet.System.Drawing import Size
        self.SetSizeF(Size(self.GetSizeWidth(), Height))

    def SetSizeGripStyle(self, Style):
        self.Class.SizeGripStyle = Style

    def SetStartPosition(self, Value):
        """
        设置窗口初始位置，请使用FormStartPosition的值设置
        :param Value:
        :return:
        """
        self.Class.StartPosition = Value

    def SetTitle(self, Strings: str):
        """
        设置窗口的标题

        :param Strings: 窗口标题
        :return:
        """
        self.Class.Text = Strings

    def SetTopLevel(self, Bool: bool):
        """
        设置窗口为顶级窗口
        :param Bool: False不设置为顶级窗口，True设置为顶级窗口。
        :return:
        """
        self.Class.TopLevel = Bool

    def SetTopMost(self, Bool: bool):
        """
        设置窗口是否置顶

        :param Bool: False不置顶窗口，True置顶窗口
        :return:
        """
        self.Class.TopMost = Bool

    def SetWindowState(self, Value: int):
        """
        设置窗口状态，可使用FormWindowState的值设置

        :param Value: 窗口状态，为FormWindowState的数值。
        :return:
        """
        self.Class.WindowState = Value

    def Show(self):
        self.Class.Show()

    def ShowDialog(self):
        self.Class.ShowDialog()


class Window(Form):
    def __init__(self, Title: str = "", Size: tuple = (300, 300)):
        super(Window, self).__init__()
        self.Class = System.Windows.Forms.Form()
        self.SetTitle(Title)
        self.SetSize(Size[0], Size[1])


class FormStartPosition(object):

    Manual = System.Windows.Forms.FormStartPosition.Manual  # 0

    CenterScreen = System.Windows.Forms.FormStartPosition.CenterScreen  # 1

    WindowsDefaultLocation = System.Windows.Forms.FormStartPosition.WindowsDefaultLocation  # 2

    WindowsDefaultBounds = System.Windows.Forms.FormStartPosition.WindowsDefaultBounds  # 3

    CenterParent = System.Windows.Forms.FormStartPosition.CenterParent  # 4


class FormWindowState(object):

    Maximized = System.Windows.Forms.FormWindowState.Maximized

    Minimized = System.Windows.Forms.FormWindowState.Minimized

    Normal = System.Windows.Forms.FormWindowState.Normal


class SizeGripStyle(object):

    Auto = System.Windows.Forms.SizeGripStyle.Auto

    Show = System.Windows.Forms.SizeGripStyle.Show

    Hide = System.Windows.Forms.SizeGripStyle.Hide


class DockStyle(object):
    Bottom = System.Windows.Forms.DockStyle.Bottom
    Fill = System.Windows.Forms.DockStyle.Fill
    Left = System.Windows.Forms.DockStyle.Left
    Right = System.Windows.Forms.DockStyle.Right
    Top = System.Windows.Forms.DockStyle.Top


class ToolTipIcon(object):
    Error = System.Windows.Forms.ToolTipIcon.Error
    Info = System.Windows.Forms.ToolTipIcon.Info
    Warning = System.Windows.Forms.ToolTipIcon.Warning


class Appearance(object):
    Normal = System.Windows.Forms.Appearance.Normal

    Button = System.Windows.Forms.Appearance.Button


class MDILayout(object):
    ArrangeIcons = System.Windows.Forms.MdiLayout.ArrangeIcons

    Cascade = System.Windows.Forms.MdiLayout.Cascade

    TileHorizontal = System.Windows.Forms.MdiLayout.TileHorizontal

    TileVertical = System.Windows.Forms.MdiLayout.TileVertical


def Padding(Bottom: int, Top: int, Left: int, Right: int):
    return System.Windows.Forms.Padding(Left, Top, Right, Bottom)


def PaddingE(Padding):
    return Padding.Bottom, Padding.Top, Padding.Left, Padding.Right
