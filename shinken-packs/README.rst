=================================================
Source package of shinken-packs for Debian Wheezy
=================================================

Description
===========

This is a (personal) package which provides:

1. **Some "host" templates** in .cfg files.
For more explanations you can see
the **/usr/share/shinken-packs/sp.example.cfg** file.

2. The **sp_notify** command to send mails etc.
See **sp_notify --help** for more explanations.

3. The **sp_merge_conf** command to merge several files
(with a specific syntax) in only one shinken configuration
file. It is useful when you export some piece of shinken
configuration with Puppet to create a valid shinken
configuration file. See the source of the command
(in Python) for more explanations (sorry it's not user
friendly).


Warning
=======

This package depends on 2 unofficial packages :

1. the `wmi-cli`__ package;
2. and the `shinken`__ package.

__ https://github.com/flaf/wmic
__ https://github.com/flaf/shinken-package


Build the .deb package on Debian Wheezy
=======================================

To build the .deb package on Debian Wheezy, you can run these commands in a shell:

.. code:: sh

  # Creation of the working directory.
  git clone https://github.com/flaf/shinken-packs.git
  cd shinken-packs/shinken-packs/
  
  # Installation of the build-dependencies
  BUILD_DEPENDS='<see the debian/control file>'
  apt-get install --no-install-recommends --yes build-essential $BUILD_DEPENDS

  # Building of the package.
  ./debian/rules create_deb

And the package is in the parent directory:

.. code:: sh

  ls -l ..

