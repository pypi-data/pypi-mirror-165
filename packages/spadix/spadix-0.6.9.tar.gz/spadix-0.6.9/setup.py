import setuptools

package_name = 'spadix'

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='spadix',
    version='0.6.9',
    packages=setuptools.find_packages(exclude=['test']),
    install_requires=['setuptools'],
    package_data={'': [
    ]},
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    author='Serge Nikulin',
    author_email='serge@safeai.ai',
    maintainer='Serge Nikulin',
    maintainer_email='serge@safeai.ai',
    url='https://safeai.ai',
    project_urls={
        'Bug Tracker': 'https://gitlab.safeai.ai/production/spadix',
    },
    keywords=['spadix'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    description='SAF friendly wrapper for colcon',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    tests_require=['pytest'],
    test_suite='test',
    entry_points={
        'console_scripts': [
            'spadix = spadix.__main__:main',
        ],
    },
)
