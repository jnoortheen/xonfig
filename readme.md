# Overview

My Xonsh configuration/dotfiles.

## Setup

``` sh
git clone ... && cd xonfig
poetry install
```

In your `~/.(ba|z)shrc`

```sh
...
# all $PATH and other environment variables updated here
...

if [ -z "$INTELLIJ_ENVIRONMENT_READER" ]; then
    
    # adjust the grep value for your system
	if [[ -z "$(ps -p $PPID -o comm | grep 'MacOS/Python')" ]]
	then
        # allow launching parent shell from xonsh
		if [[ $(uname -m) = "arm64" ]]; then
			# This is when $VIRTUALENV_HOME="~/.virtualenvs"
		 	exec ~/.virtualenvs/xonfig-*/bin/xonsh --rc=<rc.py>
		fi
	fi
fi
```
