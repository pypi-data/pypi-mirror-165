from setuptools import setup

setup(
    name='django_okta_sso',
    version='0.1.4',    
    description='Okta SSO package for Django that still uses Django users, groups, and permissions',
    url='https://github.com/crunchmasterdeluxe/django-okta-sso',
    author='Andy Gannaway',
    author_email='iamandycmd@gmail.com',
    license='BSD 2-clause',
    packages=['django_okta_sso'],
    install_requires=[],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
