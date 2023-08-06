# LiveSync

Repeatedly synchronize local workspace with a (slow) remote machine.

## Use Case

[VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview) and similar tools are great as long as your remote machine is powerfull enough.
But if your target is a Raspberry Pi, Jetson Nano/Xavier/Orin, Beagle Board or similar you feel like coding in yelly.
Especcially if you run powerful extensions like Pylance.
LiveSync solves this by watching your code and just copying the changed files to the slow remote machine.
It works best if you have some kind of relaoding meachism in place on the target.
We obviously recommend [NiceGUI](https://nicegui.io).

## Install

```bash
python3 -m pip install livesync
```

## Usage

```bash
cd <my_foder_with_vscode_workspace>
livesync <username>@<host>
```

LiveSync uses rsync (ssh) to copy the files so the `<username>@<host>` must be accessable via ssh (ideally by key not password or passphrase, because it will be called over and over).

Press `CTRL-C` to abort the sync.

NOTE: only one user can run LiveSync at a time on a target host.

## Development

```bash
python3 -m pip uninstall livesync # remove previous installed version
python3 -m pip install -e .
```

Now you can change the code and still use the `livesync` command from your `$PATH` variable.
