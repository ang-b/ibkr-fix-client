import quickfix as fix

from tradeclient import TradeClient

settings_file = None

try:
    settings = fix.SessionSettings(settings_file)
    store_factory = fix.FileStoreFactory(settings)
    log_factory = fix.LogFactory(settings)
    trade_client = TradeClient(settings)
    initiator = fix.SocketInitiator(
        application=trade_client,
        storeFactory=store_factory,
        settings=settings,
        logFactory=log_factory)
    initiator.start()
    try:
        trade_client.run()
    finally:
        initiator.stop()
except fix.ConfigError as e:
    print(e)
