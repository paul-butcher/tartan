=====
Usage
=====

Command Line Interface
----------------------

You can use the CLI to generate tartan images.  The image will be
written in PNG format to STDOUT.

.. code-block:: sh

    $ tartan "N32 DN20 LR14 N10 DG10 W14" > tartan.png

.. image:: images/tartan.png

By default, the generated image will be 512x512 pixels. You can specify height and width.

.. code-block:: sh

    $ tartan "B24 W4 B24 R2 K24 G24 W2" --width 100 > tartan_100x512.png

.. image:: images/tartan_100x512.png

.. code-block:: sh

    $ tartan "LB24 DB4 G24 R2 Lr24 G24 W2" --height 100 > tartan_512x100.png

.. image:: images/tartan_100x512.png

.. code-block:: sh

    $ tartan "DY20 W4 DR6" --width 100 --height 100 > tartan_100x100.png

.. image:: images/tartan_100x100.png

Python Interface
----------------

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

