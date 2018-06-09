import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
DJANGO_CONF = os.environ.get('DJANGO_CONF', 'conf.local')

try:
    module = __import__(DJANGO_CONF, globals(), locals(), ['*'])
    for k in dir(module):
        if not k.startswith('__'):
            locals()[k] = getattr(module, k)
except ImportError, e:
    import sys

    sys.stderr.write("""An import error occurred when looking for your environment
                       #settings (%s): %s""" % (DJANGO_CONF, e))
