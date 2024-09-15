import wx
import wx.adv
import global_var 


class MyCalendar(wx.Frame):

    def __init__(self, args, *kargs,):
        wx.Frame.__init__(self, args, *kargs,size =(250,240),style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        # wx.Frame.__init__(self, args, *kargs ,size =(470,240),style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX) # Frame Size for twotenders calander
        self.panel = wx.Panel(self,size=(120, 120), pos=(0, 0), style=wx.SUNKEN_BORDER)

        self.cal = wx.adv.CalendarCtrl(self.panel, 10, wx.DateTime.Now(),pos = (0,0))
        self.cal.Bind(wx.adv.EVT_CALENDAR, self.fromdate)

        # self.cal1 = wx.adv.CalendarCtrl(self.panel, 10, wx.DateTime.Now(),pos = (240,0))
        # self.cal1.Bind(wx.adv.EVT_CALENDAR, self.To_Date)

        self.Get_date = wx.Button(self.panel, label="From Date", pos=(50,155),size = (120,30),style=wx.NO_BORDER)
        font = wx.Font(15, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.Get_date.SetFont(font)
        self.Get_date.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.Get_date.Bind(wx.EVT_BUTTON, self.fromdate)
        # self.Get_date.SetForegroundColour('Black')
        # self.Get_date.SetBackgroundColour('#d7d7d7')



        # self.Get_date2 = wx.Button(self.panel, label="To Date", pos=(300,155),size = (120,30),style=wx.NO_BORDER) # Second Calender button
        # font = wx.Font(15, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        # self.Get_date2.SetFont(font)
        # self.Get_date2.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        # self.Get_date2.Bind(wx.EVT_BUTTON, self.To_Date)
        # self.Get_date2.SetForegroundColour('Black')
        # self.Get_date2.SetBackgroundColour('#d7d7d7')

        
    def fromdate(self,event):
        select = self.cal.GetDate()
        fromdate = select.Format('%d/%m/%Y')
        global_var.fromdate = str(fromdate).strip()
        print(fromdate)
        if global_var.fromdate == '':
            print('Please Select From Date ')
        else:
            self.Destroy()
        
    # def To_Date(self,event):
    #     select = self.cal1.GetDate()
    #     To_Date = select.Format('%d/%m/%Y')
    #     global_var.To_Date = str(To_Date).strip()
    #     print(To_Date)

    #     if global_var.fromdate == '':
    #         print('Please Select TO Date ')
    #     elif global_var.To_Date == '':
    #         print('Please Select From Date ')
    #     else:
    #         self.Destroy()
        

if __name__ == '__main__':
    app = wx.App()
    frame = MyCalendar(None)
    frame.Show()
    app.MainLoop()

import COLLECT_LINK






