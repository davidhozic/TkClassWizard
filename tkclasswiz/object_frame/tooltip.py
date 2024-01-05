import tkinter.ttk as ttk
import tkinter as tk

from typing import Optional

from ..convert import ObjectInfo
from ..storage import *
from ..dpi import dpi_scaled
from abc import ABCMeta, abstractmethod


class BaseToolTip(tk.Toplevel):
    """
    .. versionadded:: 1.2

    Used to display a nickname tooltip based on ``ObjectInfo.nickname`` attribute.
    It's triggered on ``enter_event`` after ``timeout_ms`` milliseconds and disappears on ``leave_event``.
    """
    __metaclass__ = ABCMeta

    def __init__(
        self,
        widget: tk.Widget,
        timeout_ms: int = 500,
    ):
        super().__init__(widget)
        self.label = ttk.Label(self, background="white", wraplength=1000)
        self.schedule_id = None
        self._widget = widget
        self.timeout_ms = timeout_ms
        self.label.pack(padx=5, pady=5)
        self.config(bg="white")
        self.pack_propagate(True)
        self._hide_tooltip()
        self.overrideredirect(True)
        self.attributes('-topmost', True)

    def _schedule(self, event: tk.Event):
        if not (value := self._get_value()):
            return

        self.label.config(text=str(value)[:3000])
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
        self.geometry("")
        self.deiconify()
        self._update_pos(event)
        self._widget.bind("<Motion>", self._update_pos)

    def _update_pos(self, event: tk.Event):
        geo = self.geometry().split('+')[0]
        x, y = self.winfo_pointerxy()
        self.geometry(f'{geo}+{x + 10}+{y + 10}')

    def _hide_tooltip(self):
        self.withdraw()
        

    @abstractmethod
    def _get_value(self) -> Optional[ObjectInfo]:
        pass



class ListboxTooltip(BaseToolTip):
    def __init__(self, widget: tk.Widget, timeout_ms: int = 500):
        if isinstance(widget, ListBoxScrolled):
            widget = widget.listbox

        super().__init__(widget, timeout_ms)
        self._widget.bind("<<ListboxSelect>>", self._schedule)
        self._widget.bind("<Leave>", self._cancel_schedule)
        self.start_y = 0

    def _get_value(self):
        value = self._widget.get()
        selection = self._widget.curselection()
        if len(selection) != 1:
            return

        value = value[self._widget.current()]
        return str(value)

    def _show_tooltip(self, event: tk.Event):
        self.start_y = self.winfo_pointery()
        super()._show_tooltip(event)

    def _update_pos(self, event: tk.Event):
        super()._update_pos(event)
        if abs(self.start_y - self.winfo_pointery()) > 10:
            self._cancel_schedule(event)


class ComboboxTooltip(BaseToolTip):
    def __init__(self, widget: tk.Widget, timeout_ms: int = 500):
        super().__init__(widget, timeout_ms)
        self._widget.bind("<Enter>", self._schedule)
        self._widget.bind("<Leave>", self._cancel_schedule)

    def _get_value(self):
        value = self._widget.get()
        return str(value)
