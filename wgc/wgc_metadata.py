# (c) 2019-2020 Mikhail Paulyshka
# SPDX-License-Identifier: MIT

import logging
import os
import xml.etree.ElementTree as ElementTree
from typing import Dict, List

from .wgc_error import MetadataNotFoundError
from .wgc_helper import fixup_gamename

class WgcMetadata:
    '''
    Game metadata.xml file
    '''

    def __init__(self, filepath: str):
        self.__logger = logging.getLogger('wgc_metadata')

        if not os.path.exists(filepath):
            raise MetadataNotFoundError("WgcMetadata/__init__: %s does not exists" % filepath)
        
        self.__filepath = filepath
        self.__root = ElementTree.parse(filepath).getroot()


    def get_app_id(self) -> str:
        '''
        returns app id from metadata
        '''

        # metadata v5
        result = self.__root.find('app_id')
        
        # metadata v6
        if result is None:
            result = self.__root.find('predefined_section/app_id')

        #unknown version
        if result is None:
            self.__logger.error('get_app_id: None object')
            return None

        return result.text

    def get_name(self) -> str:
        '''
        returns game name from metadata
        '''

        # metadata v5
        result = self.__root.find('shortcut_name')
        
        #metadata v6
        if result is None:
            result = self.__root.find('predefined_section/shortcut_name')

        #unknown version
        if result is None:
            self.__logger.error('get_name: None object')
            return None

        return fixup_gamename(result.text)

    def get_executable_names(self) -> Dict[str,str]:
        result = dict()

        # metadata v5
        node = self.__root.find('executable_name')
        if node is not None:
            result['windows'] = node.text
        
        #metadata v6
        node = self.__root.find('predefined_section/executables')
        if node is not None:
            for executable in node:
                platform = 'windows'
                if 'emul' in executable.attrib:
                    if executable.attrib['emul'] == 'wgc_mac':
                        platform = 'macos'

                result[platform] = executable.text

        #unknown version
        if not result:
            self.__logger.error('get_executable_names: failed to find executables')
            return None

        return result

    def get_mutex_names(self) -> List[str]:
        result = list()

        # metadata v5
        mtx_config = self.__root.find('mutex_name')
        
        #metadata v6
        if mtx_config is None:
            mtx_config = self.__root.find('predefined_section/mutex_name')

        if mtx_config is not None:
            result.append(mtx_config.text)

        #unknown version
        if not result:
            self.__logger.warning('get_mutex_names: no mutexes found for application %s' % self.get_app_id())

        return result

    def get_parts_ids(self) -> List[str]:
        pass