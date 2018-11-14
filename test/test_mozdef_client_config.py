#!/usr/bin/python
""" Test suite """
import unittest
import sys
# prepend the mozdef_client library so that we can locally test.
sys.path.insert(1, 'mozdef_client')
import mozdef_client  # pylint: disable=wrong-import-position
import mozdef_client_config  # pylint: disable=wrong-import-position


class TestMozDefClientConfig(unittest.TestCase):
    """ Class of tests """

    def setUp(self):
        """ Preparing test rig """
        self.library = mozdef_client_config.ConfigedMozDefEvent()

    def test_init(self):
        """ Verify that the self object was initialized """
        self.assertIsInstance(self.library,
                              mozdef_client.MozDefEvent)
        self.assertIsInstance(self.library,
                              mozdef_client_config.ConfigedMozDefEvent)
        # pylint: disable=protected-access
        self.assertIsInstance(self.library._send_events, bool,
                              '_send_events must be a bool')
        self.assertTrue(self.library._send_events,
                        '_send_events defaults to True')

    def test_send_squished(self):
        """ Verify that the send doesn't die when "not sending" """
        self.library.summary = 'a test message'
        self.library.tags = ['test-tag1', 'test-tag2']
        self.library.details = {'testing': True, 'alert': False,
                                'is-a-test': 'yes'}
        # pylint: disable=protected-access
        self.library._send_events = False
        try:
            self.library.send()
        except Exception:  # pylint: disable=broad-except
            # there are many 'raise' items in send, none of which should hit.
            # And since this is a test, broad is intentional and fine.
            self.fail("send() raised ExceptionType unexpectedly.")

    def test_send_actual(self):
        """ Verify that the send doesn't die when sending """
        self.library.summary = 'a test message'
        self.library.tags = ['test-tag1', 'test-tag2']
        self.library.details = {'testing': True, 'alert': False,
                                'is-a-test': 'yes'}
        try:
            self.library.send()
        except Exception:  # pylint: disable=broad-except
            # there are many 'raise' items in send, none of which should hit.
            # And since this is a test, broad is intentional and fine.
            self.fail("send() raised ExceptionType unexpectedly.")
