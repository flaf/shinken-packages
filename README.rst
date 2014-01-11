==========================================
Package of Shinken 1.4.1 for Debian Wheezy
==========================================

Description
===========

This is a single and **minimalist** package for Debian Wheezy which embeds:

- Shinken 1.4.1 
- Pyro4 version 4.18
- and that's all!

The default configuration of this package is completely dummy.
The whole shinken configuration must be created by the
administrator after installation. If you want to check that
all is fine just after the installation, you can log in
the WebUI (http://address:7767) with the **admin** username
and **admin** password.

Don't forget: change the configuration after installation!

Make your own kind of config, even if nobody else sings along... :)


Warning
=======

This package doesn't support the upgrade from the official
shinken package on Debian Wheezy (which embeds Shinken version 0.6.5).
To be honest, I have not even tested.

Build the package on Debian Wheezy
==================================

To build the package on Debian Wheezy, you can run these commands in a shell:


.. code:: sh

  # Installation of the build-dependencies (and git of course).
  build_depends='build-essential devscripts fakeroot debhelper quilt python-setuptools'
  apt-get install --no-install-recommends --yes git $build_depends

  # Creation of the working directory.
  git clone https://github.com/flaf/shinken-package.git
  cd shinken-package/shinken
  ./debian/rules populate_workingdir

  # Building of the Shinken package.
  debuild -us -uc && echo 'All is OK!'

And the package is in the parent directory:

.. code:: sh

  ls -l ../*.deb

If you want to install the package now because you haven't a personnal Debian
repository, you can run:

.. code:: sh

  # Installation of the dependencies.
  apt-get install python-ldap

  # Installation of the package directly with dpkg.
  dpkg -i ../*.deb

