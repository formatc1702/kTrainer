from machine import Timer

go = Timer(-1)
go.init(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print("BOOM"))
