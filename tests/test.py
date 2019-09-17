import pyufw as ufw
from pprint import pprint 

print("\nDisabling")
ufw.disable()

print("\nResetting")
ufw.reset()

print("\nEnable")
ufw.enable()

print(ufw.show_logging_rules()) 
print("\nSetting logging to full")
ufw.set_logging('full')

print("\nStatus")
pprint(ufw.status())

print("\nDelete *")
ufw.delete('*')

print("\nStatus")
pprint(ufw.status())

print("\nAdding defaults")
ufw.default(incoming='deny')
ufw.default(outgoing='allow', routed='reject')

print("\nStatus")
pprint(ufw.status())

print("\nAdding rules")
ufw.add("allow out on tun0 from any to any")
ufw.add("allow in on tun0 from any to any")

print("\nStatus")
pprint(ufw.status())

print("\nListening")
pprint(ufw.show_listening())

print("\nAdded")
pprint(ufw.show_added())

print("\nAdding broken rules")
try:
    ufw.add("allow sdfsdf sdf s fds ")
except:
    print("caught exception")

print("\nTesting broken delete")
try:
    ufw.delete(10)
except:
    print("caught exception")

print("\nTesting broken delete")
try:
    ufw.default(incoming="dsdf")
except:
    print("caught exception")


print(ufw.show_logging_rules())
print("\ndisabling logging\n")
ufw.set_logging('off')

print(ufw.show_logging_rules())


print("\nFIN!")