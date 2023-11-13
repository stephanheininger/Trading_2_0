import tkinter as tk
from interface.styling import *
from interface.logging_component import Logging
from connectors.binance_futures import BinanceFuturesClient
from interface.watchlist_component import Watchlist
import threading
import logging
import time
from interface.trades_component import TradesWatch
from interface.strategy_component import StrategyEditor

logger = logging.getLogger()

class Root(tk.Tk):
    def __init__(self, binance: BinanceFuturesClient):
        super().__init__()

        self.binance = binance

        self.title("Trading Bot")
        self.configure(bg=BG_COLOR)

        self.left_frame = tk.Frame(self, bg=BG_COLOR)
        self.left_frame.pack(side=tk.LEFT)

        self.right_frame = tk.Frame(self, bg=BG_COLOR)
        self.right_frame.pack(side=tk.LEFT)

        self.watchlist_frame = Watchlist(self.binance.contracts, self.left_frame, bg=BG_COLOR)
        self.watchlist_frame.pack(side=tk.TOP)

        self.logging_frame = Logging(self.left_frame, bg=BG_COLOR)
        self.logging_frame.pack(side=tk.TOP)

        self.strategy_frame = StrategyEditor(self, self.binance, self.right_frame, bg=BG_COLOR)
        self.strategy_frame.pack(side=tk.TOP)

        self.trades_frame = TradesWatch(self.right_frame, bg=BG_COLOR)
        self.trades_frame.pack(side=tk.TOP)

        self._update_ui()

    def _update_ui(self):

        #Logs
        for log in self.binance.logs:
            if not log['displayed']:
                self.logging_frame.add_log(log['log'])
                log['displayed'] = True

        #Watchlist prices
        try:
            for key, value in self.watchlist_frame.body_widgets['symbol'].items():
                symbol = self.watchlist_frame.body_widgets['symbol'][key].cget("text")
                exchange = self.watchlist_frame.body_widgets['exchange'][key].cget("text")

                #get the price
                if exchange == "Binance":
                    if symbol not in self.binance.contracts:
                        continue
                    if symbol not in self.binance.prices:
                        self.binance.get_bid_ask(self.binance.contracts[symbol])
                        continue

                    precision = self.binance.contracts[symbol].price_decimals        
                    prices = self.binance.prices[symbol]
                
                #write the price
                if prices['bid'] is not None:
                    price_str = "{0:.{prec}f}".format(prices['bid'], prec=precision)
                    self.watchlist_frame.body_widgets['bid_var'][key].set(price_str)

                if prices['ask'] is not None:
                    price_str = "{0:.{prec}f}".format(prices['ask'], prec=precision)
                    self.watchlist_frame.body_widgets['ask_var'][key].set(price_str)
        except RuntimeError as e:
            logger.error("Error while looping through watchlist dictionary: %s", e)

        self.after(1500, self._update_ui)
