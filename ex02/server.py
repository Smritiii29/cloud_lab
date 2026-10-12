
import Pyro4
from calc import Calculator

daemon = Pyro4.Daemon()

calc_uri = daemon.register(Calculator)

name_server = Pyro4.locateNS()
name_server.register("ex2.calculator", calc_uri)

print("Calculator server is running")
print("Registered name: ex2.calculator")
print("URI:", calc_uri)

daemon.requestLoop()
