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

from behave import step
from hamcrest import assert_that, is_not, is_, greater_than, equal_to, contains_string, has_length
from qautils.dataset.dataset_utils import DatasetUtils
from glancesync_cmd_client.output_constants import GLANCESYNC_OUTPUT_PARALLEL_FINISHED
import commons.glancesync_output_assertions as glancesync_assertions
import logging

__copyright__ = "Copyright 2015-2016"
__license__ = " Apache License, Version 2.0"


# Get logger for Behave steps
__logger__ = logging.getLogger("parallel_steps")

__dataset_utils__ = DatasetUtils()


@step(u'files are created with output logs')
def file_created_output_logger(context):
    """
    Step: Check that generated output files by the parallel process have been created.
    """
    result = context.glancesync_cmd_client.get_output_log_list()

    assert_that(result, is_not(None),
                "Problem when executing 'ls' command")

    list_of_files = result.split("  ")
    __logger__.info("List of output log files generated by parallel process: %s", list_of_files)

    assert_that(len(list_of_files), is_(greater_than(0)),
                "No output log files have been found")

    for region in context.glance_manager_list:
        if region != context.master_region_name:
            output_files = [file for file in list_of_files if region in file]
            assert_that(len(output_files), is_(equal_to(1)),
                        "More than one out file has been found in logger dir(s) for the node '{}': '{}'. "
                        "Perhaps they have not been cleaned in previous executions...".format(region, output_files))

    context.output_file_list = list_of_files


@step(u'parallel process is executed for all nodes')
def parallel_process_is_execute_in_all_nodes(context):
    """
    Step: Check that parallel process have been executed for all nodes.
    """
    assert_that(context.glancesync_result, is_not(None),
                "Problem when executing Sync command")
    for region in context.glance_manager_list:
        if region != context.master_region_name:

            assert_that(context.glancesync_result,
                        contains_string(GLANCESYNC_OUTPUT_PARALLEL_FINISHED.format(region_name=region)),
                        "The region '{}' has not been found in the output as finished".format(region))


@step(u'the image "(?P<image_name>\w*)" is synchronized in a parallel way')
def image_is_synchronized_parallel(context, image_name):
    """
    Step: Check that the image has been synchronized in the parallel process.
    """
    if not context.output_file_list:
        file_created_output_logger(context)

    for region in context.glance_manager_list:
        if region != context.master_region_name:
            output_files = [file for file in context.output_file_list if region in file]
            file_content = obtain_out_file_content(context, output_files, region)
            glancesync_assertions.image_is_synchronized_assertion(file_content, region, image_name)


@step(u'all images are synchronized in a parallel execution')
def images_are_synchronized(context):
    """
    Step: Check that all images have been synchronized in the parallel process.
    """
    for image_name in context.created_images_list:
        image_is_synchronized_parallel(context, image_name)


@step(u'no images are synchronized in a parallel execution')
def no_images_are_sync_parallel(context):
    """
    Step: No images have been synchronized in the parallel process.
    """
    assert_that(context.glancesync_result, is_not(None),
                "Problem when executing Sync command")

    for region in context.glance_manager_list:
        if region != context.master_region_name:
            output_files = [file for file in context.output_file_list if region in file]
            file_content = obtain_out_file_content(context, output_files, region)
            glancesync_assertions.no_images_are_sync_assertion(file_content, region)


@step(u'a warning message is logged informing about checksum conflict '
      u'with "(?P<image_name>\w*)" in a parallel execution')
def warning_message_checksum_conflict_parallel(context, image_name):
    """
    Step: Warning messages are printed in logs, result of the parallel process execution: Conflicts
    """
    assert_that(context.glancesync_result, is_not(None),
                "Problem when executing Sync command")

    for region in context.glance_manager_list:
        if region != context.master_region_name:
            output_files = [file for file in context.output_file_list if region in file]
            file_content = obtain_out_file_content(context, output_files, region)
            glancesync_assertions.warning_message_checksum_conflict_assertion(file_content, region, image_name)


@step(u'the image "(?P<image_name>\w*)" is replaced in a parallel execution')
def image_is_replaced_parallel(context, image_name):
    """
    Step: Warning messages are printed in logs, result of the parallel process execution: Conflict - Replace
    """
    assert_that(context.glancesync_result, is_not(None),
                "Problem when executing Sync command")

    for region in context.glance_manager_list:
        if region != context.master_region_name:
            output_files = [file for file in context.output_file_list if region in file]
            file_content = obtain_out_file_content(context, output_files, region)
            glancesync_assertions.image_is_replaced_assertion(file_content, region, image_name)


@step(u'the image "(?P<image_name>\w*)" is renamed and replaced in a parallel execution')
def image_is_renamed_replaced(context, image_name):
    """
    Step: Warning messages are printed in logs, result of the parallel process execution: Conflict - Rename and Replace
    """
    assert_that(context.glancesync_result, is_not(None),
                "Problem when executing Sync command")

    for region in context.glance_manager_list:
        if region != context.master_region_name:
            output_files = [file for file in context.output_file_list if region in file]
            file_content = obtain_out_file_content(context, output_files, region)
            glancesync_assertions.image_is_renamed_replaced_assertion(file_content, region, image_name)


def obtain_out_file_content(context, output_files, region):
    files = output_files[0].splitlines()
    output_file = None
    for file in files:
        if region in file:
            output_file = file
        if output_file:
            file_content = context.glancesync_cmd_client.get_output_log_content(output_file)
        else:
            file_content = context.glancesync_cmd_client.get_output_log_content(output_files[0])
    return file_content
