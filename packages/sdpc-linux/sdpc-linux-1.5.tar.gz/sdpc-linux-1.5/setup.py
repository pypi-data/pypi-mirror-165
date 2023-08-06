from setuptools import setup, find_packages

setup(
    name='sdpc-linux',
        version='1.5',
        description='a library for sdpcPY (linux version)',
        license='MIT License',
        author='Jiawen Li',
        author_email='lijiawen21@mails.tsinghua.edu.cn',
        packages=['sdpc'],
        package_dir={'sdpc': 'sdpc'},
        package_data={'sdpc': ['*.py', 'so/*', 'so/ffmpeg/*', 'so/jpeg/*']},
        platforms='linux',
        install_requires=['numpy'],
)

# package_data={'sdpc': ['*.py', 'so/*', 'so/ffmpeg/*', 'so/jpeg/*']},