import wx
from datetime import timedelta

class StopWatch(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        super().SetBackgroundColour(wx.Colour(230, 230, 230))
        self.init_sizers()
        self.timer = wx.Timer(self)
        self.sw = wx.StopWatch()
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.init_variables()
        self.stopwatch_label_1 = wx.StaticText(self, label="0:00:00.0",
                                               size=(200, 40))
        self.stopwatch_label_1.SetForegroundColour(wx.BLACK)
        font_1 = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_NORMAL)
        self.stopwatch_label_1.SetFont(font_1)
        self.left_sizer.Add(self.stopwatch_label_1, 0, wx.ALL | wx.CENTER, 5)
        self.stopwatch_label_2 = wx.StaticText(self, label="0:00:00.0",
                                               size=(200, 40))
        self.stopwatch_label_2.SetForegroundColour(wx.Colour(77, 153, 255))
        font_2 = wx.Font(22, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_NORMAL)
        self.stopwatch_label_2.SetFont(font_2)
        self.left_sizer.Add(self.stopwatch_label_2, 0, wx.ALL | wx.CENTER, 5)
        self.set_list_ctrl()
        self.left_sizer.Add(self.lap_list_ctrl, 0, wx.ALL, 5)
        # Right sizer part
        lap_button = self.set_button('Lap', (242, 242, 242), self.on_lap)
        self.right_sub_sizer.Add(lap_button, 0, wx.ALL, 5)
        self.start_stop_button = self.set_button('Start', (77, 153, 255), self.on_start_stop)
        self.right_sub_sizer.Add(self.start_stop_button, 0, wx.ALL, 5)
        reset_button = self.set_button('Reset', (242, 242, 242), self.on_reset)
        self.right_sub_sizer.Add(reset_button, 0, wx.ALL, 5)
        show_lap = wx.CheckBox(self, label="Show lap time")
        show_lap.SetValue(True)
        show_lap.Bind(wx.EVT_CHECKBOX, self.on_show_lap)
        self.right_sizer.Add(show_lap, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)

    def init_variables(self):
        self.running = None
        self.list_visible = True
        self.current_lap = 0
        self.laps = []
        self.lap_count = 0

    def init_sizers(self):
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sep_line = wx.StaticLine(self, style=wx.LI_VERTICAL)
        self.main_sizer.Add(self.left_sizer, 0, wx.ALL, 0)
        self.main_sizer.Add(sep_line, 0, wx.ALL | wx.EXPAND, 0)
        self.right_sizer.Add(self.right_sub_sizer, 0, wx.ALL, 0)
        self.main_sizer.Add(self.right_sizer, 0, wx.ALL, 0)
        self.SetSizer(self.main_sizer)

    def set_list_ctrl(self):
        self.lap_list_ctrl = wx.ListCtrl(self, size=(-1, 120),
                                         style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.lap_list_ctrl.InsertColumn(0, 'Lap', width=180)
        self.lap_list_ctrl.InsertColumn(1, 'Time', width=180)

    def set_button(self, label, color, evt_function):
        bt_name = wx.Button(self, label=label)
        bt_name.SetBackgroundColour(wx.Colour(*color))
        bt_name.Bind(wx.EVT_BUTTON, evt_function)
        return bt_name

    def on_lap(self, event):
        if self.running == True:
            self.lap_count += 1
            if self.laps:
                time = self.current_lap
            else:
                time = timedelta(microseconds=self.sw.TimeInMicro())
            lap = [[f"Lap {self.lap_count}"],[f"{time}"], [time]]
            self.laps.append(lap)

            self.clean_list()
            index = 0
            for line in self.laps:
                self.lap_list_ctrl.InsertItem(index, line[0][0])
                self.lap_list_ctrl.SetItem(index, 1, line[1][0])
                index += 1

    def on_start_stop(self, event):
        if  self.start_stop_button.GetLabel() == 'Start':
            self.start_stop_button.SetLabel('Stop')
            if self.running == True:
                self.timer.Start(10)
                self.sw.Resume()
                self.running = True
            else:
                self.timer.Start(10)
                self.sw.Start()
                self.running = True
        else:
            self.start_stop_button.SetLabel('Start')
            self.timer.Stop()
            self.sw.Pause()

    def update(self, event):
        self.stopwatch_label_1.SetLabel(str(timedelta(microseconds=self.sw.TimeInMicro())))
        if self.laps:
            total_time = timedelta(microseconds=0)
            for line in self.laps:
                total_time += line[2][0]

            self.stopwatch_label_2.SetLabel(str(timedelta(microseconds=self.sw.TimeInMicro())-total_time))
            self.current_lap = timedelta(microseconds=self.sw.TimeInMicro())-total_time

    def on_reset(self, event):
        self.running = False
        self.stopwatch_label_1.SetLabel("0:00:00.0")
        self.stopwatch_label_2.SetLabel("0:00:00.0")
        self.timer.Stop()
        self.sw.Pause()
        self.start_stop_button.SetLabel('Start')
        self.laps = []

        self.clean_list()

    def on_show_lap(self, event):
        if self.list_visible == True:
            self.list_visible = False
            self.lap_list_ctrl.Hide()
        else:
            self.list_visible = True
            self.lap_list_ctrl.Show()

    def clean_list(self):
        self.lap_list_ctrl.ClearAll()
        self.lap_list_ctrl.InsertColumn(0, 'Lap', width=180)
        self.lap_list_ctrl.InsertColumn(1, 'Time', width=180)