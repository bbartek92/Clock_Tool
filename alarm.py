import wx
import database_connector as db
from data_class import Record
from mapping import id, name, time_, repeats
import time
import pygame

class Alarm(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        super().SetBackgroundColour(wx.Colour(230, 230, 230))
        self.init_sizers()
        self.choices = []
        self.selected = []
        self.check_list = wx.CheckListBox(self,
                                     size=(350, 300), choices=self.choices,
                                     name="Alarm list")
        self.check_list.Bind(wx.EVT_CHECKLISTBOX, self.on_check)
        self.parse_choice_list()
        self.update_list()
        self.left_sizer.Add(self.check_list, 0, wx.ALL, 5)
        # Right sizer part
        lap_button = self.set_button('Add', (153, 204, 77), self.on_add)
        self.right_sub_sizer.Add(lap_button, 0, wx.ALL, 5)
        stop_button = self.set_button('Edit', (77, 153, 255), self.on_edit)
        self.right_sub_sizer.Add(stop_button, 0, wx.ALL, 5)
        reset_button = self.set_button('Delete', (204, 0, 0), self.on_delete)
        self.right_sub_sizer.Add(reset_button, 0, wx.ALL, 5)
        pygame.mixer.init()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.check_time, self.timer)
        self.timer.Start(60000)

    def check_time(self, event):
        current_list = []
        for item in self.alarms:
            current_list.append(item.time)
        if time.strftime('%H:%M') in current_list:
            if not pygame.mixer.music.get_busy():
                self.play_alarm()
                wx.MessageBox(f"It's {time.strftime('%H:%M')} !!!", "Alarm!",
                              wx.OK | wx.ICON_INFORMATION)

    def play_alarm(self):
        mp3 = 'alarm.mp3'
        pygame.mixer.music.load(mp3)
        pygame.mixer.music.play()

    def init_sizers(self):
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sub_sizer = wx.BoxSizer(wx.VERTICAL)
        sep_line = wx.StaticLine(self, style=wx.LI_VERTICAL)
        right_sizer.Add(self.right_sub_sizer, 0, wx.ALL, 0)
        main_sizer.Add(self.left_sizer, 0, wx.ALL, 0)
        main_sizer.Add(sep_line, 0, wx.ALL | wx.EXPAND, 0)
        main_sizer.Add(right_sizer, 0, wx.ALL, 0)
        self.SetSizer(main_sizer)

    def set_button(self, label, color, evt_function):
        bt_name = wx.Button(self, label=label)
        bt_name.SetBackgroundColour(wx.Colour(*color))
        bt_name.Bind(wx.EVT_BUTTON, evt_function)
        return bt_name

    def get_alarms_list(self):
        datahendler = db.DataHandler()
        data = datahendler.read_data()
        alarms_list = []
        for row in data:
            alarm = Record(id=row[id],
                                 time=row[time_],
                                 name=row[name],
                                 repeats=row[repeats])
            alarms_list.append(alarm)
        return alarms_list

    def parse_choice_list(self):
        self.alarms = self.get_alarms_list()
        self.choices = []
        for alarm in self.alarms:
            display = f"{alarm.time} - {alarm.name}"
            self.choices.append(display)

    def update_list(self):
        self.check_list.Clear()
        self.check_list.Append(self.choices)

    def on_check(self, event):
        pass

    def on_add(self, event):
        self._get_input('Add new Alarm')
        datahandler = db.DataHandler()
        datahandler.write_data(self.modal.alarm_name,
                               self.modal.alarm_hour, self.modal.alarm_minutes)
        self.parse_choice_list()
        self.update_list()

    def _get_input(self, title):
        self.modal = Modal(self, title)
        val = self.modal.ShowModal()
        if val == wx.ID_OK:
            if len(self.modal.alarm_hour) == 1:
                self.modal.alarm_hour = '0' + self.modal.alarm_hour
            if len(self.modal.alarm_minutes) == 1:
                self.modal.alarm_minutes = '0' + self.modal.alarm_minutes
        else:
            print('cancel')

    def on_edit(self, event):
        items = self.check_list.GetCheckedItems()
        datahandler = db.DataHandler()
        for item in items:
            current_name = self.alarms[item].name
            title = f'Edit {current_name} Alarm'
            self._get_input(title)
            datahandler.edit_data(self.alarms[item].id, self.modal.alarm_name, self.modal.alarm_hour, self.modal.alarm_minutes)
        self.parse_choice_list()
        self.update_list()

    def on_delete(self, event):
        items = self.check_list.GetCheckedItems()
        datahandler = db.DataHandler()
        for item in items:
            datahandler.delete_data(self.alarms[item].id)
        self.parse_choice_list()
        self.update_list()

class Modal(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        modal_sizer = wx.BoxSizer(wx.VERTICAL)
        first_sizer = wx.BoxSizer(wx.HORIZONTAL)
        second_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, label=' Set Alarm Hour and Minutes', size=(200, 30))
        modal_sizer.Add(self.text, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.spin_1 = self.set_spin_bt((60, 20), 0, 23, self.on_hours)
        first_sizer.Add(self.spin_1, 0, wx.ALL, 5)
        self.spin_2 = self.set_spin_bt((60, 20), 0, 59, self.on_minutes)
        first_sizer.Add(self.spin_2, 0, wx.ALL, 5)
        self.text = wx.StaticText(self, label='Set Alarm name', size=(200, 30))
        second_sizer.Add(self.text, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.input = wx.TextCtrl(self, size=(200, 30))
        self.input.Bind(wx.EVT_TEXT, self.on_typed)
        second_sizer.Add(self.input, 0, wx.ALL, 5)
        modal_sizer.Add(first_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        modal_sizer.Add(second_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        modal_sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.SetSizer(modal_sizer)
        self.alarm_hour = ''
        self.alarm_minutes = ''
        self.alarm_name = ''

    def set_spin_bt(self, size, min, max, function):
        spin = wx.SpinCtrl(self, size=size, min=min, max=max)
        spin.Bind(wx.EVT_SPINCTRL, function)
        return spin

    def on_hours(self, event):
        self.alarm_hour = str(self.spin_1.GetValue())

    def on_minutes(self, event):
        self.alarm_minutes = str(self.spin_2.GetValue())

    def on_typed(self, event):
        self.alarm_name = str(self.input.GetValue())