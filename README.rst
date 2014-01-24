===================================================
Source package of "Shinken 1.4.1" for Debian Wheezy
===================================================

Description
===========

Here is the source of a single and **minimalist** package for Debian Wheezy which embeds:

- Shinken 1.4.1 
- Pyro4 version 4.18
- and that's all!

The default configuration of this package is completely dummy.
The whole shinken configuration must be created by the
administrator after installation. If you want to check that
everything is fine just after the installation, you can log in
the WebUI (http://address:7767) with the **admin** username
and **admin** password.

Remenber: change the configuration after installation!

Make your own kind of config, even if nobody else sings along... :)


Warning
=======

This package doesn't manage the upgrade from the official
shinken package on Debian Wheezy (which embeds Shinken version 0.6.5).
To be honest, I have not even tried to test it.

Build the .deb package on Debian Wheezy
=======================================

To build the .deb package on Debian Wheezy, you can run these commands in a shell:

.. code:: sh

  # Creation of the working directory.
  git clone https://github.com/flaf/shinken-package.git
  cd shinken-package/shinken

  # Installation of the build-dependencies
  BUILD_DEPENDS='<see the debian/control file>'
  apt-get install --no-install-recommends --yes $BUILD_DEPENDS

  # Building of the Shinken package.
  ./debian/rules create_deb

And the package is in the parent directory:

.. code:: sh

  ls -l ..

