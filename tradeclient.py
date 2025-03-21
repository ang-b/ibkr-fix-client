import quickfix as fix
import quickfix41 as fix41

from _types import IBOrderType


class TradeClient(fix.Application):
    def __init__(self, settings: fix.SessionSettings):
        default_settings: fix.Dictionary = settings.get()
        self.sender_id = fix.SenderCompID(default_settings.getString("SenderCompID"))
        self.target_id = fix.TargetCompID("IB")

    def prepareHeader(self, msg: fix.Message):
        header = msg.getHeader()
        header.setField(self.sender_id)
        header.setField(self.target_id)

    def newEquityOrderSingle(self, isin, currency, orderType: IBOrderType, quantity):
        order = fix41.NewOrderSingle()
        self.prepareHeader(order)

        # order.setField(fix.ClOrdID(x))

        order.setField(fix.CustomerOrFirm(1))  # 1: firm, 0: customer  
        order.setField(fix.HandlInst("2"))  # IB only supports 2
        # order.setField(fix.Account(x))  # required for sessions wihch route orders to multiple accounts
        
        # assume we use SMART 
        order.setField(fix.ExDestination("SMART"))
        # this is needed for smart mode, but also if trading with ISIN
        order.setField(fix.Currency(currency))  # IB accepts [USD, AUD, CAD, CHF, EUR, GBP, HKD, JPY]
        # assume we trade by ISIN
        order.setField(fix.IDSource("4"))  # 4: ISIN, 1: CUSIP 
        order.setField(fix.SecurityID(isin))
        
        order.setField(fix.OrdType(orderType))
        order.setField(fix.Quantity(quantity))
        
        fix.Session.sendToTarget(order)
