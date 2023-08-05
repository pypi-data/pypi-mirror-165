# Copyright 2019 Intel, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from venus_tempest_plugin.services import venus_data
from venus_tempest_plugin.tests.api import base


class TestDeviceProfileController(base.BaseAPITest):

    credentials = ['admin']

    def test_create_device_profile(self):
        dp = venus_data.NORMAL_DEVICE_PROFILE_DATA1
        response = self.os_admin.venus_client.create_device_profile(dp)
        self.assertEqual(dp[0]['name'], response['name'])
        self.addCleanup(self.os_admin.venus_client.delete_device_profile,
                        dp[0]['name'])

    def test_delete_multiple_device_profile(self):
        dp_one = [{
            "name": "afaas_example_1",
            "groups": [
                {"resources:FPGA": "1",
                 "trait:CUSTOM_FPGA_1": "required",
                 "trait:CUSTOM_FUNCTION_ID_3AFB": "required",
                 }
                ]
        }]
        dp_two = [{
            "name": "afaas_example_2",
            "groups": [
                {"resources:FPGA": "1",
                 "trait:CUSTOM_FPGA_1": "required",
                 "trait:CUSTOM_FUNCTION_ID_3AFB": "required",
                 }
                ]
        }]
        self.os_admin.venus_client.create_device_profile(dp_one)
        self.os_admin.venus_client.create_device_profile(dp_two)
        self.os_admin.venus_client.delete_multiple_device_profile_by_names(
            dp_one[0]['name'], dp_two[0]['name'])

    def test_get_and_delete_device_profile(self):
        dp = [{
            "name": "afaas_example_2",
            "groups": [
                {"resources:FPGA": "1",
                 "trait:CUSTOM_FPGA_1": "required",
                 "trait:CUSTOM_FUNCTION_ID_3AFB": "required",
                 }
                ]
        }]

        response = self.os_admin.venus_client.create_device_profile(dp)
        device_profile_uuid = response['uuid']
        self.assertEqual(dp[0]['name'], response['name'])
        self.assertEqual(dp[0]['groups'], response['groups'])

        response = self.os_admin.venus_client.list_device_profile()
        device_profile_list = response['device_profiles']
        device_profile_uuid_list = [it['uuid'] for it in device_profile_list]
        self.assertIn(device_profile_uuid, device_profile_uuid_list)

        response = self.os_admin.venus_client.get_device_profile(
            device_profile_uuid)
        self.assertEqual(dp[0]['name'], response['name'])
        self.assertEqual(
            device_profile_uuid,
            response['uuid'])

        self.os_admin.venus_client.delete_device_profile_by_uuid(
            device_profile_uuid)
        response = self.os_admin.venus_client.list_device_profile()
        device_profile_list = response['device_profiles']
        device_profile_uuid_list = [it['uuid'] for it in device_profile_list]
        self.assertNotIn(device_profile_uuid, device_profile_uuid_list)

    def test_delete_single_device_profile_by_name(self):
        dp = [{
            "name": "afaas_example_1",
            "groups": [
                {"resources:FPGA": "1",
                 "trait:CUSTOM_FPGA_1": "required",
                 "trait:CUSTOM_FUNCTION_ID_3AFB": "required",
                 }
                ]
        }]
        self.os_admin.venus_client.create_device_profile(dp)
        self.os_admin.venus_client.delete_device_profile(dp[0]['name'])
        list_resp = self.os_admin.venus_client.list_device_profile()
        device_profile_list = list_resp['device_profiles']
        device_profile_name_list = [it['name'] for it in device_profile_list]
        self.assertNotIn(dp[0]['name'], device_profile_name_list)

    @classmethod
    def resource_cleanup(cls):
        super(TestDeviceProfileController, cls).resource_cleanup()
