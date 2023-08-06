from setuptools import setup

setup(
    name='tunnelossh',
    version='0.1.6',
    description='CETT SSH Tunneling',
    url='https://github.com/gpcortes/tunnelossh.git',
    author='Gustavo Côrtes',
    author_email='gpcortes@gmail.com',
    license='BSD 2-clause',
    packages=['tunnelossh'],
    install_requires=[
        'sshtunnel>=0.4.0', 'python-dotenv>=0.20.0', 'urllib3==1.26.11'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
    ],
)