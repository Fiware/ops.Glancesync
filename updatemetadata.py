#!/usr/bin/env python
# -- encoding: utf-8 --
#
# Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-Core project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#
author = 'jmpr22'
import sys
import os
from glancesync import GlanceSync

images_with_changes = {
    '2d-ui-r3.3.3': ('fiware:userinterface', 1303, True),
    '3D-UI-XML3D': ('fiware:userinterface', 1304, True),
    'cloud-rendering-r3.3.3': ('fiware:userinterface', 1305, True),
    'VirtualCharacters': ('fiware:userinterface', 1306, True),
    'interface-designer-r3.3.3': ('fiware:userinterface', 1307, True),
    '2D3DCapture-3.3.3': ('fiware:userinterface', 1308, True),
    'GIS-3.3.3': ('fiware:userinterface', 1309, True),
    'RealVirtualInteractionGE-3.3.3':  ('fiware:userinterface', 1310, True),
}


def update_nids(region):
    """Update (or add) the nid and/or type of the images.

    It uses the dictionary images_with_changes
    """
    glancesync = GlanceSync()
    for image in glancesync.get_images_region(region):
        if image['Name'] in images_with_changes:
            (typei, nid, public) = images_with_changes[image['Name']]
            if nid:
                nid = str(nid)
            if public:
                is_public = 'Yes'
            else:
                is_public = 'No'
            # don't update if values haven't changed.
            if (image.get('_nid', None) == nid and
                    image.get('_type', None) == typei and
                    image.get('Public') == is_public):
                continue
            image['_nid'] = nid
            image['_type'] = typei
            image['Public'] = is_public
            glancesync.update_metadata_image(region, image)

if __name__ == '__main__':
    update_nids('Spain')
