import wx
import stopwatch
import timer
import alarm

class ClockFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='BeBe Clock Tool', size=(700, 300))
        super().SetBackgroundColour(wx.WHITE)
        nb = wx.Notebook(self)
        nb.AddPage(stopwatch.StopWatch(nb), "Stopwatch")
        nb.AddPage(timer.Timer(nb), "Timer")
        nb.AddPage(alarm.Alarm(nb), "Alarm")
        self.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = ClockFrame()
    app.MainLoop()

################### Objectives ###################


# DISPLAY
# list alarms
# show current time
# active and inactive alarms

# PLAY SOUND
# audio signals at certain times
# keep checking for certain time to come
# snooze for 5 minutes

# MANAGE TIME
# display current time

# ALARMS
# create alarm
# edit alarm
# delete alarm
# activate/ deactivate alarm

# DATABASE
# id
# date
# time
# tone location


