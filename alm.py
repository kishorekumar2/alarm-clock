import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import time
import datetime
import threading
import pygame

# Initialize pygame mixer for playing sound
pygame.mixer.init()

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")

        self.alarms = []

        self.time_label = tk.Label(root, font=('calibri', 40, 'bold'))
        self.time_label.pack(anchor='center')

        self.set_alarm_frame = tk.Frame(root)
        self.set_alarm_frame.pack(anchor='center')

        self.hour_entry = tk.Entry(self.set_alarm_frame, width=5, font=('calibri', 20, 'bold'))
        self.hour_entry.insert(0, "HH")
        self.hour_entry.pack(side=tk.LEFT)

        self.minute_entry = tk.Entry(self.set_alarm_frame, width=5, font=('calibri', 20, 'bold'))
        self.minute_entry.insert(0, "MM")
        self.minute_entry.pack(side=tk.LEFT)

        self.second_entry = tk.Entry(self.set_alarm_frame, width=5, font=('calibri', 20, 'bold'))
        self.second_entry.insert(0, "SS")
        self.second_entry.pack(side=tk.LEFT)

        self.tone_button = tk.Button(self.set_alarm_frame, text="Select Tone", command=self.select_tone)
        self.tone_button.pack(side=tk.LEFT)

        self.set_button = tk.Button(self.set_alarm_frame, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(side=tk.LEFT)

        self.tone_path = None

        self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.time_label.config(text=now)
        self.check_alarms()
        self.root.after(1000, self.update_clock)

    def set_alarm(self):
        alarm_time = f"{self.hour_entry.get()}:{self.minute_entry.get()}:{self.second_entry.get()}"
        self.alarms.append((alarm_time, self.tone_path))
        messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")

    def select_tone(self):
        self.tone_path = filedialog.askopenfilename(title="Select Alarm Tone", filetypes=[("Audio Files", "*.mp3 *.wav")])
        if self.tone_path:
            messagebox.showinfo("Tone Selected", f"Selected tone: {self.tone_path.split('/')[-1]}")

    def check_alarms(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        for alarm_time, tone_path in self.alarms:
            if current_time == alarm_time:
                self.play_alarm(tone_path)

    def play_alarm(self, tone_path):
        if tone_path:
            pygame.mixer.music.load(tone_path)
            pygame.mixer.music.play()
            self.snooze_alarm()

    def snooze_alarm(self):
        if messagebox.askyesno("Snooze", "Do you want to snooze the alarm?"):
            snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
            self.alarms.append((snooze_time.strftime("%H:%M:%S"), self.tone_path))
            pygame.mixer.music.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
