# pyufw
A python wrapper for UFW (Uncomplicated FireWall), a wrapper for iptables.

## Install
pyufw is avaliable from PyPi. You can download it using pip:

```console
$ pip3 install pyufw
```

## Documentation

```python
import pyufw as ufw
```

#### Enable the firewall
```python
ufw.enable()
```

#### Disable the firewall
```python
ufw.disable()
```

#### Reset the firewall
Returns the firewall to it's install defaults. `incoming=deny, outgoing=allow, routed=reject`  
The default rules are:
  * `allow SSH`
  * `allow to 224.0.0.251 app mDNS`
```python
ufw.reset()
```


#### Returns the status of the firewall
Retuns a dict. Status is either `'active'` or `'inactive'`. If the firewall is active the default policies and rules list will also be included.
```python
ufw.status()
```
```python
{ 
   'status':'active',
   'default':{ 
      'incoming':'deny',
      'outgoing':'allow',
      'routed':'reject'
   },
   'rules':{ 
      1:'allow out on tun0',
      2:'allow in on tun0'
   }
}
```
```python
{
    'status': 'inactive'
}
```

#### Set defaults
Set the default policies for `incoming`, `outgoing` and `routed`. Policies to choose from are `allow`, `deny` and `reject`.
```python
ufw.default(incoming='deny', outgoing='allow', routed='reject')
```

#### Add rule
Add or Insert a rule. To insert a rule you can specify a rule number but this is optional.  
Check out `man ufw` for rule syntax.  
Returns the raw iptables rule added (incase your interested)
```python
ufw.add("allow 22")
ufw.add("allow 22", number=3)
```
```python
"allow -p all --dport 22 -j ACCEPT both"
```

#### Delete rule
Delete a rule. You can specify the rule itself or the rule number.
```python
ufw.delete("allow 22")
ufw.delete(3)
```

#### Get rules
Get a list of the current rules. Returns a dict with the rule numbers as the index.
```python
ufw.get_rules()
```
```python
{ 
   1:'allow out on tun0',
   2:'allow in on tun0',
   3:'allow 22'
}
```

#### Show listening
Returns an array of listening ports, applications and rules that apply.  
Array contains a series of tuples of the following structure:  
`(str transport, str listen_address, int listen_port, str application, dict rules)`
```python
ufw.show_listening()
```
```python
[
    ('tcp', '*', '22', 'openssh', {
        3: 'allow 22'
    }), 
    ('tcp', '*', '57621', 'spotify', {}), 
    ('udp', '*', '1900', 'spotify', {}), 
    ('udp', '224.0.0.251', '5353', 'chrome', {}), 
    ('udp', '224.0.0.251', '5353', 'chrome', {}), 
    ('udp', '*', '68', 'dhclient', {})
]
```

#### Get raw iptables output
The following resources mirror the ufw cli commands and return the same unformatted string outputs. Maybe more useful for debugging.
```python
ufw.show_raw()
ufw.show_builtins()
ufw.show_before_rules()
ufw.show_user_rules()
ufw.show_logging_rules()
```

### Similar cool projects
  * https://gitlab.com/dhj/easyufw


