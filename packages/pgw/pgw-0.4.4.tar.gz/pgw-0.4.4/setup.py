version = '0.4.4'
from setuptools import setup
setup(
  name='pgw',
  packages=['pygwin'],
  version=version,
  author='themixray',
  description='A library for creating Python applications.',
  license='MIT',
  install_requires=[
    'attrdict','cython','pywin32','pygame','inputs',
    'randstr','pydub','wxPython','pyautogui','moviepy',
    'pipwin','wave','opencv-python','mutagen'
  ]
)
