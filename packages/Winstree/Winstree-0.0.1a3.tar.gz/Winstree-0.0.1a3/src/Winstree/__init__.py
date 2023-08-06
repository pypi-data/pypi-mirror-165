import clr

System_Windows_Forms = "System.Windows.Forms"

System_Windows = "System.Windows"

Microsoft_UI_Xaml = "Microsoft.UI.Xaml"

PresentationFramework_Classic = \
    "PresentationFramework.Classic, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"

PresentationCore = \
    "PresentationCore, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"


def AddReference(Lib: str):
    clr.AddReference(Lib)
