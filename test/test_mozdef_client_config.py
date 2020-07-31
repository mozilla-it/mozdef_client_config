""" Test suite """
import unittest
import os
import test.context  # pylint: disable=unused-import
import mock
import mozdef_client
import mozdef_client_config


class TestMozDefClientConfig(unittest.TestCase):
    """ Class of tests """

    def test_00_ingest_no_config(self):
        """ With no config files, get an error """
        with mock.patch.object(mozdef_client_config.ConfigFetchMixin, 'CONFIG_FILE_LOCATIONS',
                               new=[]):
            with self.assertRaises(ValueError):
                mozdef_client_config.ConfigedMozDefEvent()

    def test_01_ingest_empty_config(self):
        """ With junk config files, get an error """
        test_reading_file = 'test/context.py'
        with mock.patch.object(mozdef_client_config.ConfigFetchMixin, 'CONFIG_FILE_LOCATIONS',
                               new=[test_reading_file]):
            with self.assertRaises(ValueError):
                mozdef_client_config.ConfigedMozDefEvent()

    def test_02_ingest_bad_config(self):
        """ With config file lacking a url, get an error """
        test_reading_file = '/tmp/mozdef.cfg'
        with open(test_reading_file, 'w') as filepointer:
            filepointer.write('[aa]\nbb = cc\n')
        filepointer.close()
        with mock.patch.object(mozdef_client_config.ConfigFetchMixin, 'CONFIG_FILE_LOCATIONS',
                               new=[test_reading_file]):
            with self.assertRaises(ValueError):
                mozdef_client_config.ConfigedMozDefEvent()
        os.remove(test_reading_file)

    def test_03_ingest_partial_config(self):
        """ With send_events and no url, get an error """
        test_reading_file = '/tmp/mozdef.cfg'
        with open(test_reading_file, 'w') as filepointer:
            filepointer.write('[mozdef]\nsend_events = True\n')
        filepointer.close()
        with mock.patch.object(mozdef_client_config.ConfigFetchMixin, 'CONFIG_FILE_LOCATIONS',
                               new=[test_reading_file]):
            with self.assertRaises(ValueError):
                mozdef_client_config.ConfigedMozDefEvent()
        os.remove(test_reading_file)

    def test_04_ingest_noop_config(self):
        """ With send_events false and no url, proceed """
        test_reading_file = '/tmp/mozdef.cfg'
        with open(test_reading_file, 'w') as filepointer:
            filepointer.write('[mozdef]\nsend_events = False\n')
        filepointer.close()
        with mock.patch.object(mozdef_client_config.ConfigFetchMixin, 'CONFIG_FILE_LOCATIONS',
                               new=[test_reading_file]):
            with mock.patch.object(mozdef_client, '__init__') as mock_super:
                library = mozdef_client_config.ConfigedMozDefEvent()
            mock_super.assert_called_once()
        os.remove(test_reading_file)
        self.assertIsInstance(library, mozdef_client.MozDefEvent)
        self.assertIsInstance(library, mozdef_client_config.ConfigedMozDefEvent)
        self.assertIsInstance(library._send_events, bool, '_send_events must be a bool')
        self.assertFalse(library._send_events, '_send_events can be told to be False')

    def test_05_good_init(self):
        """ Verify that the self object was initialized """
        test_reading_file = '/tmp/mozdef.cfg'
        with open(test_reading_file, 'w') as filepointer:
            filepointer.write('[mozdef]\nmozdef_url = foo\n')
        filepointer.close()
        with mock.patch.object(mozdef_client_config.ConfigFetchMixin, 'CONFIG_FILE_LOCATIONS',
                               new=[test_reading_file]):
            library = mozdef_client_config.ConfigedMozDefEvent()
        self.assertIsInstance(library, mozdef_client.MozDefEvent)
        self.assertIsInstance(library, mozdef_client_config.ConfigedMozDefEvent)
        self.assertIsInstance(library._send_events, bool, '_send_events must be a bool')
        self.assertTrue(library._send_events, '_send_events defaults to True')

    def test_11_properties(self):
        """ Verify that property wrappers work """
        test_reading_file = '/tmp/mozdef.cfg'
        with open(test_reading_file, 'w') as filepointer:
            filepointer.write('[mozdef]\nmozdef_url = foo\n')
        filepointer.close()
        with mock.patch.object(mozdef_client_config.ConfigFetchMixin, 'CONFIG_FILE_LOCATIONS',
                               new=[test_reading_file]):
            library = mozdef_client_config.ConfigedMozDefEvent()
        # Don't set anything?  It's an event:
        self.assertEqual(library.category, 'event')
        # Setting:
        library.category = 'Authentication'
        # Getting OUR property:
        self.assertEqual(library.category, 'authentication')
        # And the upstream property (this might change in the future):
        self.assertEqual(library._category, 'authentication')

        self.assertEqual(library.source, None)
        # Setting:
        library.source = 'SomeWords Go Here'
        # Getting OUR property:
        self.assertEqual(library.source, 'SomeWords Go Here')
        # And the upstream property (this might change in the future):
        self.assertEqual(library._source, 'SomeWords Go Here')

    def test_send_squished(self):
        """ Verify that the send doesn't die when "not sending" """
        test_reading_file = '/tmp/mozdef.cfg'
        with open(test_reading_file, 'w') as filepointer:
            filepointer.write('[mozdef]\nmozdef_url = foo\n')
        filepointer.close()
        with mock.patch.object(mozdef_client_config.ConfigFetchMixin, 'CONFIG_FILE_LOCATIONS',
                               new=[test_reading_file]):
            library = mozdef_client_config.ConfigedMozDefEvent()
        library.summary = 'a test message'
        library.tags = ['test-tag1', 'test-tag2']
        library.details = {'testing': True, 'alert': False,
                           'is-a-test': 'yes'}
        library._send_events = False
        try:
            library.send()
        except Exception:  # pragma: no cover  pylint: disable=broad-except
            # there are many 'raise' items in send, none of which should hit.
            # And since this is a test, broad is intentional and fine.
            self.fail("send() raised ExceptionType unexpectedly.")

    def test_send_actual(self):
        """ Verify that the send doesn't die when sending """
        test_reading_file = '/tmp/mozdef.cfg'
        with open(test_reading_file, 'w') as filepointer:
            filepointer.write('[mozdef]\nmozdef_url = foo\n')
        filepointer.close()
        with mock.patch.object(mozdef_client_config.ConfigFetchMixin, 'CONFIG_FILE_LOCATIONS',
                               new=[test_reading_file]):
            library = mozdef_client_config.ConfigedMozDefEvent()
        library.summary = 'a test message'
        library.tags = ['test-tag1', 'test-tag2']
        library.details = {'testing': True, 'alert': False,
                           'is-a-test': 'yes'}
        try:
            library.send()
        except Exception:  # pragma: no cover  pylint: disable=broad-except
            # there are many 'raise' items in send, none of which should hit.
            # And since this is a test, broad is intentional and fine.
            self.fail("send() raised ExceptionType unexpectedly.")
