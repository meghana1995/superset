# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from copy import deepcopy
from typing import Any, Dict

from flask import Flask


class FeatureFlagManager:
    def __init__(self) -> None:
        super().__init__()
        self._get_feature_flags_func = None
        self._feature_flags: Dict[str, Any] = {}

    def init_app(self, app: Flask) -> None:
        self._get_feature_flags_func = app.config["GET_FEATURE_FLAGS_FUNC"]
        self._feature_flags = app.config["FEATURE_FLAGS"].copy()

    def get_feature_flags(self) -> Dict[str, Any]:
        if self._get_feature_flags_func:
            return self._get_feature_flags_func(deepcopy(self._feature_flags))

        return self._feature_flags

    def is_feature_enabled(self, feature: str) -> bool:
        """Utility function for checking whether a feature is turned on"""
        feature_flags = self.get_feature_flags()

        if feature_flags and feature in feature_flags:
            return feature_flags[feature]

        return False
