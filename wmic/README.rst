===========================================
Source package of wmi-cli for Debian Wheezy
===========================================

Description
===========

This is a (personal) package which provides **wmic**, a
simple WMI client binary

Build the .deb package on Debian Wheezy
=======================================

To build the .deb package on Debian Wheezy, you can run these commands in a shell:

.. code:: sh

  # Creation of the working directory.
  git clone https://github.com/flaf/shinken-packages.git
  cd shinken-packages/wmi-cli/wmi-cli/
  
  # Installation of the build-dependencies
  BUILD_DEPENDS='<see the debian/control file>'
  apt-get install --no-install-recommends --yes build-essential $BUILD_DEPENDS

  # Building of the package.
  ./debian/rules create_deb

And the package is in the parent directory:

.. code:: sh

  ls -l ..
