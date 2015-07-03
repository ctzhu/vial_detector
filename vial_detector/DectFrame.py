# -*- coding: utf-8 -*-
#Boa:Frame:DectFrame

import wx
import os
import time
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from vial_detector import *



def create(parent, vid_file):
    if vid_file==None:
        vid_file='Test_data.h264'
    return DectFrame(parent, vid_file)



[wxID_DECTFRAME, wxID_DECTFRAMEBUTTON_BRS, wxID_DECTFRAMEBUTTON_LDVID,
 wxID_DECTFRAMEBUTTON_RUNANA, wxID_DECTFRAMEBUTTON_STRPAR,
 wxID_DECTFRAMEBUTTON_TESTPAR, wxID_DECTFRAMECHECKBOX_FIXSZ,
 wxID_DECTFRAMEPANEL1, wxID_DECTFRAMESTATICTEXT1, wxID_DECTFRAMESTATICTEXT10,
 wxID_DECTFRAMESTATICTEXT11, wxID_DECTFRAMESTATICTEXT12,
 wxID_DECTFRAMESTATICTEXT13, wxID_DECTFRAMESTATICTEXT14,
 wxID_DECTFRAMESTATICTEXT2, wxID_DECTFRAMESTATICTEXT3,
 wxID_DECTFRAMESTATICTEXT4, wxID_DECTFRAMESTATICTEXT5,
 wxID_DECTFRAMESTATICTEXT6, wxID_DECTFRAMESTATICTEXT7,
 wxID_DECTFRAMESTATICTEXT8, wxID_DECTFRAMESTATICTEXT9,
 wxID_DECTFRAMESTATUSBAR1, wxID_DECTFRAMETESTCTRL_HEIGHT,
 wxID_DECTFRAMETESTCTRL_WIDTH, wxID_DECTFRAMETEXTCTRL_ADDARGS,
 wxID_DECTFRAMETEXTCTRL_BCKGR1, wxID_DECTFRAMETEXTCTRL_BCKGR2,
 wxID_DECTFRAMETEXTCTRL_DIAMETER, wxID_DECTFRAMETEXTCTRL_DIM,
 wxID_DECTFRAMETEXTCTRL_FRATE, wxID_DECTFRAMETEXTCTRL_FREARLY,
 wxID_DECTFRAMETEXTCTRL_FRLATER, wxID_DECTFRAMETEXTCTRL_MAXDIA,
 wxID_DECTFRAMETEXTCTRL_MINMASS, wxID_DECTFRAMETEXTCTRL_THLD,
 wxID_DECTFRAMETEXTCTRL_XPOS, wxID_DECTFRAMETEXTCTRL_YPOS,
] = [wx.NewId() for _init_ctrls in range(38)]



class DectFrame(wx.Frame):
    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_DECTFRAME, name='', parent=prnt,
              pos=wx.Point(326, 128), size=wx.Size(843, 759),
              style=wx.DEFAULT_FRAME_STYLE,
              title='Background adjusted particle detection')
        self.SetClientSize(wx.Size(843, 737))

        self.panel1 = wx.Panel(id=wxID_DECTFRAMEPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(855, 231),
              style=wx.TAB_TRAVERSAL)

        self.textCtrl_xpos = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_XPOS,
              name=u'textCtrl_xpos', parent=self.panel1, pos=wx.Point(38, 36),
              size=wx.Size(100, 22), style=0, value=u'0')

        self.textCtrl_ypos = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_YPOS,
              name=u'textCtrl_ypos', parent=self.panel1, pos=wx.Point(38, 72),
              size=wx.Size(100, 22), style=0, value=u'0')

        self.testCtrl_height = wx.TextCtrl(id=wxID_DECTFRAMETESTCTRL_HEIGHT,
              name=u'testCtrl_height', parent=self.panel1, pos=wx.Point(220,
              36), size=wx.Size(100, 22), style=0, value=u'0')

        self.testCtrl_width = wx.TextCtrl(id=wxID_DECTFRAMETESTCTRL_WIDTH,
              name=u'testCtrl_width', parent=self.panel1, pos=wx.Point(220, 72),
              size=wx.Size(100, 22), style=0, value=u'0')

        self.staticText1 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT1,
              label='staticText1', name='staticText1', parent=self.panel1,
              pos=wx.Point(8, 8), size=wx.Size(811, 17), style=0)
        self.staticText1.SetLabelText(u'IMG_FileName')
        self.staticText1.SetBackgroundColour(wx.Colour(241, 241, 241))

        self.checkBox_fixsz = wx.CheckBox(id=wxID_DECTFRAMECHECKBOX_FIXSZ,
              label=u'Fixed ROI Size?', name=u'checkBox_fixsz',
              parent=self.panel1, pos=wx.Point(38, 108), size=wx.Size(250, 18),
              style=0)
        self.checkBox_fixsz.SetLabelText(u'Fixed Region of Interest (ROI) Size?')
        self.checkBox_fixsz.SetValue(False)

        self.staticText2 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT2,
              label=u'x:', name='staticText2', parent=self.panel1,
              pos=wx.Point(8, 38), size=wx.Size(17, 17), style=0)

        self.staticText3 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT3,
              label=u'y:', name='staticText3', parent=self.panel1,
              pos=wx.Point(8, 74), size=wx.Size(15, 17), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT4,
              label=u'Height:', name='staticText4', parent=self.panel1,
              pos=wx.Point(160, 38), size=wx.Size(50, 17), style=0)

        self.staticText5 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT5,
              label=u'Width:', name='staticText5', parent=self.panel1,
              pos=wx.Point(166, 74), size=wx.Size(45, 17), style=0)

        self.staticText6 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT6,
              label=u'Compare Frames:', name='staticText6', parent=self.panel1,
              pos=wx.Point(350, 38), size=wx.Size(115, 17), style=0)

        self.textCtrl_FrEarly = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_FREARLY,
              name=u'textCtrl_FrEarly', parent=self.panel1, pos=wx.Point(480,
              36), size=wx.Size(35, 22), style=0, value=u'1')

        self.textCtrl_FrLater = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_FRLATER,
              name=u'textCtrl_FrLater', parent=self.panel1, pos=wx.Point(520,
              36), size=wx.Size(35, 22), style=0, value=u'100')

        self.staticText7 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT7,
              label=u'Background Frames:', name='staticText7',
              parent=self.panel1, pos=wx.Point(332, 74), size=wx.Size(133, 17),
              style=0)

        self.textCtrl_bckgr1 = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_BCKGR1,
              name=u'textCtrl_bckgr1', parent=self.panel1, pos=wx.Point(480,
              72), size=wx.Size(36, 22), style=0, value=u'1')

        self.textCtrl_bckgr2 = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_BCKGR2,
              name=u'textCtrl_bckgr2', parent=self.panel1, pos=wx.Point(520,
              72), size=wx.Size(36, 22), style=0, value=u'10')

        self.staticText8 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT8,
              label=u'Thershold:', name='staticText8', parent=self.panel1,
              pos=wx.Point(608, 32), size=wx.Size(72, 17), style=0)

        self.staticText9 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT9,
              label=u'MinMass:', name='staticText9', parent=self.panel1,
              pos=wx.Point(608, 56), size=wx.Size(63, 17), style=0)

        self.staticText10 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT10,
              label=u'Diameter:', name='staticText10', parent=self.panel1,
              pos=wx.Point(608, 80), size=wx.Size(66, 17), style=0)

        self.staticText11 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT11,
              label=u'MaxDiameter:', name='staticText11', parent=self.panel1,
              pos=wx.Point(608, 104), size=wx.Size(92, 17), style=0)

        self.textCtrl_thld = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_THLD,
              name=u'textCtrl_thld', parent=self.panel1, pos=wx.Point(720, 30),
              size=wx.Size(100, 22), style=0, value=u'100')

        self.textCtrl_Diameter = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_DIAMETER,
              name=u'textCtrl_Diameter', parent=self.panel1, pos=wx.Point(720,
              78), size=wx.Size(100, 22), style=0, value=u'5')

        self.textCtrl_MinMass = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_MINMASS,
              name=u'textCtrl_MinMass', parent=self.panel1, pos=wx.Point(720,
              54), size=wx.Size(100, 22), style=0, value=u'500')

        self.textCtrl_MaxDia = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_MAXDIA,
              name=u'textCtrl_MaxDia', parent=self.panel1, pos=wx.Point(720,
              102), size=wx.Size(100, 22), style=0, value=u'7')

        self.textCtrl_addArgs = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_ADDARGS,
              name=u'textCtrl_addArgs', parent=self.panel1, pos=wx.Point(165,
              136), size=wx.Size(654, 22), style=0, value=u"{'invert':True}")

        self.staticText12 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT12,
              label=u'Additional Parameters:', name='staticText12',
              parent=self.panel1, pos=wx.Point(8, 136), size=wx.Size(148, 17),
              style=0)

        self.button_testPar = wx.Button(id=wxID_DECTFRAMEBUTTON_TESTPAR,
              label=u'Test Parameters', name=u'button_testPar',
              parent=self.panel1, pos=wx.Point(306, 164), size=wx.Size(140, 20),
              style=0)
        self.button_testPar.Bind(wx.EVT_BUTTON, self.OnButton_testParButton,
              id=wxID_DECTFRAMEBUTTON_TESTPAR)

        self.button_strPar = wx.Button(id=wxID_DECTFRAMEBUTTON_STRPAR,
              label=u'Store Parameters w/o analysis', name=u'button_strPar',
              parent=self.panel1, pos=wx.Point(466, 164), size=wx.Size(210, 20),
              style=0)
        self.button_strPar.Bind(wx.EVT_BUTTON, self.OnButton_strParButton,
              id=wxID_DECTFRAMEBUTTON_STRPAR)

        self.button_runAna = wx.Button(id=wxID_DECTFRAMEBUTTON_RUNANA,
              label=u'Run Analysis', name=u'button_runAna', parent=self.panel1,
              pos=wx.Point(696, 164), size=wx.Size(120, 20), style=0)
        self.button_runAna.Bind(wx.EVT_BUTTON, self.OnButton_runAnaButton,
              id=wxID_DECTFRAMEBUTTON_RUNANA)

        self.statusBar1 = wx.StatusBar(id=wxID_DECTFRAMESTATUSBAR1,
              name='statusBar1', parent=self, style=0)

        self.staticText13 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT13,
              label=u'Video dimension:', name='staticText13',
              parent=self.panel1, pos=wx.Point(8, 200), size=wx.Size(130, 17),
              style=0)

        self.staticText14 = wx.StaticText(id=wxID_DECTFRAMESTATICTEXT14,
              label=u'Video Frame Rate:', name='staticText14',
              parent=self.panel1, pos=wx.Point(400, 200), size=wx.Size(140, 17),
              style=0)

        self.textCtrl_dim = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_DIM,
              name=u'textCtrl_dim', parent=self.panel1, pos=wx.Point(140, 198),
              size=wx.Size(100, 22), style=0, value=u'"default"')

        self.textCtrl_frate = wx.TextCtrl(id=wxID_DECTFRAMETEXTCTRL_FRATE,
              name=u'textCtrl_frate', parent=self.panel1, pos=wx.Point(550,
              198), size=wx.Size(100, 22), style=0, value=u'"default"')

        self.button_ldvid = wx.Button(id=wxID_DECTFRAMEBUTTON_LDVID,
              label=u'Load Video', name=u'button_ldvid', parent=self.panel1,
              pos=wx.Point(126, 164), size=wx.Size(120, 20), style=0)
        self.button_ldvid.Bind(wx.EVT_BUTTON, self.OnButton_ldvidButton,
              id=wxID_DECTFRAMEBUTTON_LDVID)

        self.button_Brs = wx.Button(id=wxID_DECTFRAMEBUTTON_BRS,
              label=u'Browse...', name=u'button_Brs', parent=self.panel1,
              pos=wx.Point(24, 164), size=wx.Size(82, 20), style=0)
        self.button_Brs.Bind(wx.EVT_BUTTON, self.OnButton_BrsButton,
              id=wxID_DECTFRAMEBUTTON_BRS)

        self._init_sizers()

    def __init__(self, parent, vid_file):
        self._init_ctrls(parent)
        ##self.SetAutoLayout(True)
        self.boxSizer1.Add(self.panel1, 0, wx.EXPAND)
        ##self.figure, self.axes = plt.subplots(nrows=1, ncols=2)
        ##Doing it this way may cause hangup. why???
        self.button_strPar.Enable(False)
        self.button_runAna.Enable(False)

        #Plot canvas init
        self.figure = Figure()
        #self.axes   = [self.figure.add_subplot(111), ]
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.boxSizer1.Add(self.canvas, 1, wx.EXPAND)
        ##self.Fit()
        self.vid_file = vid_file
        self.vid_path, self.vid_fname = os.path.split(self.vid_file)
        self.vid_noext = os.path.join(self.vid_path,
                                      '.'.join(self.vid_fname.split('.')[:-1]))
        self.staticText1.SetLabelText(self.vid_file)

        #ROI selection init
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None

        #self.rect = Rectangle((0,0), 1, 1, fill=False, ec='r')
        #self.axes[0].add_patch(self.rect)

        #StatusBar and ProgressBar init
        self.boxSizer1.Add(self.statusBar1, 0, border=0, flag=0)
        #Some how if set postion to 2 make it look strange
        #self.statusBar1.SetStatusText('Ready', 0)
        self.progress_bar = wx.Gauge(self.statusBar1, 0, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        rect = self.statusBar1.GetFieldRect(0)
        self.progress_bar.SetPosition((rect.x+1, rect.y+1))
        self.progress_bar.SetSize((rect.width-10, rect.height-2))
        #need to set the position manually
        self.progress_bar.SetRange(50)
        self.progress_bar.SetValue(0)
        self.progress_bar.Hide()
        #Hide it when not in use

        #store a property of whether the mouse key is pressed
        self.pressed = False
        
        #all the controls of parameters:
        self.pars_ctrls = [self.textCtrl_xpos,
                           self.textCtrl_ypos,
                           self.testCtrl_height,
                           self.testCtrl_width,
                           self.textCtrl_FrEarly,
                           self.textCtrl_FrLater,
                           self.textCtrl_bckgr1,
                           self.textCtrl_bckgr2,
                           self.textCtrl_thld,
                           self.textCtrl_Diameter,
                           self.textCtrl_MinMass,
                           self.textCtrl_MaxDia,
                           self.textCtrl_addArgs,
                           self.textCtrl_dim,
                           self.textCtrl_frate]




    def ChangeCursor(self, event):
        '''Change cursor into crosshair type when enter the plot area'''
        self.canvas.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))



    def on_press(self, event):
        '''Draw ROI rectangle'''
        self.pressed = True
        if self.checkBox_fixsz.Enabled:
            try:
                self.x0 = int(event.xdata)
                self.y0 = int(event.ydata)
                if self.checkBox_fixsz.GetValue():
                    self.x1 = self.x0 + int(eval(self.testCtrl_width.GetValue()))
                    self.y1 = self.y0 + int(eval(self.testCtrl_height.GetValue()))
                    self.rect.set_width(self.x1 - self.x0)
                    self.rect.set_height(self.y1 - self.y0)
                    self.rect.set_xy((self.x0, self.y0))
                    self.canvas.draw()
                self.textCtrl_xpos.SetValue(str(self.x0))
                self.textCtrl_ypos.SetValue(str(self.y0))
                self.testCtrl_height.SetValue(str(self.rect.get_height()))
                self.testCtrl_width.SetValue(str(self.rect.get_width()))
            except:
                pass



    def on_release(self, event):
        '''When mouse is on plot and button is released, redraw ROI rectangle, update ROI values'''
        self.pressed = False
        if self.checkBox_fixsz.Enabled:
            if self.checkBox_fixsz.GetValue():
                pass
            else:
                self.redraw_rect(event)
            self.update_ROIdisp()



    def on_motion(self, event):
        '''If the mouse is on plot and if the mouse button is pressed, redraw ROI rectangle'''
        if self.pressed & self.checkBox_fixsz.Enabled & (not self.checkBox_fixsz.GetValue()):
            # redraw the rect
            self.redraw_rect(event)
            self.update_ROIdisp()



    def redraw_rect(self, event):
        '''Draw the ROI rectangle overlay'''
        try:
            self.x1 = int(event.xdata)
            self.y1 = int(event.ydata)
            self.rect.set_xy((self.x0, self.y0))
            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
        except:
            pass
        self.canvas.draw()



    def update_ROIdisp(self):
        '''Update ROI display in UI'''
        self.textCtrl_xpos.SetValue(str(self.x0))
        self.textCtrl_ypos.SetValue(str(self.y0))
        self.testCtrl_height.SetValue(str(self.y1 - self.y0))
        self.testCtrl_width.SetValue(str(self.x1 - self.x0))



    def OnButton_runAnaButton(self, event):
        '''Analysis the whole video, output the result pandas.dataframe and analysis config file
        in the same folder (as the video file).
        Plot diagnostic plots.
        '''
        #maybe plot the result?
        ROIx1, ROIy1 = self.rect.get_xy()
        ROIx2        = ROIx1 + self.rect.get_width()
        ROIy2        = ROIy1 + self.rect.get_height()

        earlyF, laterF, startF, endF, thld, diameter, minmass, maxsize, addpar = self.pars[4:-2]

        ##plot ROI
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.imshow(self.detector.img_stack[0])
        ax.vlines([ROIx1, ROIx2], ROIy1, ROIy2, 'r')
        ax.hlines([ROIy1, ROIy2], ROIx1, ROIx2, 'r')
        ax.set_title(self.vid_file, fontsize=10)
        self.figure.savefig(self.vid_noext+'_ovv.png')

        ##Detector Workflow and Progress bar update
        self.detector.set_ROI([ROIx1, ROIx2], [ROIy1, ROIy2])
        self.detector.set_backgrd((startF, endF))
        self.progress_bar.Show()
        wx.BeginBusyCursor()
        F=lambda x, y: (self.progress_bar.SetRange(y),
                        self.progress_bar.SetValue(x))
        try:
            P_dfs = self.detector.bckgrd_pdetect(thld=thld,
                                                 minmass=minmass,
                                                 diameter=diameter,
                                                 maxsize=maxsize,
                                                 progress_barF=F,
                                                 Print = False,
                                                 **addpar)
        finally:
            wx.EndBusyCursor()

        ##Result presentation
        self.figure.clear()
        [ax1, ax3, ax2, ax4] = map(self.figure.add_subplot, [221, 222, 223, 224])
        self.detector.diagnostic_plot(earlyF, ax=ax1)
        self.detector.diagnostic_plot(laterF, ax=ax2)
        ax1.set_title('Frame #%s'%earlyF)
        ax2.set_title('Frame #%s'%laterF)
        big_df = pd.concat(P_dfs)
        big_df_clean = big_df[big_df.True_particle]
        gby_obj = big_df_clean.groupby('Timestamp')
        ax3.plot(gby_obj.count().index,
                 -gby_obj.mean().y + big_df_clean.y.max())
        ax3.set_title('Mean vertical displacement')
        ax3.set_ylabel('pixel')
        ax4.plot(gby_obj.count().index,
                 gby_obj.count().x)
        ax4.set_title('No. of flies detected')
        ax4.set_ylabel('Count')
        ax4.set_xlabel('Time (S)')
        self.figure.suptitle(self.vid_file)
        self.figure.savefig(self.vid_noext+'_dig.png')
        self.figure.canvas.draw()

        ##save dfs
        big_df.to_csv(self.vid_noext+'.csv', index=None)
        ##also need to save the pararmeters
        self.save_parameter()
        F(0, 100)
        self.progress_bar.Hide()
        #event.Skip()



    def OnButton_testParButton(self, event):
        '''plot the decection result and compare two frames, an early and a late Frame
        So the parameter can be fine tuned.'''
        #Prep the parameters
        for item in self.pars_ctrls[:4]:
            item.SetEditable(False)
            item.Enable(False)
        self.checkBox_fixsz.Enable(False)
        self.pars = [eval(item.GetValue()) for item in self.pars_ctrls]

        #Do the plotting
        self.figure.clear()
        self.axes = [self.figure.add_subplot(121),
                     self.figure.add_subplot(122)]
        wx.BeginBusyCursor()
        try:
            self.detector.plot_partest(self.pars[:-2], self.axes)
        finally:
            wx.EndBusyCursor()
        self.figure.canvas.draw()

        #Once the ROI is defined, disable further changes
        self.button_strPar.Enable(True)
        self.button_runAna.Enable(True)
        #event.Skip()



    def OnButton_strParButton(self, event):
        #save the analysis parameters
        self.save_parameter()
        #event.Skip()



    def save_parameter(self):
        '''Save parameters as python list.
        New parameter sets appended to the config file.
        Each parameter sets come with a comment line, contain the datetime of analysis'''
        with open(self.vid_noext+'.cfg', 'a') as f:
            print>>f, '#Aanlysis Parameters: '+time.ctime()
            print>>f, self.pars



    def OnButton_ldvidButton(self, event):
        #Load the video, set Cursor to be busy
        self.figure.clear()
        self.axes   = [self.figure.add_subplot(111), ]
        #self.axes[0].add_patch(self.rect)
        for item in self.pars_ctrls[:4]:
            item.SetEditable(True)
            item.Enable(True)
        self.checkBox_fixsz.Enable(True)
        wx.BeginBusyCursor()
        try:
            self.detector = detector(self.vid_file,
                                    resolution=eval(self.textCtrl_dim.GetValue()),
                                    frame_rate=eval(self.textCtrl_frate.GetValue()))
            self.axes[0].imshow(self.detector.img_stack[0])
            self.figure.canvas.draw()
        finally:
            wx.EndBusyCursor()
        #self.canvas = FigureCanvas(self, -1, self.figure)
        self.canvas.Bind(wx.EVT_ENTER_WINDOW, self.ChangeCursor)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.rect = Rectangle((0,0), 1, 1, fill=False, ec='r')
        self.axes[0].add_patch(self.rect)
        #event.Skip()



    def OnButton_BrsButton(self, event):
        openFileDialog = wx.FileDialog(self, "Open Video file", "", "",
                                       "Video files (*.*)|*.*", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        try:
            openFileDialog.SetDirectory(self.vid_path)
        except:
            pass
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
        	pass
        else:
            self.vid_file = openFileDialog.GetPath()
            self.vid_path, self.vid_fname = os.path.split(self.vid_file)
            self.vid_noext = os.path.join(self.vid_path,
                                          '.'.join(self.vid_fname.split('.')[:-1]))
            self.staticText1.SetLabelText(self.vid_file)
            self.OnButton_ldvidButton(event)
        #event.Skip()
