import os
from pathlib import Path


SERVICE_TEMPLATE='''\
[Unit]
Description={name}
Before=network.target
{after}

[Service]
Type=notify
WorkingDirectory=/
ExecStart={cmd}
Restart=always

[Install]
WantedBy=network.target
'''

def install_unit(basepath, unit, name, after, cmd, args):
    cmd = str(cmd)
    if ' ' in cmd:
        cmd = '"' + cmd + '"'

    if args:
        cmd += ' ' + args

    text = SERVICE_TEMPLATE.format(
        name=name,
        after=after,
        cmd=cmd,
        args=args)
    svcfile = basepath / f'{unit}.service'
    svcfile.write_text(text, encoding='utf8')
    try:
        os.chmod(svcfile, 0o644)
        os.chown(svcfile, 0, 0)
    except OSError:
        pass
