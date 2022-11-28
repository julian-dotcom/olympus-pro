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
    def __init__(self, _id):
        self._id = _id
        self.interval = self.ask_user_for_interval()

    # =============================================================================
    # MAIN function that executes infinitely and saves midnight
    # =============================================================================
    def main(self):
        self.reset_for_new_day()
        self.sleep_to_desired_interval()
        while True:
            if determine_if_new_day(self.midnight):
                self.handle_midnight_event()
            self.get_current_bond_yield()
            self.sleep_to_desired_interval()

    # =============================================================================
    # It's midnight! Save important data and reset for next day
    # =============================================================================
    def handle_midnight_event(self):
        pass

    # =============================================================================
    # Reset all values that start a new with new day
    # =============================================================================
    def reset_for_new_day(self):
        self.today = determine_today_str_timestamp()
        self.midnight = determine_next_midnight()

    # =============================================================================
    # Fetch current bond yield from Blockchain
    # =============================================================================
    def get_current_bond_yield(self):
        cur_price = self.get_current_bond_price()
        jprint(cur_price)

    # =============================================================================
    # Get current bond price
    # =============================================================================
    def get_current_bond_price(self):
        return dec(CONTRACT.functions.marketPrice(self._id).call())

    # =============================================================================
    #
    # HELPERS
    #
    # =============================================================================

    # =============================================================================
    # Ask user for interval on how often to fetch bid/ask
    # =============================================================================
    def ask_user_for_interval(self):
        inp = int(input("Specify the desired interval in seconds: ").strip())
        if inp < 5:
            raise ValueError("Interval is too small. Execution cancelled.")
        return inp

    # =============================================================================
    # Sleep until top of minute, hour, etc
    # =============================================================================
    def sleep_to_desired_interval(self):
        time.sleep(float(self.interval) - (time.time() % float(self.interval)))


if __name__ == "__main__":
    obj = YieldPuller(4)
    obj.main()
