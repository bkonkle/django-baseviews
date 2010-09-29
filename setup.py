from distutils.core import setup

VERSION = __import__('baseviews').__version__

try:
    long_description = open('README', 'rt').read()
except IOError:
    long_description = ''

setup(
    name='django-baseviews',
    version=VERSION,
    description='A small collection of Django view classes to build upon.',
    long_description = long_description,
    author='Brandon Konkle',
    author_email='brandon@brandonkonkle.com',
    license='License :: OSI Approved :: BSD License',
    url='http://github.com/bkonkle/django-baseviews',
    packages=['baseviews'],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
    ]
)
