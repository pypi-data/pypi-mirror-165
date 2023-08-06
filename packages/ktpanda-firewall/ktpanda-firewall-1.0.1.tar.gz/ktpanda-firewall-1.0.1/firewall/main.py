#!/usr/bin/python3
import sys
import re
import time
import os
import argparse
import subprocess
import traceback
import signal
import asyncio
from pathlib import Path

def run_firewall(script, scriptargs=''):
    p = argparse.ArgumentParser(description='')

    p.add_argument('-i', '--install-service',
                   nargs='?', metavar='PATH', const='/lib/systemd/system',
                   help='Install as a systemd service')

    p.add_argument('-c', '--config',
                   metavar='PATH',
                   default='/etc/firewall',
                   help='config directory')

    p.add_argument('-s', '--controlsock', dest='controlpath',
                   action='store', metavar='PATH', type=Path,
                   default=Path('/var/run/firewall-control'),
                   help='admin control socket')

    p.add_argument('-u', '--ucontrolsock', dest='ucontrolpath',
                   action='store', metavar='PATH', type=Path,
                   default=Path('/var/run/firewall-user-control'),
                   help='user control socket')

    args = p.parse_args()


    if args.install_service:
        from firewall import service
        service.install_unit(
            Path(args.install_service),
            'firewall',
            'Firewall Manager',
            '',
            Path(script).resolve(),
            scriptargs
        )
        return

    from firewall import core

    notify = None
    try:
        from systemd import daemon
        notify = lambda: daemon.notify('READY=1')
    except ImportError:
        pass

    try:
        print('firewall daemon started', file=sys.stderr)

        asyncio.run(core.run(args.config, args.controlpath, args.ucontrolpath, notify))

    except KeyboardInterrupt:
        pass
    finally:
        print('shutting down', file=sys.stderr)

if __name__ == '__main__':
    run_firewall(sys.executable, '-m firewall.main')
