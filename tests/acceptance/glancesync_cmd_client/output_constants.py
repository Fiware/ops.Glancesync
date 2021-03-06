# -*- coding: utf-8 -*-

# Copyright 2015-2016 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FIWARE project.
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

__copyright__ = "Copyright 2015-2016"
__license__ = " Apache License, Version 2.0"


GLANCESYNC_OUTPUT_UPLOADING = "{region_name}: Uploading image {image_name}"
GLANCESYNC_OUTPUT_IMAGE_UPLOADED = "{region_name}: Image uploaded"
GLANCESYNC_OUTPUT_IMAGE_REPLACING = "{region_name}: Replacing image {image_name}"
GLANCESYNC_OUTPUT_REGION_SYNC = "{region_name}: Region is synchronized"
GLANCESYNC_OUTPUT_WARNING_IMAGES_SAME_NAME = "WARNING:Duplicated images with name {image_name} will be ignored"
GLANCESYNC_OUTPUT_RENAMING = "{region_name}: Renaming and replacing image {image_name}"
GLANCESYNC_OUTPUT_OWNER = "{region_name}: image {image_name} (UUID {uuid_image}) " \
                          "is owned by other tenant: {other_tenant}"
GLANCESYNC_OUTPUT_METADATA_UPDATING = "{region_name}: Updating the metadata of image {image_name}"
GLANCESYNC_OUTPUT_DUPLICATED = "{region_name}: image name {image_name} is duplicated."
GLANCESYNC_OUTPUT_NOT_ACTIVE = "(.*){region_name}: state of image {image_name} with UUID ([\w-]*)  is not active(.*)"
GLANCESYNC_OUTPUT_MISSING_KERNEL = "{region_name}: Not found {kernel_image_name} on region. It should be kernel_id " \
                                   "of image {image_name}"
GLANCESYNC_OUTPUT_MISSING_RAMDISK = "{region_name}: Not found {ramdisk_image_name} on region. It should be " \
                                    "ramdisk_id of image {image_name}"
GLANCESYNC_OUTPUT_WARNING_CHECKSUM_CONFLICT = "(.*)Image {image_name} has a different checksum \(([\w-]*)\) " \
                                              "in region {region_name} than in the master region. " \
                                              "It was not set what to do. Please, fill either dontupdate, " \
                                              "replace or rename with the checksum."
GLANCESYNC_OUTPUT_UPLOADING_OBSOLETE = "{region_name}: updating obsolete image {image_name}"
GLANCESYNC_OUTPUT_WARNING_OBSOLETE_IGNORE = "WARNING:Ignore obsolete master image {image_name}_obsolete " \
                                            "because {image_name} exists and it is synchronisable."
GLANCESYNC_OUTPUT_PENDING = "{region_name}: Pending: {image_name}"
GLANCESYNC_OUTPUT_STATUS_REPORT = "{status},{region_name},{image_name}"
GLANCESYNC_OUTPUT_PARALLEL_FINISHED = "Region {region_name} has finished"
