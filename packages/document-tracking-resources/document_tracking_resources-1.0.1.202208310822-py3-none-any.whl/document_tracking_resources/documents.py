#
# This file is part of the document_tracking_resources project.
#
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

from abc import ABC
from collections.abc import MutableMapping
from datetime import datetime
from typing import Any, Dict, Iterator, List, Type

from pandas import Series


class Features(ABC, MutableMapping):
    def __init__(self, features: Dict[str, Any] = None):
        if features is None:
            self._features = {}
        else:
            self._features = features

    def __setitem__(self, k, v) -> None:
        self._features[k] = v

    def __delitem__(self, v) -> None:
        del self._features[v]

    def __getitem__(self, k):
        return self._features[k]

    def __len__(self) -> int:
        return len(self._features)

    def __iter__(self) -> Iterator:
        return iter(self._features)


class SparseFeatures(Features, MutableMapping):
    """
    Features that are stored in a Sparse Matrix, such as TF-IDF weights. This object does not store the sparse data but
    instead only stores existing features, for every dimension, this means values with a weight of 0 are removed from
    the dictionary that associates the dict key (the TF-IDF token) and the dict value (the TF-IDF weight).

    An example of the sparse format is given below:

    .. code-block:: json

      {
        "f_title_entities": {"paris": 0.65456, "eiffel": 0.5694},
        "f_body_entities": {"paris": 0.943, "montparnasse": 0.6964},
        [...]
      }
    """

    def __init__(self, features: Dict[str, Dict[str, float]]):
        """
        :type features: dict of features as keys, other dictionaries as values. Each contain the sparse token id as key
        and the sparse weight of the corresponding sparse word as the dictionary value.
        """
        super().__init__(features)


class DenseFeatures(Features, MutableMapping):
    def __init__(self, features: Dict[str, List[float]]):
        """
        :type features: dict of features as keys, dense vectors as values.
        """
        super().__init__(features)


class Document(ABC):
    FEATURES_TYPE: Type[Features] = None

    @property
    def features(self) -> Features:
        return self._features

    def __init__(self, document: Series, features: Features):
        self.id: int = document.name
        self.timestamp: datetime = document.date.to_pydatetime()
        self._features = self.FEATURES_TYPE({key: value for key, value in features.items() if len(value) > 0})

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id and self.timestamp == other.timestamp and self.features == other.features


class DocumentWithSparseFeatures(Document):
    FEATURES_TYPE = SparseFeatures


class DocumentWithDenseFeatures(Document):
    FEATURES_TYPE = DenseFeatures
