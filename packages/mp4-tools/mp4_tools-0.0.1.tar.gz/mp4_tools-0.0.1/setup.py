from setuptools import setup, find_packages


setup(
    name='mp4_tools',
    version='0.0.1',
    license='MIT',
    author="Happy",
    author_email='zoujian49@126.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='mp4 tools',
    install_requires=[
          'coloredlogs',
          'ffmpeg-python',
          'ffmpy',
          'ffmpeg'
      ],
)