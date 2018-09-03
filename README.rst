mozdef_client_config
==========

Python lib wrapper around mozdef_client
mozdef_client is an argument-driven way to send events.  However, when you have multiple disparate scripts, you end up with scripts that end up reinventing the wheel and having the same configs and credentials spread out everywhere, which is a mess.  This package unifies your mozdef client setup under one config file, so that you can simply send events from your programs, without every program needing to know WHERE to send them.  Think 'syslog': you just send events, end of story.

Building
~~~~~~~
```fpm -s python -t rpm --rpm-dist "$$(rpmbuild -E '%{?dist}' | sed -e 's#^\.##')" --iteration 1 setup.py```

Testing
~~~~~~~
Fill in the [testing] subsection of the config file, then ```make test```

Python dependencies
~~~~~~~~~~~~~~~~~~~

* python-mozdef_client

Usage
-----

.. code::

    import mozdef_client_config

    msg = mozdef_client_config.ConfigedMozDefEvent()
    msg.summary = 'a test message'
    msg.tags = ['tag1', 'tag2']
    msg.details = {'hostname': 'test', 'alert': True}
    msg.send()

