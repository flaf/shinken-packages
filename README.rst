==========================================
Package of Shinken 1.4.1 for Debian Wheezy
==========================================

Description
===========

This is a single and **minimalist** package for Debian Wheezy which embeds:

- Shinken 1.4.1 
- Pyro4 version 4.18
- and that's all!

The default configuration of this package is dummy.
The whole shinken configuration must be created by the
administrator after installation.

Warning
=======

This package doesn't support the upgrade from the official
shinken package on Debian Wheezy (which embeds Shinken version 0.6.5).
To be honest, I have not even tested.

Build the package on Debian Wheezy
==================================

To build the package on Debian Wheezy, you can run these commands in a shell:

::

  build_depends='build-essential devscripts fakeroot debhelper quilt python-setuptools'
  apt-get install --no-install-recommends --yes git $build_depends
  
  git clone https://github.com/flaf/shinken-package.git
  cd shinken-package/shinken
  
  ./debian/rules populate_workingdir
  debuild -us -uc && echo 'All is OK!'


