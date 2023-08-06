from Winkit import KApplication, KWindow, KLabel, KTypeDockStyle, ContentAlignment, FontStyle


def empty_demo():
    App = KApplication()
    Window = KWindow()
    Window.SetSize(250, 100)
    Window.SetTitle("示例")
    Label = KLabel()
    Label.SetFont("Microsoft YaHei UI", 10, FontStyle.Regular)
    Label.SetTextAlign(ContentAlignment.MiddleCenter)
    Label.SetDockF(KTypeDockStyle.Fill)
    Label.SetText("这只是一个小小的示例程序")
    Window.Add(Label)
    App.Run(Window)


if __name__ == '__main__':
    empty_demo()
