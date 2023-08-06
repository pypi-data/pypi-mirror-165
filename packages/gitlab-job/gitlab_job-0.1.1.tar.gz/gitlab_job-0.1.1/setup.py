from setuptools import setup, find_packages

setup(
   name='gitlab_job',
   version='0.1.1',
   description='GitLab script magic',
   author='Alexander Presber',
   author_email='alexander@giantmonkey.de',
   packages=find_packages(),
   install_requires=['docker'], #external packages acting as dependencies
)
