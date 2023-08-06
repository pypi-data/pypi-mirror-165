from setuptools import find_packages, setup
long_description = 'A tiny Python package to convert Python source code/files into images that can be executed.'
pck = find_packages(include=['py2img', 'py2img.*'])
setup(
      name='py2img',
      version='0.1',
      description='Python Source to Image converter',
      author='Itzsten',
      install_requires = ['numpy', 'Pillow'],
      author_email='itzsten@gmail.com',
      url='https://github.com/Itzsten/py2img',
      packages=pck,
      python_requires='>=3',
      keywords=['python', 'python to image', 'py to image', 'python converter', 'python run image'],
      long_description_content_type="text/markdown",
      long_description=long_description,
      classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
      ]
)