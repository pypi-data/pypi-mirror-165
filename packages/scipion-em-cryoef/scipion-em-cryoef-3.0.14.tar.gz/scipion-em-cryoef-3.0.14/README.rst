=============
Cryoef plugin
=============

This plugin provides a wrapper for `cryoEF <https://www.mrc-lmb.cam.ac.uk/crusso/cryoEF/>`_ program.

.. image:: https://img.shields.io/pypi/v/scipion-em-cryoef.svg
        :target: https://pypi.python.org/pypi/scipion-em-cryoef
        :alt: PyPI release

.. image:: https://img.shields.io/pypi/l/scipion-em-cryoef.svg
        :target: https://pypi.python.org/pypi/scipion-em-cryoef
        :alt: License

.. image:: https://img.shields.io/pypi/pyversions/scipion-em-cryoef.svg
        :target: https://pypi.python.org/pypi/scipion-em-cryoef
        :alt: Supported Python versions

.. image:: https://img.shields.io/sonar/quality_gate/scipion-em_scipion-em-cryoef?server=https%3A%2F%2Fsonarcloud.io
        :target: https://sonarcloud.io/dashboard?id=scipion-em_scipion-em-cryoef
        :alt: SonarCloud quality gate

.. image:: https://img.shields.io/pypi/dm/scipion-em-cryoef
        :target: https://pypi.python.org/pypi/scipion-em-cryoef
        :alt: Downloads

Installation
------------

You will need to use 3.0+ version of Scipion to be able to run these protocols. To install the plugin, you have two options:

a) Stable version

.. code-block::

    scipion installp -p scipion-em-cryoef

b) Developer's version

    * download repository

    .. code-block::

        git clone -b devel https://github.com/scipion-em/scipion-em-cryoef.git

    * install

    .. code-block::

        scipion installp -p /path/to/scipion-em-cryoef --devel

CryoEF binaries will be installed automatically with the plugin, but you can also link an existing installation. 
Default installation path assumed is ``software/em/cryoEF-1.1.0``, if you want to change it, set *CRYOEF_HOME* in `scipion.conf`` file to the folder where the cryoEF is installed. To check the installation, simply run the following Scipion test:

``scipion test cryoef.tests.test_protocols_cryoef.TestCryoEF``

Supported versions
------------------

1.1.0

Protocols
---------

    * orientation analysis

Detailed manual can be found in ``software/em/cryoEF-1.1.0/cryoEF_v1.1.0_manual.pdf``

References
----------

    * `1.  Naydenova, K and Russo, CJ "Measuring the effects of particle orientation to improve the efficiency of electron cryomicroscopy" Nature Communications (2017). <https://www.nature.com/articles/s41467-017-00782-3>`_
