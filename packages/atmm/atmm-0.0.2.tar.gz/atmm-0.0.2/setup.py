from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='atmm',
    version='0.0.2',
    description='Animation Time Manager for Manim',
    url='https://github.com/chunribu/atmm',
    author='Jian Jiang',
    author_email='jianjiang.bio@gmail.com',
    packages=find_packages(),
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='Animation Time Manager Manim',
)