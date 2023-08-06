from setuptools import setup


def read_file(fname):
    with open(fname) as f:
        return f.read()


setup(
    name='tailscale-util-ns',
    description='TailScale util to get device details',
    long_description=read_file('README.rst'),
    version='2.0.1',
    author='Nishith Shah',
    author_email='nshthshah@gmail.com',
    url='https://github.com/nishithcitc/tailscale-util-ns',
    packages=[
        'tailscale_ns',
    ],
    package_dir={'tailscale_ns': 'tailscale_ns'},
    install_requires=[
        'tailscale==0.2.0',
        'jmespath==1.0.0'
    ],
    include_package_data=True
)
