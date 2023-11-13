import tkinter as tk
import logging
from connectors.binance_futures import BinanceFuturesClient
from interface.root_component import Root



#######################################################################################################

#######################################################################################################


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('info.log')

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s : %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


if __name__ == '__main__': 
    #API KEY
    #ffa79c377a245fc97de0d3c8c6154e143cdf37c4fb378386797aed7ec8e2377c

    #API SECRET
    #0aec650506b8e64c4620aa8abcc0aca1e1e5b0ff12ad47e5f6fad80ce10e4bc3

    binance = BinanceFuturesClient("ffa79c377a245fc97de0d3c8c6154e143cdf37c4fb378386797aed7ec8e2377c", 
                                   "0aec650506b8e64c4620aa8abcc0aca1e1e5b0ff12ad47e5f6fad80ce10e4bc3", True)
    
    root = Root(binance)
    root.mainloop()

    

    
