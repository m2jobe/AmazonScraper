# AmazonScraper
Amazon crawler that scrapes product information based on an inputted product search string from another retailer to provide price comparison data

This crawler uses Scrapy_ and uses Splash_ to render javascript on the given page. Follow the guides below to set them up in your local environment.

Splash runs in a docker container, see here for installation guide: Docker_

.. _Scrapy: https://github.com/scrapy/scrapy
.. _Splash: https://github.com/scrapinghub/splash
.. _Docker: https://docs.docker.com/compose/


For production or large scale crawling multiple splash servers will needed, the cookiecutter template aquarium comes in very handy for this.

Aquarium
========

Aquarium_ is a cookiecuter_ template for hassle-free
`Docker Compose`_ + Splash_ setup. Think of it as a Splash instance
with extra features and without common pitfalls.

.. Aquarium: https://github.com/TeamHG-Memex/aquarium
.. _cookiecuter: http://cookiecutter.rtfd.org
.. _Splash: https://github.com/scrapinghub/splash

