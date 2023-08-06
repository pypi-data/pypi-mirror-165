# sparkfun_qwiicquadsolidstaterelay: Copyright (c) 2022 Graham Beland
#
# SPDX-License-Identifier: MIT
"""
`sparkfun_qwiicquadsolidstaterelay`
================================================================================

CircuitPython library for SparkFun Qwiic Quad Solid State Relay Kit (COM-16833).

* Author(s): Graham Beland, Sept. 2022

Implementation Notes
--------------------

**Hardware:**

* SparkFun Qwiic Quad Solid State Relay Kit (COM-16566)
* Hardware <https://www.sparkfun.com/products/16833>

**Software and Dependencies:**
* Adafruit CircuitPython <https://github.com/adafruit/circuitpython>
* Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>
* Adafruit CircuitPython firmware for the supported boards:
* https://circuitpython.org/downloads

* Adafruit's Bus Device library:
* https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library:
* https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "1.0.6"
__repo__ = (
    "https://github.com/gbeland/CircuitPython_Sparkfun_QwiicQuadSolidStateRelay.git"
)

# import time as tm
from adafruit_bus_device.i2c_device import I2CDevice

# public constants
DEVICE_I2C_ADDRESS = 0x08

# private constants
_REGISTER_BASE_RELAY_TOGGLE = 0x01
_REGISTER_BASE_RELAY_STATUS = 0x05
_REGISTER_BASE_RELAY_PWM = 0x10
_REGISTER_ALL_RELAY_OFF = 0x0A
_REGISTER_ALL_RELAY_ON = 0x0B
_REGISTER_ALL_RELAY_TOGGLE = 0x0C
_REGISTER_CHANGE_ADDRESS = 0xC7

# class
class Sparkfun_QwiicQuadSolidStateRelay:
    """CircuitPython class for Sparkfun Qwicc Quad Solid State Relay"""

    def __init__(self, i2c, address=DEVICE_I2C_ADDRESS, debug=False):
        """Initialize Qwiic Quad Solid State Relay for i2c."""
        self._device = I2CDevice(i2c, address)
        # save handle to i2c bus in case address is changed
        self._i2c = i2c
        self._debug = debug

    # public properites
    @property
    def connected(self):
        """Check to see of the relay is available.  Returns True if successful."""
        # Attempt a connection and see if we get an error
        try:
            self._read_command(_REGISTER_BASE_RELAY_STATUS)
        except ValueError:
            return False

        return True

    # public functions
    def relay_on(self, relay_num):
        """Turn the relay on (1-4)."""
        if relay_num in range(1, 5):
            result = self._read_command((_REGISTER_BASE_RELAY_STATUS + (relay_num - 1)))
            if result == 0:
                self._write_command(_REGISTER_BASE_RELAY_TOGGLE + (relay_num - 1))
        else:
            if self._debug:
                print("Error: relay number out of range")

    def relay_off(self, relay_num):
        """Turn the relay on (1-4)."""
        if relay_num in range(1, 5):
            result = self._read_command((_REGISTER_BASE_RELAY_STATUS + (relay_num - 1)))
            if result != 0:
                self._write_command(_REGISTER_BASE_RELAY_TOGGLE + (relay_num - 1))
        else:
            if self._debug:
                print("Error: relay number out of range")

    def relay_toggle(self, relay_num):
        """Toggle the relay on (1-4)."""
        if relay_num in range(1, 5):
            return self._write_command(_REGISTER_BASE_RELAY_TOGGLE + (relay_num - 1))
        if self._debug:
            print("relay number out of range")
        return 0

    def relay_all_on(self):
        """Turn all the relays on."""
        return self._write_command(_REGISTER_ALL_RELAY_ON)

    def relay_all_off(self):
        """Turn all the relays off."""
        return self._write_command(_REGISTER_ALL_RELAY_OFF)

    def relay_all_toggle(self):
        """Toggle all relays."""
        return self._write_command(_REGISTER_ALL_RELAY_TOGGLE)

    def relay_pwm_set(self, relay_num, pwm_value):
        """
        Sets the value for the slow PWM signal. Can be anywhere from 0(off) to 120(on)
        A full cycle takes 1 second.

        :param: The relay to set the PWM signal of
        :param: The value of the PWM signal, a value between 0 and 120
        :return: successful I2C transaction
        :rtype: bool
        """
        if relay_num in range(4):
            return self._write_register(_REGISTER_BASE_RELAY_PWM + relay_num, pwm_value)
        return 0
        # ----------------------------------------------------------------

    # get_pwm(relayNum)
    #
    # Gets the value for the slow PWM signal. Can be anywhere from 0 (off) to 120 (on).
    def relay_pwm_get(self, relay_num):
        """
        Gets the value for the slow PWM signal. Can be anywhere from 0(off) to 120(on)

        :param: The relay to get the PWM signal of
        :return: The value of the PWM signal, a value between 0 and 120
        :rtype: bool
        """
        if relay_num in range(4):
            return self._read_command(_REGISTER_BASE_RELAY_PWM + relay_num)
        return 0

    # ----------------------------------------------------------------
    # get_relay_state(relayNum)
    #
    # Returns the status of the relayNum you pass to it. Do not pass in a relay number
    # if you are using a single relay.

    def relay_state_get(self, relay_num):
        """
        Returns true if the relay is currently on, and false if it is off.
        :return: Status of the relay
        :rtype: bool
        """
        if self._read_command(_REGISTER_BASE_RELAY_STATUS + relay_num) == 0:
            return False
        return True

    def set_i2c_address(self, new_address):
        """Change the i2c address of Relay and return True if successful.
        Caution: this new address is stored in non volatile RAM
        Once this new address is sent you will need to use this new address to change
        the address back to the default address (0x08)
        (Valid addresses are within 8-118)
        """
        # check range of new address
        print(f"New Address {new_address}")
        if new_address not in range(8, 119):
            print("ERROR: Address outside 8-119 range")
            return False
        self._write_register(_REGISTER_CHANGE_ADDRESS, new_address)
        # wait a second for relay to settle after change
        # tm.sleep(1)
        # try to re-create new i2c device at new address
        try:
            self._device = I2CDevice(self._i2c, new_address)
            print(f"New address {new_address}")
        except ValueError as err:
            print("Address Change Failure")
            print(err)
            return False

        return True

    # private functions

    def _read_command(self, command):
        # Send a command then read count number of bytes.
        with self._device as device:
            device.write(bytes([command]))
            result = bytearray(1)
            device.readinto(result)

            if self._debug:
                print("$%02X => %s" % (command, [hex(i) for i in result]))

            return result[0]

    def _write_command(self, command):
        # Send a byte command to the device
        with self._device as device:
            device.write(bytes([command & 0xFF]))
            if self._debug:
                print("$%02X" % (command))

    def _write_register(self, addr, value):
        # Write a byte to the specified 8-bit register address
        with self._device as device:
            device.write(bytes([addr & 0xFF, value & 0xFF]))
            if self._debug:
                print("$%02X <= 0x%02X" % (addr, value))
