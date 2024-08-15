# SPDX-FileCopyrightText: 2024 adeliae1316 <knsak.ug487@gmail.com>
#
# SPDX-License-Identifier: MIT

import sys

from .sorting_assistant import initialize_parser, main

sys.exit(main(args=initialize_parser(prog="python -m sorting_assistant")))
