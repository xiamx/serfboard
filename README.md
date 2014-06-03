# To develop locally


## Initializing tools

```bash

source devenv.sh
cd $DIR_WHERE_YOU_WANT_TO_STORE_SERF_CONFIG
board.py init

```

## Install boards(plugins)

```bash

board.py install $GITHUB_NAMESPACE/$GITHUB_REPO

# for example board.py install xiamx/foo

```

## Run serf

```

serf agent -config-dir serf.conf.d

```

See https://github.com/xiamx/foo for an example of a board/plugin 

