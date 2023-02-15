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

# =============================================================================
# Pull bid/ask from exchanges, save to S3 at midnight
# =============================================================================
class YieldPuller:
    def __init__(self, interval, tokens):
        self.interval = interval
        self.tokens = tokens

    # =============================================================================
    # MAIN
    # =============================================================================
    def main(self):
        self.sleep_to_desired_interval()
        while True:
            self.get_data_for_all_tokens()
            self.sleep_to_desired_interval()

    # =============================================================================
    # Iterate over all tokens and get data
    # =============================================================================
    def get_data_for_all_tokens(self):
        for token in self.tokens:
            markets = self.get_markets_for_token(token)
            prices = self.get_bond_prices(markets)
            print(prices)

    # =============================================================================
    # Get array of market IDs for specific token
    # =============================================================================
    def get_markets_for_token(self, token) -> list:
        return CONTRACT.functions.liveMarketsFor(token_=token, isPayout_=True).call()

    # =============================================================================
    # Get the live market price for the bond
    # =============================================================================
    def get_bond_prices(self, markets):
        prices = {}
        for market in markets:
            price = CONTRACT.functions.marketPrice(market).call()
            prices[market] = price
        return prices

    # =============================================================================
    # Sleep until top of minute, hour, etc
    # =============================================================================
    def sleep_to_desired_interval(self):
        i = self.interval
        time.sleep(float(i) - (time.time() % float(i)))


if __name__ == "__main__":
    tokens = ["0xc770EEfAd204B5180dF6a14Ee197D99d808ee52d"]
    obj = YieldPuller(5, tokens)
    obj.main()
