import wx
from vial_detector import DectFrame
import sys


class App(wx.App):
    def OnInit(self):
        'Create the main window and insert the custom frame'
        frame = DectFrame.create(None, filename)
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__=='__main__':
    if len(sys.argv)>1:
    	filename = sys.argv[-1]
    else:
    	filename = None
    app = App(0)
    app.MainLoop()
