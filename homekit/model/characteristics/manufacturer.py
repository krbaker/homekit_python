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

from homekit.model.characteristics import CharacteristicsTypes, CharacteristicFormats, AbstractCharacteristic


class ManufacturerCharacteristic(AbstractCharacteristic):
    """
    Defined on page 156
    """

    def __init__(self, iid, manufacturer):
        AbstractCharacteristic.__init__(self, iid, CharacteristicsTypes.MANUFACTURER, CharacteristicFormats.string)
        self.value = manufacturer
        self.maxLen = 64
        self.description = 'Manufacturer'