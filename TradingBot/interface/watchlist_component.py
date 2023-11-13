import tkinter as tk
from interface.styling import *
import typing
from models import *



class Watchlist(tk.Frame):
    def __init__(self, binance_contracts: typing.Dict[str, Contract], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.binance_symbols = list(binance_contracts.keys())

        self.commands_frame = tk.Frame(self, bg=BG_COLOR)
        self.commands_frame.pack(side=tk.TOP)

        self.table_frame = tk.Frame(self, bg=BG_COLOR)
        self.table_frame.pack(side=tk.TOP)

        self.binance_label = tk.Label(self.commands_frame, text="Binance", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.binance_label.grid(row=0, column=0)

        self.binance_entry = tk.Entry(self.commands_frame, fg=FG_COLOR, justify=tk.CENTER, insertbackground=FG_COLOR, bg= BG_COLOR_2)
        self.binance_entry.bind("<Return>", self._add_binance_symbol)
        self.binance_entry.grid(row=1,column=0)

        self.body_widgets = dict()

        self.headers = ["symbol", "exchange", "bid", "ask", "remove"]

        for idx, h in enumerate(self.headers):
            header = tk.Label(self.table_frame, text=h.capitalize() if h != "remove" else "" , 
                              bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            header.grid(row=0, column=idx)

        for h in self.headers:
            self.body_widgets[h] = dict() 
            if h in ['bid', 'ask']:
                self.body_widgets[h + "_var"] = dict()

        self.body_index = 1


    def _remove_symbol(self, b_index: int):
        for h in self.headers:
            self.body_widgets[h][b_index].grid_forget()
            del self.body_widgets[h][b_index]


    def _add_binance_symbol(self, event):
        symbol = event.widget.get()

        if symbol in self.binance_symbols:
            self._add_symbol(symbol, "Binance")
            event.widget.delete(0, tk.END)

    def _add_symbol(self, symbol: str, exchange: str):
        
        b_index = self.body_index

        self.body_widgets['symbol'][b_index] = tk.Label(self.table_frame, text=symbol, bg=BG_COLOR, fg=FG_COLOR_2, font=GLOBAL_FONT)
        self.body_widgets['symbol'][b_index].grid(row=b_index, column=0)

        self.body_widgets['exchange'][b_index] = tk.Label(self.table_frame, text=exchange, bg=BG_COLOR, fg=FG_COLOR_2, font=GLOBAL_FONT)
        self.body_widgets['exchange'][b_index].grid(row=b_index, column=1)

        self.body_widgets['bid_var'][b_index] = tk.StringVar()
        self.body_widgets['ask_var'][b_index] = tk.StringVar()

        self.body_widgets['bid'][b_index] = tk.Label(self.table_frame, textvariable=self.body_widgets['bid_var'][b_index], 
                                                     bg=BG_COLOR, fg=FG_COLOR_2, font=GLOBAL_FONT)
        self.body_widgets['bid'][b_index].grid(row=b_index, column=2)

        self.body_widgets['ask'][b_index] = tk.Label(self.table_frame, textvariable=self.body_widgets['ask_var'][b_index],
                                                      bg=BG_COLOR, fg=FG_COLOR_2, font=GLOBAL_FONT)
        self.body_widgets['ask'][b_index].grid(row=b_index, column=3)

        self.body_widgets['remove'][b_index] = tk.Button(self.table_frame, text="X",
                                                      bg="darkred", fg=FG_COLOR, font=GLOBAL_FONT, command=lambda: self._remove_symbol(b_index))
        self.body_widgets['remove'][b_index].grid(row=b_index, column=4)

        self.body_index += 1

