#
# This file is part of the document_tracking package

# Copyright (c) 2021 Guillaume Bernard <contact@guillaume-bernard.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import logging
from datetime import datetime

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s in %(module)s − %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

__version_info__ = {
    "number": {
        "major": "1",
        "minor": "0",
        "revision": "2",
    }
}

__version__ = ".".join(list(__version_info__.get("number").values())) + f".{datetime.utcnow().strftime('%Y%m%d%H%M')}"
