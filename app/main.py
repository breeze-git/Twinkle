import tkinter as tk
from tkinter import ttk

import pygame

from config import ASSETS_DIR, SOUNDS_DIR


class SilentSound:
    def play(self, *args, **kwargs):
        pass

    def stop(self):
        pass


class TimerApp:
    def __init__(self, root, time, message):
        self.root = root
        self.time = time
        self.label = None
        self.message = tk.StringVar(value=message)
        self.timerid = None
        self.write_mode = False
        self.chs_time = ""
        self._inp_time = ""
        self.sounds = {}
        self.icon = tk.PhotoImage(file=ASSETS_DIR / "favicon.png")
        self.hotkeys = {
            "<Return>": self.start_timer,
            "<Escape>": self.stop_timer,
            "<KeyPress-space>": self.write_mode_controller,
            "<KeyPress-BackSpace>": self.sub_inp_time,
            "<Configure>": self._on_resize,
            "<Control-q>": self._close_app,
            "<KeyPress-h>": self.show_tooltip,
        }

        self._create_layout()
        self._load_sounds()
        self._configure_style()
        self._apply_hotkeys()

    @property
    def inp_time(self):
        return self._inp_time

    @inp_time.setter
    def inp_time(self, value):
        if not value or len(self._inp_time) < 4:
            self._inp_time = value

    def start_timer(self, event=None):
        if self.write_mode or not self.time:
            return

        self.sounds["done"].play()

        self.update_time()

    def stop_timer(self, event=None):
        if self.timerid:
            self.sounds["done"].play()
            self.root.after_cancel(self.timerid)
            self.timerid = None

    def update_time(self):
        if 0 <= self.time <= 10:
            self.sounds["countdown"].play()

        if self.time < 0:
            self.stop_timer()
            return

        self.refresh_display()

        self.time -= 1

        self.timerid = self.root.after(1000, self.update_time)

    def refresh_display(self):
        f_time = None

        if self.write_mode:
            f_time = self.format_input(self.inp_time, "_")
        else:
            f_time = self.format_time()

        self.message.set(f_time)
        self.root.update_idletasks()

    def set_time(self, event):
        self.sounds["action"].play()
        self.stop_timer()

        value = None

        if self.write_mode:
            self.inp_time += event.char
            value = self.inp_time
        else:
            self.chs_time = f"0{event.char}"
            value = self.chs_time

        f_time = self.format_input(value, "0")
        self.time = 60 * int(f_time[:2]) + min(int(f_time[3:]), 59)

        self.refresh_display()

    def sub_inp_time(self, event=None):
        self.sounds["action"].play()

        if self.write_mode:
            self._inp_time = self.inp_time[:-1]

        self.refresh_display()

    def format_time(self):
        mins = self.time // 60
        secs = self.time % 60

        return f"{mins:0>2}:{secs:0>2}"

    def format_input(self, value, fill):
        s = f"{value:{fill}<4}"

        return f"{s[:2]}:{s[2:]}"

    def write_mode_controller(self, event=None):
        self.sounds["action"].play()

        if not self.write_mode:
            self.stop_timer()
            self.label.configure(foreground="#827f7f")
        else:
            self._inp_time = ""
            self.label.configure(foreground="#ffffff")

        self.write_mode = not self.write_mode
        self.refresh_display()

    def show_tooltip(self, event=None):
        window = tk.Toplevel()
        window.title("Tooltip")
        window.geometry("600x200")
        window.resizable(False, False)

        tooltip_message = "Сочетания клавиш\n\nEnter - запустить таймер\nEscape - остановить таймер\nКлавиши 0-9 - выбрать время/ввести цифры(в руч. режиме)\nBackspace - стереть цифру(в руч. режиме)\nSpace - вкл/выкл ручной ввод\nCtrl + Q - закрыть приложение\n"

        label = ttk.Label(window, text=tooltip_message, font=("Arial", 15), anchor="nw")
        label.pack(fill="both", anchor="center", expand=True)

    def _create_layout(self):
        self.root.title("Timer v1.0")
        self.root.iconphoto(True, self.icon)

        width, height = self.root.wm_maxsize()
        self.root.geometry(f"{width}x{height}")

        self.label = ttk.Label(
            self.root,
            textvariable=self.message,
            anchor="center",
            font=("Arial", int((width + height) / 5)),
        )
        self.label.pack(anchor="center", fill="both", expand=True)

    def _load_sounds(self):
        names = ["action", "done", "countdown"]

        for name in names:
            try:
                self.sounds[name] = pygame.mixer.Sound(str(SOUNDS_DIR / f"{name}.mp3"))
                continue
            except pygame.error as e:
                print(f"Ошибка загрузки: {e}")
            except FileNotFoundError as e:
                print(f"Файл не найден: {e}")
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}")

            self.sounds[name] = SilentSound()

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background="#000000", foreground="#ffffff")

        self.root.configure(background="#000000")

    def _on_resize(self, event):
        self.label.configure(font=("Arial", int((event.width + event.height) / 7)))

    def _apply_hotkeys(self):
        for i in range(0, 10):
            key = f"<KeyPress-{i}>"
            self.hotkeys[key] = self.set_time

        for key, handler in self.hotkeys.items():
            self.root.bind(key, handler)

    def _close_app(self, event=None):
        pygame.mixer.quit()
        self.root.destroy()


def main():
    root = tk.Tk()

    pygame.mixer.init()

    timer = TimerApp(root, 60, "01:00")

    root.mainloop()


if __name__ == "__main__":
    main()
