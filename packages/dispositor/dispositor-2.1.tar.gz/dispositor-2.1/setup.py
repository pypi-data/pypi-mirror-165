from setuptools import setup, find_packages

setup(name='dispositor',
      version='2.1',
      description='Added the offset degree experiment',
      packages=['dispositor',
                'dispositor.db',
                'dispositor.experiments.degree_of_displacement',
                'dispositor.segment36'
                ],
      author_email='astro.slfd@gmail.com',
      zip_safe=False)