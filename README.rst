Package of Shinken 1.4.1 for Debian Wheezy
------------------------------------------

Description
^^^^^^^^^^^

This is a single and *minimalist* package for Debian Wheezy which embeds:

- Shinken 1.4.1 
- Pyro4 version 4.18
- and that's all!

The default configuration of this package is dummy.
The whole shinken configuration must be create by the
administrator after installation.

To build the package on Debian Wheezy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can run these commands in a shell:

::
  build_dependencies='build-essential debhelper quilt python python-setuptools'
  apt-get install --no-install-recommends --yes git $build_dependencies
  
  git clone https://github.com/flaf/shinken-package.git
  cd shinken-package/shinken
  
  ./debian/rules populate_workingdir
  dpkg-buildpackage -us -uc && echo 'All is OK!'

