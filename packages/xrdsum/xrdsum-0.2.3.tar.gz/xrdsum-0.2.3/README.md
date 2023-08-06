# xrdsum

[XrootD](https://xrootd.org) plugin for calculating checksums and storing them
in extended attributes. Currently supports ADLER32 checksum and HDFS as backend.
Borrows heavily from [cephsum plugin](https://github.com/snafus/cephsum).

This plugin is designed to easily accommodate new checksum types and backends.
Additional dependencies for backends are defined as optional dependencies for
the package (see usage instructions).

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![Code style: black][black-badge]][black-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Gitter][gitter-badge]][gitter-link]

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/BristolComputing/xrdsum/workflows/CI/badge.svg
[actions-link]:             https://github.com/BristolComputing/xrdsum/actions
[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]:               https://github.com/psf/black
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/BristolComputing/xrdsum/discussions
[gitter-badge]:             https://badges.gitter.im/https://github.com/BristolComputing/xrdsum/community.svg
[gitter-link]:              https://gitter.im/https://github.com/BristolComputing/xrdsum/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[pypi-link]:                https://pypi.org/project/xrdsum/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/xrdsum
[pypi-version]:             https://badge.fury.io/py/xrdsum.svg
[rtd-badge]:                https://readthedocs.org/projects/xrdsum/badge/?version=latest
[rtd-link]:                 https://xrdsum.readthedocs.io/en/latest/?badge=latest
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
<!-- prettier-ignore-end -->

## Usage

xrdsum requires Python version >=3.8. To install, run:

```bash
pip install xrdsum[hdfs]
```

```bash
xrdsum --help
Usage: xrdsum [OPTIONS] COMMAND [ARGS]...

  Callback to give the --verbose and --debug options to all commands

Options:
  -v, --verbose         Verbose output
  -d, --debug           Debug output
  -l, --log-file TEXT   Log file
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  get     Get the checksum of a file.
  verify  Check if a file has the correct checksum.
```

Example:

```bash
/usr/bin/time -v xrdsum --verbose  --debug get  /xrootd/dteam/user/jwalder/file_1GB_020 --read-size 128
```

### xrootd config

```
# ensure cksum adler32 is included in the tpc directive, in order to caclulate by default on transfer
ofs.tpc cksum adler32 fcreds ?gsi =X509_USER_PROXY autorm xfr 40 pgm /etc/xrootd/xrdcp-tpc.sh

# add this line to trigger external checksum calculation. Would be overwritten by other xrootd.chksum lines
xrootd.chksum max 50 adler32 /etc/xrootd/xrdsum.sh
```

with `/etc/xrootd/xrdcp-tpc.sh` containing:

```bash
#!/bin/sh

# from https://github.com/snafus/cephsum/blob/master/scripts/xrdcp-tpc.sh
#Original code
#/usr/bin/xrdcp --server -f $1 root://$XRDXROOTD_PROXY/$2

# Get the last two variables as SRC and DST, all others are assumed as additional arguments
OTHERARGS="${@:1:$#-2}"
DSTFILE="${@:$#:1}"
SRCFILE="${@:$#-1:1}"


/usr/bin/xrdcp $OTHERARGS --server -f $SRCFILE root://$XRDXROOTD_PROXY/$DSTFILE
```

and with `/etc/xrootd/xrdsum.sh` containing:

```bash
#!/usr/bin/env bash

RESULT=$(xrdsum get --store-result --chunk-size 64 --verbose --storage-catalog /etc/xrootd/storage.xml "$1")
ECODE=$?

# XRootD expects return on stdout - checksum followed by a new line
printf "%s\n" "$RESULT"
exit "$ECODE"
```

### Conda installation example

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda
rm -f Miniconda3-latest-Linux-x86_64.sh
export PATH="/miniconda/bin:$PATH"
conda init
conda update -y conda
conda install python=3.10
pip install xrdsum[hdfs]
```
