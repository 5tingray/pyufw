import gettext
import os

import ufw.frontend
import ufw.common
import ufw.parser
import ufw.util


def _init_gettext():
    progName = ufw.common.programName
    # Due to the lack of _ method (of gettext module) in builtins namespace, some methods used in ufw fail
    gettext.install(progName)  # fixes '_' not defined. Performs builtins.__dict__['_'] = self.gettext according to https://github.com/python/cpython/blob/3.9/Lib/gettext.py


def _update_ufw_dependencies():  # When the state is changed externaly (i.e. another python program), a previous frontend instance does not detect the changes
    _init_gettext()
    frontend = ufw.frontend.UFWFrontend(dryrun=False)
    return frontend, frontend.backend


_init_gettext()

frontend = ufw.frontend.UFWFrontend(dryrun=False)
backend = frontend.backend


def _run_rule(rule_str, force=True):
    
    _init_gettext()

    p = ufw.parser.UFWParser()

    # Rule commands
    for i in ['allow', 'limit', 'deny' , 'reject', 'insert', 'delete']:
        p.register_command(ufw.parser.UFWCommandRule(i))
        p.register_command(ufw.parser.UFWCommandRouteRule(i))

    pr = p.parse_command(rule_str.split(' '))

    rule = pr.data.get('rule', '') 
    ip_type = pr.data.get('iptype', '')

    return frontend.do_action(pr.action, rule, ip_type, force)


def enable():
    _init_gettext()
    frontend.set_enabled(True)


def disable():
    _init_gettext()
    frontend.set_enabled(False)


def reset():
    _init_gettext()

    prior_state = backend.is_enabled()
    if prior_state:
        frontend.set_enabled(False)

    resp = backend.reset()

    backend.defaults = None
    backend.rules = []
    backend.rules6 = []

    backend._get_defaults()
    backend._read_rules()

    # 'ufw reset' doesn't appear to reset the default policies???? weird
    # We'll set theses defaults then instead
    default(incoming='deny', outgoing='allow', routed='reject')

    if prior_state:
        frontend.set_enabled(True)

    return resp


def reload():
    _init_gettext()
    # Only reload if ufw is enabled
    if backend.is_enabled():
        frontend.set_enabled(False)
        frontend.set_enabled(True)


def set_logging(level):
    _init_gettext()
    if not level in('on', 'off', 'low', 'medium', 'high', 'full'):
        raise ufw.common.UFWError('Logging level must be one of: on, off, medium, high, full')

    frontend.set_loglevel(level)


def default(incoming=None, outgoing=None, routed=None, force=True):
    _init_gettext()
    for direction in ('incoming', 'outgoing', 'routed'):
        policy = locals()[direction]
        if not policy: continue
        if not policy in ('allow', 'deny', 'reject'):
            raise ufw.common.UFWError('Policy must be one of: allow, deny, reject')

        backend.set_default_policy(policy, direction)

    if backend.is_enabled():
        backend.stop_firewall()
        backend.start_firewall()


def add(rule, number=None, force=True):
    _init_gettext()
    
    if not rule.startswith(('allow', 'deny', 'reject', 'limit', 'route')):
        raise ufw.common.UFWError('Rule must start with one of: allow, deny, reject, limit, route')

    if rule.startswith('route'):
        if not number:
            _run_rule(rule, force=force)
        else:
            rule_parts = rule.split(' ')
            rule_parts.insert(1, 'insert {}'.format(number))
            rule = ' '.join(rule_parts)
            _run_rule(rule, force=force)
    else:
        if not number:
            _run_rule("rule {}".format(rule), force=force)
        else:
            _run_rule("rule insert {} {}".format(number, rule), force=force)


def delete(rule, force=True):
    _init_gettext()

    try:
        rule = int(rule)
    except: pass

    if type(rule) == int:
        frontend.delete_rule(rule, force=force)
    elif rule == "*":
        number_of_rules = len(get_rules())
        for _ in range(number_of_rules):
            frontend.delete_rule(1, force=force)
    else:
        if rule.split(' ')[0] == 'route':
            _run_rule("route delete {}".format(rule), force=force)
        else:
            _run_rule("rule delete {}".format(rule), force=force)


def _get_enabled():
    _init_gettext()

    for direction in ["input", "output", "forward"]:
        # Is the firewall loaded at all?
        (rc, out) = ufw.util.cmd([backend.iptables, '-L', 'ufw-user-%s' % (direction), '-n'])
        if rc == 1:
            return False
        elif rc != 0:
            raise ufw.common.UFWError("iptables: {}\n".format(out))
    return True


def status():
    _init_gettext()
    frontend, backend = _update_ufw_dependencies()  # Backend is not storing some changes that happen outside this program => create a new instance to get the last state

    if not _get_enabled():
        status = {'status': 'inactive'}
    else:
        status = {
            'status': 'active',
            'default': {
                'incoming': backend._get_default_policy(),
                'outgoing': backend._get_default_policy('output'),
                'routed': backend._get_default_policy('forward')
            },
            'rules': get_rules()
        }
    return status


def get_rules():
    _init_gettext()
    frontend, backend = _update_ufw_dependencies()  # Backend is not storing some changes that happen outside this program => create a new instance to get the last state

    rules = backend.get_rules()
    count = 1
    app_rules = {}
    return_rules = {}
    for r in rules:

        if r.dapp != "" or r.sapp != "":
            tupl = r.get_app_tuple()

            if tupl in app_rules:
                continue
            else:
                app_rules[tupl] = True

        if r.forward:
            rstr = "route {}".format(ufw.parser.UFWCommandRouteRule.get_command(r))
        else:
            rstr = ufw.parser.UFWCommandRule.get_command(r)
            
        return_rules[count] = rstr
        count += 1
    return return_rules


def show_raw():
    _init_gettext()
    return frontend.get_show_raw('raw')


def show_builtins():
    _init_gettext()
    return frontend.get_show_raw('builtins')


def show_before_rules():
    _init_gettext()
    return frontend.get_show_raw('before-rules')


def show_user_rules():
    _init_gettext()
    return frontend.get_show_raw('user-rules')


def show_logging_rules():
    _init_gettext()
    return frontend.get_show_raw('logging-rules')


def show_listening():
    _init_gettext()

    try:
        netstat = ufw.util.parse_netstat_output(backend.use_ipv6())
    except Exception:
        #Could not get listening status
        return

    listeners = []
    rules = backend.get_rules()
    l4_protocols = list(netstat.keys())
    l4_protocols.sort()
    for transport in l4_protocols:
        if not backend.use_ipv6() and transport in ['tcp6', 'udp6']: continue

        ports = list(netstat[transport].keys())
        ports.sort()
        for port in ports:
            for item in netstat[transport][port]:

                listen_addr = item['laddr']

                if listen_addr.startswith("127.") or listen_addr.startswith("::1"):
                    continue

                ifname = ""
                if listen_addr == "0.0.0.0" or listen_addr == "::":
                    listen_addr = "%s/0" % (item['laddr'])
                    addr = "*"
                else:
                    ifname = ufw.util.get_if_from_ip(listen_addr)
                    addr = listen_addr

                application = os.path.basename(item['exe'])

                rule = ufw.common.UFWRule(action="allow",
                                            protocol=transport[:3],
                                            dport=port,
                                            dst=listen_addr,
                                            direction="in",
                                            forward=False
                                            )
                rule.set_v6(transport.endswith("6"))

                if ifname != "":
                    rule.set_interface("in", ifname)
                rule.normalize()

                matching_rules = {}
                matching = backend.get_matching(rule)
                if len(matching) > 0:
                    for rule_number in matching:
                        if rule_number > 0 and rule_number - 1 < len(rules):
                            rule = backend.get_rule_by_number(rule_number)
                            rule_command = ufw.parser.UFWCommandRule.get_command(rule)
                            matching_rules[rule_number] = rule_command

                listeners.append((transport, addr, int(port), application, matching_rules))
    return listeners


def show_added():
    return get_rules()
