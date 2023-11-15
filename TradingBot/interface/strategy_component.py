import tkinter as tk
import typing
from interface.styling import *
from connectors.binance_futures import BinanceFuturesClient
from strategies import TechnicalStrategy, BreakoutStrategy

class StrategyEditor(tk.Frame):
    def __init__(self, root, binance:BinanceFuturesClient, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.root = root

        self.exchanges = {"Binance": binance}

        self.all_contracts = []
        self.all_timeframes = ["1m", "5m", "15m", "30m", "1h", "4h"]

        for exchange, client in self.exchanges.items():
            for symbol, contract in client.contracts.items():
                self.all_contracts.append(symbol + "_" + exchange.capitalize())

        self.commands_frame = tk.Frame(self, bg=BG_COLOR)
        self.commands_frame.pack(side=tk.TOP)

        self.table_frame = tk.Frame(self, bg=BG_COLOR)
        self.table_frame.pack(side=tk.TOP)

        self.add_button = tk.Button(self.commands_frame, text="Add strategy", font=GLOBAL_FONT,
                                    command=self.add_strategy_row, bg=BG_COLOR_2, fg=FG_COLOR)
        
        self.add_button.pack(side=tk.TOP)

        self.body_widgets = dict()

        self.headers = ["Strategy", "Contract", "Timeframe", "Balance %", "TP %", "SL %"]

        self.additional_parameters = dict()
        self.extra_input = dict()

        self.base_params = [
            {"code_name": "strategy_type", "widget": tk.OptionMenu, "data_type": str, "values": ["Technical", "Breakout"], "width": 10},
            {"code_name": "contract", "widget": tk.OptionMenu, "data_type": str, "values": self.all_contracts, "width": 15},
            {"code_name": "timeframe", "widget": tk.OptionMenu, "data_type": str, "values": self.all_timeframes, "width": 7},
            {"code_name": "balance_pct", "widget": tk.Entry, "data_type": float, "width": 7},
            {"code_name": "take_profit", "widget": tk.Entry, "data_type": float, "width": 7},
            {"code_name": "stop_loss", "widget": tk.Entry, "data_type": float, "width": 7},
            {"code_name": "parameters", "widget": tk.Button, "data_type": float, "text": "Parameters", 
             "bg": BG_COLOR_2, "command": self.show_popup},
            {"code_name": "activation", "widget": tk.Button, "data_type": float, "text": "OFF", 
             "bg": "darkred", "command": self.switch_strategy},
            {"code_name": "delete", "widget": tk.Button, "data_type": float, "text": "X", 
             "bg": "darkred", "command": self.delete_row},
        ]

        self.extra_params = {
            "Technical": [
                {"code_name": "rsi_length", "name": "RSI Periods", "widget": tk.Entry, "data_type": int},
                {"code_name": "ema_fast", "name": "MACD Fast Length", "widget": tk.Entry, "data_type": int},
                {"code_name": "ema_slow", "name": "MACD Slow Length", "widget": tk.Entry, "data_type": int},
                {"code_name": "ema_signal", "name": "MACD Signal Length", "widget": tk.Entry, "data_type": int},
            ],
            "Breakout": [
                {"code_name": "min_volume", "name": "Minimum Volume", "widget": tk.Entry, "data_type": float},
            ]
        }

        for idx, h in enumerate(self.headers):
            header = tk.Label(self.table_frame, text=h, 
                              bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
            header.grid(row=0, column=idx)

        for h in self.base_params:
            self.body_widgets[h['code_name']] = dict()
            if h['widget'] == tk.OptionMenu:
                self.body_widgets[h['code_name'] + "_var"] = dict()


        self.body_index = 1


    def add_strategy_row(self):
        b_index = self.body_index

        for col, base_params in enumerate(self.base_params):
            code_name = base_params['code_name']
            if base_params['widget'] == tk.OptionMenu:
                self.body_widgets[code_name + "_var"][b_index] = tk.StringVar()
                self.body_widgets[code_name + "_var"][b_index].set(base_params['values'][0])
                self.body_widgets[code_name][b_index] = tk.OptionMenu(self.table_frame, self.body_widgets[code_name + "_var"][b_index],
                                                                      *base_params['values'])
                
                self.body_widgets[code_name][b_index].config(width=base_params['width'])
            elif base_params['widget'] == tk.Entry:
                self.body_widgets[code_name][b_index] = tk.Entry(self.table_frame, justify=tk.CENTER)
            elif base_params['widget'] == tk.Button:
                self.body_widgets[code_name][b_index] = tk.Button(self.table_frame, text=base_params['text'],
                                                        bg=base_params['bg'], fg=FG_COLOR, 
                                                        command=lambda frozen_command=base_params['command']: frozen_command(b_index))
            else:
                continue
            self.body_widgets[code_name][b_index].grid(row=b_index, column=col)

        self.additional_parameters[b_index] = dict()

        for strat, params in self.extra_params.items():
            for param in params:
                self.additional_parameters[b_index][param['code_name']] = None


        self.body_index += 1

    def delete_row(self, b_index: int):
        for element in self.base_params:
            self.body_widgets[element['code_name']][b_index].grid_forget()
            del self.body_widgets[element['code_name']][b_index]

    def show_popup(self, b_index: int):
        self.popup_window = tk.Toplevel(self)
        self.popup_window.wm_title("Parameters")
        self.popup_window.config(bg=BG_COLOR)
        self.popup_window.attributes("-topmost", "true")
        self.popup_window.grab_set()

        strat_selected = self.body_widgets['strategy_type_var'][b_index].get()
        row_nb = 0

        for param in self.extra_params[strat_selected]:
            code_name = param['code_name']

            temp_label = tk.Label(self.popup_window, bg=BG_COLOR, fg=FG_COLOR, text=param['name'], font=BOLD_FONT)
            temp_label.grid(row = row_nb, column=0)

            if param['widget'] == tk.Entry:
                self.extra_input[code_name] = tk.Entry(self.popup_window, bg=BG_COLOR_2, justify=tk.CENTER, fg=FG_COLOR,
                                      insertbackground=FG_COLOR) 
                if self.additional_parameters[b_index][code_name] is not None:
                    self.extra_input[code_name].insert(tk.END, str(self.additional_parameters[b_index][code_name]))

            else:
                continue

            self.extra_input[code_name].grid(row=row_nb, column=1)
            row_nb += 1

        # Validation Button

        validation_button = tk.Button(self.popup_window, text="Validate", bg=BG_COLOR_2, fg=FG_COLOR,
                                      command=lambda: self.validate_parameters(b_index))
        validation_button.grid(row=row_nb, column=0, columnspan=2)
       
    def validate_parameters(self, b_index: int):
        strat_selected = self.body_widgets['strategy_type_var'][b_index].get()

        for param in self.extra_params[strat_selected]:
            code_name = param['code_name']
            if self.extra_input[code_name].get() == "":
                self.additional_parameters[b_index][code_name] = None
            else:
                self.additional_parameters[b_index][code_name] = param['data_type'](self.extra_input[code_name].get())

        self.popup_window.destroy()
    
    def switch_strategy(self, b_index: int):

        for param in ["balance_pct", "take_profit", "stop_loss"]:
            if self.body_widgets[param][b_index].get() == "":
                self.root.logging_frame.add_log(f"Missing {param} parameter")
                return
            
        strat_selected = self.body_widgets['strategy_type_var'][b_index].get()

        for param in self.extra_params[strat_selected]:
            if self.additional_parameters[b_index][param['code_name']] is None:
                self.root.logging_frame.add_log(f"Missing{param['code_name']} parameter")
                return
            
        symbol = self.body_widgets['contract_var'][b_index].get().split("_")[0]
        timeframe = self.body_widgets['timeframe_var'][b_index].get()
        exchange = self.body_widgets['contract_var'][b_index].get().split("_")[1]

        contract = self.exchanges[exchange].contracts[symbol]

        balance_pct = float(self.body_widgets['balance_pct'][b_index].get())
        take_profit = float(self.body_widgets['take_profit'][b_index].get())
        stop_loss = float(self.body_widgets['stop_loss'][b_index].get())

        if self.body_widgets['activation'][b_index].cget("text") == "OFF":

            if strat_selected == "Technical":
                new_strategy = TechnicalStrategy(self.exchanges[exchange],contract, exchange, timeframe, balance_pct, take_profit, stop_loss,
                                                 self.additional_parameters[b_index])
            elif strat_selected == "Breakout":
                new_strategy = BreakoutStrategy(self.exchanges[exchange],contract, exchange, timeframe, balance_pct, take_profit, stop_loss,
                                                 self.additional_parameters[b_index])
            else:
                return
            
            new_strategy.candles = self.exchanges[exchange].get_historical_candles(contract, timeframe)

            if len(new_strategy.candles) == 0:
                self.root.logging_frame.add_log(f"No historical data retrieved for {contract.symbol}")
                return
            
            if exchange == "Binance":
                self.exchanges[exchange].subscribe_channel([contract], "aggTrade")
                
            self.exchanges[exchange].strategies[b_index] = new_strategy


            for param in self.base_params:
                code_name = param['code_name']
                if code_name != "activation" and "_var" not in code_name:
                    self.body_widgets[code_name][b_index].config(state=tk.DISABLED)
            self.body_widgets['activation'][b_index].config(bg="darkgreen", text="ON")
            self.root.logging_frame.add_log(f"{strat_selected} strategy on {symbol} / {timeframe} started")
        else:
            del self.exchanges[exchange].strategies[b_index]    

            for param in self.base_params:
                code_name = param['code_name']
                if code_name != "activation" and "_var" not in code_name:
                    self.body_widgets[code_name][b_index].config(state=tk.NORMAL)
            self.body_widgets['activation'][b_index].config(bg="darkred", text="OFF")
            self.root.logging_frame.add_log(f"{strat_selected} strategy on {symbol} / {timeframe} stopped")
