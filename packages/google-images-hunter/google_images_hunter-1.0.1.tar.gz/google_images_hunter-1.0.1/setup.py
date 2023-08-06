from setuptools import setup

setup(name='google_images_hunter',
      version='1.0.1',
      license='MIT',
      author='David Romero',
      email='davidromerorodriguez21@gmail.com',
      packages=['google_images_hunter'],
      url='https://github.com/RomeroRodriguezD/Google-Images-Hunter',
      download_url='https://github.com/RomeroRodriguezD/Google-Images-Hunter/archive/refs/tags/v1.0.1.tar.gz',
      description='Selenium-based web scraper to perform massive image downloads from Google Images search engine.',
      long_description='Selenium-based web scraper to perform massive image downloads from Google Images search engine.'
                       ' First version, hope it helps.',
      keywords=['web scraping', 'scraping', 'selenium', 'images', 'image scraping'],
      install_requires=[
            'selenium',
            'pandas'],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Programming Language :: Python",
                   'Programming Language :: Python :: 3',
                   "Topic :: Text Processing :: Markup :: HTML",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ]
      )
