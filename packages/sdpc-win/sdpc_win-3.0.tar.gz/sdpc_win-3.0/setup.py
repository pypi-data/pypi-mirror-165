from setuptools import setup, find_packages

setup(
    name='sdpc_win',
    version='3.0',
    description='a library for sdpcPY (windows version)',
    license='MIT License',
    url='https://github.com/THU-JWonderLand/sdpcPY-win',
    author='Qiming He, Renao Yan, Yiqing Liu, Jiawen Li',
    author_email='lijiawen21@mails.tsinghua.edu.cn',
    packages=['sdpc'],
    package_dir={'sdpc': 'sdpc'},
    package_data={'sdpc': ['*.py', 'DLL/*.lib', 'DLL/dll/*.dll']},
    platforms='windows',
    install_requires=['numpy'],
)