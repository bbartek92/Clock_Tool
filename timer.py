import wx

class Timer(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        super().SetBackgroundColour(wx.Colour(230, 230, 230))
        self.init_sizers()
        self.set_variables()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.spin_1 = self.set_spin_bt((60, 20), 0, 60, self.on_hours)
        self.left_sizer.Add(self.spin_1, 10, wx.ALL, 5)
        self.spin_2 = self.set_spin_bt((60, 20), 0, 59, self.on_minutes)
        self.left_sizer.Add(self.spin_2, 0, wx.ALL, 5)
        self.spin_3 = self.set_spin_bt((60, 20), 0, 59, self.on_seconds)
        self.left_sizer.Add(self.spin_3, 0, wx.ALL, 5)
        self.spin_1_val = 0
        self.spin_2_val = 0
        self.spin_3_val = 0
        lap_button = self.set_button('Pause', (242, 242, 242), self.on_pause)
        self.right_sub_sizer.Add(lap_button, 0, wx.ALL, 5)
        stop_button = self.set_button('Start', (77, 153, 255), self.on_start)
        self.right_sub_sizer.Add(stop_button, 0, wx.ALL, 5)
        reset_button = self.set_button('Reset', (242, 242, 242), self.on_reset)
        self.right_sub_sizer.Add(reset_button, 0, wx.ALL, 5)

    def set_variables(self):
        self.running = None

    def set_button(self, label, color, evt_function):
        bt_name = wx.Button(self, label=label)
        bt_name.SetBackgroundColour(wx.Colour(*color))
        bt_name.Bind(wx.EVT_BUTTON, evt_function)
        return bt_name

    def init_sizers(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sep_line = wx.StaticLine(self, style=wx.LI_VERTICAL)
        right_sizer.Add(self.right_sub_sizer, 0, wx.ALL, 0)
        main_sizer.Add(self.left_sizer, 0, wx.ALL, 0)
        main_sizer.Add(sep_line, 0, wx.ALL | wx.EXPAND, 0)
        main_sizer.Add(right_sizer, 0, wx.ALL, 0)
        self.SetSizer(main_sizer)

    def set_spin_bt(self, size, min, max, function):
        spin = wx.SpinCtrl(self, size=size, min=min, max=max)
        spin.Bind(wx.EVT_SPINCTRL, function)
        return spin

    def on_hours(self, event):
        self.spin_1_val = self.spin_1.GetValue()

    def on_minutes(self, event):
        self.spin_2_val = self.spin_2.GetValue()

    def on_seconds(self, event):
        self.spin_3_val = self.spin_3.GetValue()

    def update(self, event):
        if self.running:
            if self.spin_1_val == 0 and self.spin_2_val == 0 and self.spin_3_val == 0:
                self.running = False
                self.timer.Stop()
            else:
                if self.spin_3_val > 0:
                    self.spin_3_val -= 1
                    self.spin_3.SetValue(self.spin_3_val)
                else:
                    self.spin_3_val = 59
                    self.spin_3.SetValue(self.spin_3_val)
                    if self.spin_2_val > 0:
                        self.spin_2_val -= 1
                        self.spin_2.SetValue(self.spin_2_val)
                    else:
                        self.spin_2_val = 59
                        self.spin_2.SetValue(self.spin_2_val)
                        if self.spin_1_val > 0:
                            self.spin_1_val -= 1
                            self.spin_1.SetValue(self.spin_1_val)
                        else:
                            self.running = False
                            self.timer.Stop()

    def on_pause(self, event):
        self.running = False
        self.timer.Stop()

    def on_start(self, event):
        self.running = True
        self.timer.Start(1000)

    def on_reset(self, event):
        self.spin_1_val = 0
        self.spin_2_val = 0
        self.spin_3_val = 0
        self.spin_1.SetValue(0)
        self.spin_2.SetValue(0)
        self.spin_3.SetValue(0)
        self.timer.Stop()