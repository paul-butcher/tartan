======
tartan
======


.. image:: https://img.shields.io/pypi/v/tartan.svg
        :target: https://pypi.python.org/pypi/tartan

.. image:: https://img.shields.io/travis/paul-butcher/tartan.svg
        :target: https://travis-ci.com/paul-butcher/tartan

.. image:: https://readthedocs.org/projects/tartan/badge/?version=latest
        :target: https://tartan.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Generates tartan images from threadcount definitions.


* Free software: MIT license
* Documentation: https://tartan.readthedocs.io.


Features
--------

* Command line interface to generate a PNG image from a threadcount.
* Function to generate a PIL image in memory.
* Generate images with your preferred size.

Usage
-----

Command Line Interface
^^^^^^^^^^^^^^^^^^^^^^

You can use the CLI to generate tartan images.  The image will be
written in PNG format to STDOUT.

.. code-block:: sh

    $ tartan "DY20 W4 DR6" > tartan.png

By default, the generated image will be 512x512 pixels. You can specify height and width.

.. code-block:: sh

    $ tartan "DY20 W4 DR6" --width 1024 > tartan_1024x512.png
    $ tartan "DY20 W4 DR6" --height 1024 > tartan_512x1024.png
    $ tartan "DY20 W4 DR6" --width 100 --height 100 > tartan_100x100.png

Python Interface
^^^^^^^^^^^^^^^^

Using the threadcount_to_image function, you can generate a
`PIL Image <https://pillow.readthedocs.io/en/stable/reference/Image.html>`_
to do with as you will.

.. code-block::

    from tartan import threadcount_to_image

    img = threadcount_to_image('T30 G14 Y2')

As with the CLI, above, you can specify a size.  This follows the PIL convention
of using a 2-tuple - `(width, height)`

.. code-block::

    img_100x200 = threadcount_to_image('T30 G14 Y2', (100,200))



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
