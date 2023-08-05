# -*- coding: utf-8 -*-
# 2018 to present - Copyright Microchip Technology Inc. and its subsidiaries.

# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.

# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR
# PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL,
# PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY
# KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP
# HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.

import os
import time
import platform
from pathlib import Path
import hid

from tpds.tp_utils import run_subprocess_cmd
from tpds.tp_utils.tp_settings import TPSettings
from tpds.proto_boards import TPBoardConfig
from pykitinfo import pykitinfo
from pymcuprog.backend import Backend, SessionConfig
from pymcuprog.toolconnection import ToolUsbHidConnection

class FlashProgram():
    """
    Class with methods which help with wrappers and
    helpers for flash hex file into CryptoAuth Trust Platform board
    """
    def __init__(self, board_info=None):
        if board_info is None:
            board_info = TPBoardConfig().board_config.get('DM320118')

        self.board_info = board_info
        self.board_details = None

    def check_board_status(self):
        board_connected = False
        factory_programmed = False

        for kit in pykitinfo.detect_all_kits():
            if kit.get('debugger',{}).get('kitname','') == self.board_info.get('kitname'):
                board_connected = True
                self.board_details = kit

        for dev in hid.enumerate(
                            vendor_id=self.board_info.get('vendor_id', 0),
                            product_id=self.board_info.get('application_pid', 0)):
            if dev['product_string'] == self.board_info.get('product_string'):
                factory_programmed = True

        if factory_programmed is True:
            board_status = 'factory_programmed'
        elif board_connected is True:
            board_status = 'board_connected'
        else:
            board_status = 'board_disconnected'

        return board_status

    def is_board_connected(self):
        return not self.check_board_status() == 'board_disconnected'

    def is_factory_programmed(self):
        return self.check_board_status() == 'factory_programmed'

    def load_hex_image(self, hexfile_path):
        """
        Function which check whether the proper device connected or not
        if connected which flash default factory reset image

        Outputs:
              Returns true or error message
        """
        try:
            backend = Backend()
            backend.connect_to_tool(ToolUsbHidConnection(serialnumber=self.board_details.get('serial_number')))
            backend.start_session(SessionConfig(self.board_details.get('debugger',{}).get('device')))
            backend.erase()
            backend.write_hex_to_target(hexfile_path)
            programming_status = 'Success'  #if backend.verify_hex(hexfile_path) else 'Verify Failed'
        except BaseException as e:
            raise ValueError(
                    f'Programming failed with {e}, Please rerun or program manually!')
        finally:
            # Cleanup
            time.sleep(2)  # delay to allow USB reenumeration
            backend.release_from_reset()
            time.sleep(2)  # delay to allow USB reenumeration
            backend.end_session()

        return programming_status

    def load_hex_image_with_ipe(self, hexfile_path):
        """
        Function which check whether the proper device connected or not
        if connected which flash default factory reset image

        Outputs:
              Returns true or error message
        """
        tp_settings = TPSettings()
        mplab_paths = tp_settings.get_mplab_paths()
        self.mplab_path = mplab_paths.get('mplab_path')
        self.jar_loc = mplab_paths.get('jar_loc')
        self.java_loc = mplab_paths.get('java_loc')

        if not self.mplab_path:
            raise PermissionError(
                'MPLAB Path is not set... Pls program manually')

        if self.jar_loc is None or self.java_loc is None:
            raise FileNotFoundError(
                'jar/java file(s) not found... Pls program manually')

        if not os.path.exists(hexfile_path):
            raise FileNotFoundError(
                f'{hexfile_path} is not found... Pls program manually')

        subprocessout = self.__flash_micro(hexfile_path)
        if subprocessout.returncode:
            raise ValueError(
                    'Programming failed with {} error code, Please rerun \
                    \nor program manually!'.format(subprocessout.returncode))

        # Cleanup
        time.sleep(2)  # delay to allow USB reenumeration
        try:
            for f in os.listdir(os.getcwd()):
                if "mplabxlog" in f.lower():
                    os.remove(f)
            os.remove('log.0')
        except Exception:
            pass

        return 'success'

    def __flash_micro(self, hexfile_path):
        """
        Function which flash the hex file into crypto trust platform board
        by executing command

        Examples:
            To flash hex file: java -jar "C:\\Program Files (x86)\\Microchip\
                \\MPLABX\\v5.30\\mplab_platform\\mplab_ipe\\ipecmd.jar" \
                -PATSADM21E18A -TPPKOB -ORISWD -OL -M -F"cryptoauth_trust_platform.hex"
        Inputs:
              hexfile_path              Hex file which will be flashed into
                                        CryptoAuth Trust Platform

        Outputs:
               Returns a namedtuple of ['returncode', 'stdout', 'stderr']

               returncode               Returns error code from terminal
               stdout                   All standard outputs are accumulated
                                        here.
               srderr                   All error and warning outputs
        """
        print('Started Flash Programming, please wait a moment...', end='')
        if platform.system().lower() == 'darwin':
            subprocessout = run_subprocess_cmd(
                cmd=[
                    str(self.jar_loc),
                    "-P"+self.board_info.get('mcu_part_number'),
                    "-TP"+self.board_info.get('program_tool'),
                    "-OL",
                    "-M",
                    ("-F"+str(Path(hexfile_path)))])
        else:
            print([
                    str(Path(self.java_loc)),
                    "-jar",
                    str(self.jar_loc),
                    "-P"+self.board_info.get('mcu_part_number'),
                    "-TP"+self.board_info.get('program_tool'),
                    "-OL",
                    "-M",
                    ("-F"+str(Path(hexfile_path)))])
            subprocessout = run_subprocess_cmd(
                cmd=[
                    str(Path(self.java_loc)),
                    "-jar",
                    str(self.jar_loc),
                    "-P"+self.board_info.get('mcu_part_number'),
                    "-TP"+self.board_info.get('program_tool'),
                    "-OL",
                    "-M",
                    ("-F"+str(Path(hexfile_path)))])
        print('OK')
        return subprocessout

    def get_board_config(self):
        return self.board_info


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    pass

__all__ = ['FlashProgram']
