#
# Copyright 2018 Joachim Lusiardi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from homekit.model.characteristics import CharacteristicsTypes, CharacteristicFormats, CharacteristicPermissions, \
    AbstractCharacteristic


class RemoteKeyCharacteristic(AbstractCharacteristic):
    """
    Defined on page XXX  (look https://github.com/KhaosT/HAP-NodeJS/blob/master/src/lib/gen/HomeKit-TV.ts instead)
    Values could be:
        REWIND = 0
        FAST_FORWARD = 1
        NEXT_TRACK = 2
        PREVIOUS_TRACK = 3
        ARROW_UP = 4
        ARROW_DOWN = 5
        ARROW_LEFT = 6
        ARROW_RIGHT = 7
        SELECT = 8
        BACK = 9
        EXIT = 10
        PLAY_PAUSE = 11
        INFORMATION = 15
        XXX = 16
    """

    def __init__(self, iid):
        AbstractCharacteristic.__init__(self, iid, CharacteristicsTypes.REMOTE_KEY,
                                        CharacteristicFormats.uint8)
        self.perms = [CharacteristicPermissions.paired_write]
        self.description = 'Target media state'
        self.minValue = 0
        self.maxValue = 16
        self.minStep = 1
        self.value = 0


class RemoteKeyCharacteristicMixin(object):
    def __init__(self, iid):
        self._remoteKey = RemoteKeyCharacteristic(iid)
        self.characteristics.append(self._targetMediaState)

    def set_on_set_callback(self, callback):
        self._remoteKey.set_set_value_callback(callback)
