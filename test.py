# =============================================================================
# IMPORTS
# =============================================================================
import time

# =============================================================================
# FILE IMPORTS
# =============================================================================
from utils.constants import CONTRACT
from utils.time_helpers import (
    determine_if_new_day,
    determine_today_str_timestamp,
    determine_next_midnight,
)
from utils.dec import dec
from utils.jprint import jprint

address = "0xc770EEfAd204B5180dF6a14Ee197D99d808ee52d"
markets = CONTRACT.functions.liveMarketsFor(token_=address, isPayout_=True).call()
print("Market_id", markets)
price = CONTRACT.functions.marketPrice(markets[0]).call()
print("Price: ", price)
