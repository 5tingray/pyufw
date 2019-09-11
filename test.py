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

'''

 enable                          enables the firewall
 disable                         disables the firewall

 default ARG                     set default policy

 logging LEVEL                   set logging to LEVEL

 allow ARGS                      add allow rule
 deny ARGS                       add deny rule
 reject ARGS                     add reject rule
 limit ARGS                      add limit rule
route RULE                      add route RULE

insert NUM RULE                 insert RULE at NUM
route insert NUM RULE           insert route RULE at NUM

delete RULE|NUM                 delete RULE
route delete RULE|NUM           delete route RULE


 reload                          reload firewall
 reset                           reset firewall


 status                          show firewall status
 status numbered                 show firewall status as numbered list of RULES
 status verbose                  show verbose firewall status


 show ARG                        show firewall report


 version  

# --

pyufw.enable()
pyufw.disable()

pyufw.default()???

pyufw.add(RULE, number=None)     allow, deny, reject, limit, route
pyufw.delete(RULE)               allow, deny, reject, limit, route, 1, 2, 3, *

pyufw.reload()
pyufw.reset()

pyufw.status()

pyufw.get_rules()

# reports
pyufw.show_raw()
pyufw.show_builtins()
pyufw.show_before_rules()
pyufw.show_user_rules()
pyufw.show_logging_rules()
pyufw.show_listening()
pyufw.show_added()


 '''