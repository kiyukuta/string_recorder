#!/bin/bash
set -o errexit
set -o nounset

CMD=wget
# On macOS, wget is not available by default.
if [[ `uname -s` = "Darwin" ]]; then
  CMD="curl -L -O"
fi
$CMD https://github.com/adobe-fonts/source-han-code-jp/archive/2.000R.tar.gz
tar zxvf 2.000R.tar.gz
