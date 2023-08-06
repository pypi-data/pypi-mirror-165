from setuptools import setup, find_packages

setup(
    name='sdpcPY_win',
    version='2.0',
    description='a library for sdpcPY (windows version)',
    license='MIT License',
    url='https://github.com/THU-JWonderLand/sdpcPY-win',
    author='Qiming He, Renao Yan, Yiqing Liu, Jiawen Li',
    author_email='lijiawen21@mails.tsinghua.edu.cn',
    packages=find_packages(),
    include_package_data=True,
    platforms='windows',
    install_requires=['numpy'],
)