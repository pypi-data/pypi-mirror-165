from Winstree import AddReference, System_Windows_Forms

AddReference(System_Windows_Forms)

import System.Drawing


def ColorRGB(Red: int, Green: int, Blue: int):
    return System.Drawing.Color.FromArgb(Red, Green, Blue)


def ColorARGB(Alpha: int, Red: int, Green: int, Blue: int):
    return System.Drawing.Color.FromArgb(Alpha, ColorRGB(Red, Green, Blue))


def ColorRGBE(ColorRGB):
    return ColorRGB.ToArgb()


def ColorNameE(ColorName):
    return ColorName.ToString()


def ColorName(Name: str):
    return System.Drawing.Color.FromName(Name)


def Size(Width: int, Height: int):
    return System.Drawing.Size(Width, Height)


def SizeE(Size: Size):
    return Size.Width, Size.Height


def SizeEWidth(Size: Size):
    return Size.Width


def SizeEHeight(Size: Size):
    return Size.Height


def Point(X: int, Y: int):
    return System.Drawing.Point(X, Y)


def PointE(Point: Point):
    return Point.X, Point.Y


def PointEX(Point):
    return Point.X


def PointEY(Point):
    return Point.Y


class FontStyle(object):
    Regular = System.Drawing.FontStyle.Regular

    Bold = System.Drawing.FontStyle.Bold

    Italic = System.Drawing.FontStyle.Italic

    Underline = System.Drawing.FontStyle.Underline

    Strikeout = System.Drawing.FontStyle.Strikeout


def Font(Family: str = "Microsoft YaHei UI", Size: int = 9, Style=FontStyle.Regular):
    return System.Drawing.Font(Family, Size, Style)


class ContentAlignment(object):
    BottomCenter = System.Drawing.ContentAlignment.BottomCenter

    BottomLeft = System.Drawing.ContentAlignment.BottomLeft

    BottomRight = System.Drawing.ContentAlignment.BottomRight

    MiddleCenter = System.Drawing.ContentAlignment.MiddleCenter

    MiddleLeft = System.Drawing.ContentAlignment.MiddleLeft

    MiddleRight = System.Drawing.ContentAlignment.MiddleRight

    TopCenter = System.Drawing.ContentAlignment.TopCenter

    TopLeft = System.Drawing.ContentAlignment.TopLeft

    TopRight = System.Drawing.ContentAlignment.TopRight
