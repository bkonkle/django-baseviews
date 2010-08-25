from distutils.core import setup

setup(
    name='django-baseviews',
    version='0.1',
    description=(
        'A small collection of base Django view classes to build upon. It is',
        'intended to handle a lot of the repetition in common view patterns ',
        'and allow you to focus on what makes each view different.'
    ),
    author='Brandon Konkle',
    author_email='brandon@brandonkonkle.com',
    license='License :: OSI Approved :: BSD License',
    download_url='http://github.com/pegasus/django-baseviews',
    py_modules=['baseviews'],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
    ]
)
