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


class ActiveIdentifierCharacteristic(AbstractCharacteristic):
    """
    Defined on page 159 (R2)
    """

    def __init__(self, iid):
        AbstractCharacteristic.__init__(self, iid, CharacteristicsTypes.ACTIVE_IDENTIFIER, CharacteristicFormats.uint32)
        self.description = 'Indicate target as selected in UI'
        # TODO notify is missing here
        self.perms = [CharacteristicPermissions.paired_read]
        self.value = 0


class ActiveIdentifierCharacteristicMixin(object):
    def __init__(self, iid):
        self._activeIdentifierCharacteristic = ActiveIdentifierCharacteristic(iid)
        self.characteristics.append(self._activeIdentifierCharacteristic)

    def set_on_set_callback(self, callback):
        self._activeIdentifierCharacteristic.set_set_value_callback(callback)

    def set_on_get_callback(self, callback):
        self._activeIdentifierCharacteristic.set_get_value_callback(callback)
