# © Copyright 2022 CERN. This software is distributed under the terms of
# the GNU General Public Licence version 3 (GPL Version 3), copied verbatim
# in the file "LICENCE.txt". In applying this licence, CERN does not waive
# the privileges and immunities granted to it by virtue of its status as an
# Intergovernmental Organization or submit itself to any jurisdiction.

class TransferBroker():
    """Class for transfer broker attributes."""

    def __init__(self):
        """Function to initialize the attributes."""
        self._list_src_rcsites = []
        self._list_dst_rcsites = []
        self._list_src_endpoints = []
        self._list_dst_endpoints = []
        self._from_email_address = ''
        self._to_email_address   = ''
        self._subject_email  = ''
        self._message_email  = ''
        self._link_src_state = False
        self._link_dst_state = False
        self._unidirectional = False
        self._events_to_wait = 0
        self._max_throughput = 0
        self._min_throughput = 0
        self._num_circuits   = 0
        self._sense_uuid = ''
        self._sense_vlan = ''
        self._sense_uuid_2 = ''
        self._sense_vlan_2 = ''
        self._auth_token = ''

    def get_list_src_rcsites(self):
        """Function to get list_src_rcsites attribute."""
        return self._list_src_rcsites

    def set_list_src_rcsites(self, src_rcsites):
        """Function to set list_src_rcsites attribute."""
        self._list_src_rcsites = src_rcsites

    def get_list_dst_rcsites(self):
        """Function to get list_dst_rcsites attribute."""
        return self._list_dst_rcsites

    def set_list_dst_rcsites(self, dst_rcsites):
        """Function to set list_dst_rcsites attribute."""
        self._list_dst_rcsites = dst_rcsites

    def get_list_src_endpoints(self):
        """Function to get list_src_endpoints attribute."""
        return self._list_src_endpoints

    def set_list_src_endpoints(self, endpoints):
        """Function to set list_src_endpoints attribute."""
        self._list_src_endpoints = endpoints

    def get_list_dst_endpoints(self):
        """Function to get list_dst_endpoints attribute."""
        return self._list_dst_endpoints

    def set_list_dst_endpoints(self, endpoints):
        """Function to set list_dst_endpoints attribute."""
        self._list_dst_endpoints = endpoints

    def get_link_src_state(self):
        """Function to get link_src_state attribute."""
        return self._link_src_state

    def set_link_src_state(self, state):
        """Function to set link_src_state attribute."""
        self._link_src_state = state

    def get_link_dst_state(self):
        """Function to get link_dst_state attribute."""
        return self._link_dst_state

    def set_link_dst_state(self, state):
        """Function to set link_dst_state attribute."""
        self._link_dst_state = state

    def get_from_email_address(self):
        """Function to get from_email_address attribute."""
        return self._from_email_address

    def set_from_email_address(self, email):
        """Function to set from_email_address attribute."""
        self._from_email_address = email

    def get_to_email_address(self):
        """Function to get to_email_address attribute."""
        return self._to_email_address

    def set_to_email_address(self, email):
        """Function to set to_email_address attribute."""
        self._to_email_address = email

    def get_subject_email(self):
        """Function to get subject_email attribute."""
        return self._subject_email

    def set_subject_email(self, email):
        """Function to set subject_email attribute."""
        self._subject_email = email

    def get_message_email(self):
        """Function to get message_email attribute."""
        return self._message_email

    def set_message_email(self, email):
        """Function to set message_email attribute."""
        self._message_email = email

    def get_unidirectional(self):
        """Function to get unidirectional attribute."""
        return self._unidirectional

    def set_unidirectional(self, unidir):
        """Function to set unidirectional attribute."""
        self._unidirectional = unidir

    def get_events_to_wait(self):
        """Function to get events_to_wait attribute."""
        return self._events_to_wait

    def set_events_to_wait(self, events):
        """Function to set events_to_wait attribute."""
        self._events_to_wait = events

    def get_max_throughput(self):
        """Function to get max_throughput attribute."""
        return self._max_throughput

    def set_max_throughput(self, threshold):
        """Function to set max_throughput attribute."""
        self._max_throughput = threshold

    def get_min_throughput(self):
        """Function to get min_throughput attribute."""
        return self._min_throughput

    def set_min_throughput(self, threshold):
        """Function to set min_throughput attribute."""
        self._min_throughput = threshold

    def get_num_circuits(self):
        """Function to get num_circuits attribute."""
        return self._num_circuits

    def set_num_circuits(self, circuits):
        """Function to set num_circuits attribute."""
        self._num_circuits = circuits

    def get_sense_uuid(self):
        """Function to get sense_uuid attribute."""
        return self._sense_uuid

    def set_sense_uuid(self, uuid):
        """Function to set sense_uuid attribute."""
        self._sense_uuid = uuid

    def get_sense_vlan(self):
        """Function to get sense_vlan attribute."""
        return self._sense_vlan

    def set_sense_vlan(self, vlan):
        """Function to set sense_vlan attribute."""
        self._sense_vlan = vlan

    def get_sense_uuid_2(self):
        """Function to get sense_uuid_2 attribute."""
        return self._sense_uuid_2

    def set_sense_uuid_2(self, uuid):
        """Function to set sense_uuid_2 attribute."""
        self._sense_uuid_2 = uuid

    def get_sense_vlan_2(self):
        """Function to get sense_vlan_2 attribute."""
        return self._sense_vlan_2

    def set_sense_vlan_2(self, vlan):
        """Function to set sense_vlan_2 attribute."""
        self._sense_vlan_2 = vlan

    def get_auth_token(self):
        """Function to get auth_token attribute."""
        return self._auth_token

    def set_auth_token(self, auth):
        """Function to set auth_token attribute."""
        self._auth_token = auth
