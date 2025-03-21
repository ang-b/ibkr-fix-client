from enum import Enum


class IBOrderType(Enum):
    BUY = "1",
    SELL = "2",
    BUY_MINUS = "3",
    SELL_PLUS = "4",
    SELL_SHORT = "5",
    SELL_SHORT_EXEMPT = "6"