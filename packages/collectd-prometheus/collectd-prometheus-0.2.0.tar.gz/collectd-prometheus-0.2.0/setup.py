# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['collectd_prometheus']
install_requires = \
['prometheus-client>=0.7.1,<0.8.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'collectd-prometheus',
    'version': '0.2.0',
    'description': 'collectd plugin to read Prometheus metrics endpoints',
    'long_description': '# collectd-prometheus\n\nA collectd Python plugin to read Prometheus metrics endpoints\n\n## Installation\n\n1. Find out which version of Python your collectd is built against to know\n   which python/pip binary to use. So e.g. with Debian:\n   ```terminal\n   $ dpkg -S python.so | grep collectd\n   collectd-core: /usr/lib/collectd/python.so\n   $ ldd /usr/lib/collectd/python.so | grep python\n   libpython2.7.so.1.0 => /usr/lib/x86_64-linux-gnu/libpython2.7.so.1.0 (0x00007f953a5c2000)\n   $\n   ```\n   which uses Python 2.7 still so I need to use `pip2` when installing the\n   dependencies.\n1. Install `collectd-prometheus`:\n   ```terminal\n   # pip2 install collectd-prometheus\n   ```\n\n## Usage\n1. Create a collectd configuration e.g.\n   `/etc/collectd/collectd.conf.d/prom-service.conf`\n```apache\nLoadPlugin python\n<Plugin python>\n    Import "collectd_prometheus"\n    <Module "collectd_prometheus">\n       Interval 30 # How often to scrape metrics. This is the default, can be omitted\n       <Process>\n           Process "mycoolservice" # Name this instance, e.g. after what service you\'re scraping\n           Protocol "http" # This is default, can be omitted\n           Host "127.0.0.1" # This is default, can be omitted\n           Port "8080" # This is default, can be omitted\n           Filter "only|these" # A regex which matches the names of the metrics you only want to include\n           Filter "metrics" # You can even specify multiple regexes\n       </Process>\n       # Scrape another another service as well, e.g.\n       <Process>\n           Process "anothercoolservice"\n           # This time we use the defaults, except Port\n           Port "8081"\n       </Process>\n    </Module>\n</Plugin>\n```\n\n## Using a virtualenv\nIn Python, using a virtual environment [is the\nrecommended](https://docs.python.org/3/tutorial/venv.html) way to isolate your\napplications dependencies from other applications. To use a virtualenv with\ncollectd we have to create one, activate it, install our package into it.\n\n1. Using the steps listed [Installation](#installation) figure out which Python\n   version collectd uses.\n1. If python3 use `venv` which is included in Python 3. When using Python 2.7,\n   we have to [install\n   virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) which\n   can be packaged in your OS/distribution (`python-virtualenv` in Debian) or\n   you install it manually, see the linked documentation.\n1. Create your virtualenv where you want to store it, e.g:\n   ```terminal\n   # python -m virtualenv /usr/lib/collectd/prom\n   ```\n1. Activate it and install our package, e.g.:\n   ```terminal\n   # source /usr/lib/collectd/prom/bin/activate\n   (prom) # pip install collectd-prometheus\n   ```\n1. Find your virtualenvs site-packages folder, e.g:\n   ```terminal\n   # find /usr/lib/collectd/prom/ -type d -iname "site-packages"\n   /usr/lib/collectd/prom/lib/python2.7/site-packages\n   ```\n1. Configure collectd to look for `collectd-prometheus` and it\'s dependencies\n   in the directory that you found in step 5. E.g:\n\n   ```apache\n   LoadPlugin python\n   <Plugin python>\n       ModulePath "/usr/lib/collectd/prom/lib/python2.7/site-packages" # Right here\n       Import "collectd_prometheus"\n   […]\n   ```\n',
    'author': 'Ryar Nyah',
    'author_email': 'ryarnyah@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ryarnyah/collectd-prometheus',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
