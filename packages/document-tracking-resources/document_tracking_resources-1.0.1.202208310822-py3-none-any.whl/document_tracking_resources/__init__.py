#
# This file is part of the document_tracking_resources project.

# Copyright (c) 2021 − Present Guillaume Bernard <contact@guillaume-bernard.fr>
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
from datetime import datetime
from typing import NewType

ISO6393LanguageCode = NewType("ISO6393LanguageCode", str)

__version_info__ = {
    "number": {
        "major": "1",
        "minor": "0",
        "revision": "1",
    }
}

__version__ = (
    ".".join(list(__version_info__.get("number").values())) + f".{datetime.utcnow().strftime('%Y%m%d%H%M')}"
)
