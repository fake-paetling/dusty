from unittest import TestCase
from mock import patch, call
from nose.tools import nottest

from dusty.runner.virtualbox import (_name_for_rule, _add_forwarding_rules,
                                     _remove_existing_forwarding_rules,
                                     update_port_forwarding_from_port_spec)

class TestVirtualBoxRunner(TestCase):
    def setUp(self):
        self.test_spec = [{'host_ip': '127.0.0.1', 'host_port': '5000',
                           'guest_ip': '', 'guest_port': '55000'},
                          {'host_ip': '127.0.0.2', 'host_port': '5001',
                           'guest_ip': '', 'guest_port': '55001'}]

    def test_name_for_rule(self):
        self.assertEqual(_name_for_rule(self.test_spec[0], 'tcp'), 'dusty_5000_tcp')
        self.assertEqual(_name_for_rule(self.test_spec[1], 'udp'), 'dusty_5001_udp')

    @nottest
    def _add_call(self, rule_spec):
        return call(['VBoxManage', 'control-vm', 'boot2docker-vm', 'natpf1', rule_spec])

    @nottest
    def _delete_call(self, rule_name):
        return call(['VBoxManage', 'control-vm', 'boot2docker-vm', 'natpf1', 'delete', rule_name])

    @patch('subprocess.check_call')
    def test_add_forwarding_rules(self, fake_check_call):
        _add_forwarding_rules(self.test_spec[0])
        _add_forwarding_rules(self.test_spec[1])
        fake_check_call.assert_has_calls([self._add_call('dusty_5000_tcp,tcp,127.0.0.1,5000,,55000'),
                                          self._add_call('dusty_5000_udp,udp,127.0.0.1,5000,,55000'),
                                          self._add_call('dusty_5001_tcp,tcp,127.0.0.2,5001,,55001'),
                                          self._add_call('dusty_5001_udp,udp,127.0.0.2,5001,,55001')])

    @patch('subprocess.check_call')
    def test_remove_existing_forwarding_rules(self, fake_check_call):
        _remove_existing_forwarding_rules(self.test_spec[0])
        _remove_existing_forwarding_rules(self.test_spec[1])
        fake_check_call.assert_has_calls([self._delete_call('dusty_5000_tcp'),
                                          self._delete_call('dusty_5000_udp'),
                                          self._delete_call('dusty_5001_tcp'),
                                          self._delete_call('dusty_5001_udp')])

    @patch('subprocess.check_call')
    def test_update_port_forwarding_from_port_spec(self, fake_check_call):
        update_port_forwarding_from_port_spec({'virtualbox': self.test_spec})
        fake_check_call.assert_has_calls([self._delete_call('dusty_5000_tcp'),
                                          self._delete_call('dusty_5000_udp'),
                                          self._add_call('dusty_5000_tcp,tcp,127.0.0.1,5000,,55000'),
                                          self._add_call('dusty_5000_udp,udp,127.0.0.1,5000,,55000'),
                                          self._delete_call('dusty_5001_tcp'),
                                          self._delete_call('dusty_5001_udp'),
                                          self._add_call('dusty_5001_tcp,tcp,127.0.0.2,5001,,55001'),
                                          self._add_call('dusty_5001_udp,udp,127.0.0.2,5001,,55001')])
