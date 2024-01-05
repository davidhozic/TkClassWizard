import tkinter.ttk as ttk
import tkinter as tk

from ..convert import ObjectInfo
from ..storage import *
from ..dpi import dpi_scaled

class NicknameTooltip(tk.Toplevel):
    """
    .. versionadded:: 1.2

    Used to display a nickname tooltip based on ``ObjectInfo.nickname`` attribute.
    It's triggered on ``enter_event`` after ``timeout_ms`` milliseconds and disappears on ``leave_event``.
    """
    def __init__(
        self,
        widget: tk.Widget,
        enter_event: str,
        leave_event: str,
        timeout_ms: int = 500,
    ):
        super().__init__(widget)
        self.label = ttk.Label(self, background="white")
        self.schedule_id = None
        self._widget = widget
        self.timeout_ms = timeout_ms
        self.label.pack(padx=5, pady=5)
        self.config(bg="white")
        self.pack_propagate(True)
        self._hide_tooltip()
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        
        if isinstance(self._widget, ListBoxScrolled):
            self._widget = self._widget.listbox

        self._widget.bind(enter_event, self._schedule)
        self._widget.bind(leave_event, self._cancel_schedule)

    def _schedule(self, event: tk.Event):
        value = self._widget.get()
        if isinstance(self._widget, ListBoxObjects):
            selection = self._widget.curselection()
            if len(selection) != 1:
                return

            value = value[self._widget.current()]

        if isinstance(value, ObjectInfo) and value.nickname:
            self.label.config(text=f"({value.nickname}) {value}")
            if self.timeout_ms:
                self.schedule_id = self.after(self.timeout_ms, lambda: self._show_tooltip(event))
            else:
                self.after_idle(lambda: self._show_tooltip(event))

    def _cancel_schedule(self, event: tk.Event):
        if self.schedule_id:
            self.after_cancel(self.schedule_id)
            self.schedule_id = None

        self._hide_tooltip()

    def _show_tooltip(self, event: tk.Event):
        self.deiconify()
        self._update_pos(event)
        self._widget.bind("<Motion>", self._update_pos)
    
    def _update_pos(self, event: tk.Event):
        geo = self.geometry().split('+')[0]
        x, y = self.winfo_pointerxy()
        self.geometry(f'{geo}+{x + 10}+{y + 10}')

    def _hide_tooltip(self):
        self.withdraw()
