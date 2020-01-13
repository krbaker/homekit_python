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

from homekit.model import get_id
from homekit.model.characteristics import ActiveCharacteristic, ActiveIdentifierCharacteristic, \
    ConfiguredNameCharacteristic, SleepDiscoveryModeCharacteristic, BrightnessCharacteristic, \
    ClosedCaptionsCharacteristic, DisplayOrderCharacteristic, CurrentMediaStateCharacteristic, \
    TargetMediaStateCharacteristic, PictureModeCharacteristic, PowerModeSelectionCharacteristic, \
    RemoteKeyCharacteristic
from homekit.model.services import ServicesTypes, AbstractService


class TelevisionService(AbstractService):
    """
    Defined on page XXX (look https://github.com/KhaosT/HAP-NodeJS/blob/master/src/lib/gen/HomeKit-TV.ts instead)
    """

    def __init__(self):
        AbstractService.__init__(self, ServicesTypes.get_uuid('public.hap.service.television'), get_id())

        self.append_characteristic(ActiveCharacteristic(get_id()))
        self.append_characteristic(ActiveIdentifierCharacteristic(get_id()))
        self.append_characteristic(ConfiguredNameCharacteristic(get_id()))
        self.append_characteristic(SleepDiscoveryModeCharacteristic(get_id()))
        self.append_characteristic(BrightnessCharacteristic(get_id()))
        self.append_characteristic(ClosedCaptionsCharacteristic(get_id()))
        self.append_characteristic(DisplayOrderCharacteristic(get_id()))
        self.append_characteristic(CurrentMediaStateCharacteristic(get_id()))
        self.append_characteristic(TargetMediaStateCharacteristic(get_id()))
        self.append_characteristic(PictureModeCharacteristic(get_id()))
        self.append_characteristic(PowerModeSelectionCharacteristic(get_id()))
        self.append_characteristic(RemoteKeyCharacteristic(get_id()))

    def get_name(self):
        for characteristic in self.characteristics:
            if isinstance(characteristic, ConfiguredNameCharacteristic):
                return characteristic.value
        return None
