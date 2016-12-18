cropfaces |License MIT|
==========================

http://python-packaging.readthedocs.io/en/latest/index.html


|PyPI version|

.. |PyPI version| image:: https://badge.fury.io/py/cropfaces.svg
   :target: https://badge.fury.io/py/cropfaces


Librería Python: Recorta imágenes dejando las caras para adaptarse a una escala concreta.

Parámetros de entrada:
Scale: Escala (obligado)
Input: Imagen de entrada (obligado)
Output: Imagen salida (opcional)
Zoom: Enumerado (opcional). Valores:
AUTO
NEAR
MIDDLE
FAR


Posibles inconvenientes:
   No se detectan caras
   No hay forma de adaptar la imagen a la escala.
   Se detectan caras muy pequeñas.
   Se detectan múltiples caras, unas muy grandes y otras claramente más pequeñas.

   Si no se detectan caras, se escoge la mayor parte central que se adapte a la escala

   Si no se adapta a la escala, se crea una imagen alternativa que sí se adapte.

   Si sólo se detectan caras pequeñas, se puede optar por varias estrategias:
Cuadrar la mayor parte considerando las caras.
Cuadrar la mayor parte central sin considerar las caras.

   Si se detectan caras de diferentes tamaños, se puede optar por varias estrategias:
Intentar cuadrar todas las caras
Cuadrar sólo las caras grandes


Algoritmo básico de crop una imagen:
StartX
StartY
EndX
EndY

Algoritmo para adaptar la mayor parte central a la escala:
scale: Escala buscada: width/height
Width y Height de la imagen
Width_imagen / scale <= Height_imagen
Height_imagen * scale <= Width_imagen
   

Algoritmo para crear una imagen alternativa que sí se adapte a la escala:
   Colocar la imagen sobre otra imagen de fondo.
    Resaltar la imagen con algún sombreado.
    La imagen de fondo es la propia imagen pero más grande y difuminada (Blur)




Getting started with the library
--------------------------------

| To use the library, you first need to install it.

::

    pip install text2img
    #python -c "import sys; import svgmanager; svgmanager.SvgManager.generate(sys.argv)"
    #python -c "import sys; from text2img import svgmanager; svgmanager.SvgManager.generate(sys.argv)"
    python -c "import sys; from text2img import SvgManager; SvgManager.generate(sys.argv)"
    python -c "import sys; from text2img import SvgManager; SvgManager.generate(sys.argv)" /home/jmramoss/almacen/ORLAS/text2img/text2img/base2.svd
    python -c "import sys; import svgmanager; svgmanager.SvgManager.generate(sys.argv)" /home/jmramoss/almacen/ORLAS/text2img/text2img/base.svd /home/jmramoss/almacen/ORLAS/text2img/text2img/themes.svd /home/jmramoss/text2img_output/clips
    sudo pip install --upgrade text2img

Every resource exposes the following **methods**:

-  list()
-  search()
-  get()
-  create()
-  update()
-  delete()

To use each resource you will need to create an instance of them,
passing the client as parameter in the constructor.

**Note:** at the moment not all the methods and not all the resources
have been implemented.

Here you can find a couple of examples, but for the complete
documentation you can have a look at the official website
https://developer.toshl.com/docs/

For me
~~~~~~

::

    git init
    git remote add origin https://github.com/tuaplicacionpropia/cropfaces.git
    git pull origin master

    git status
    git add .
    git rm file2delete
    git commit -m "commit message"
    git push origin master
    python setup.py register sdist upload


Accounts
~~~~~~~~

::

    from toshl.client import ToshlClient, Account

    client = ToshlClient('xxx-xxxxx-xxx-xxxxxx-xxxxxx-xxx-xxxxxx')
    account = Account(client)

    # list all accounts
    account.list()

    # search for a specific account
    account.search('Test Account')

Categories
~~~~~~~~~~

::

    from toshl.client import ToshlClient, Category

    client = ToshlClient('xxx-xxxxx-xxx-xxxxxx-xxxxxx-xxx-xxxxxx')
    category = Category(client)

    # list all categories
    category.list()

    # search for a specific category
    category.search('Test Category')

Entries
~~~~~~~

::

    from toshl.client import ToshlClient, Entry

    client = ToshlClient('xxx-xxxxx-xxx-xxxxxx-xxxxxx-xxx-xxxxxx')
    entry = Entry(client)

    # create an Entry
    json_payload = {
        'amount': -123.68,
        'currency': {
            'code': 'GBP'
        },
        'date': '2016-04-07',
        'account': 'abcd1234',
        'category': 'category-001'
    }

    response = entry.create(json_payload)

Copyright Note
--------------

| **cropfaces** and its logos, design, text, graphics, and other files, and
  the selection arrangement and organization thereof, are owned by
  http://tuaplicacionpropia.com.
| This is a 3rd party code and I’m not affiliated nor I work for cropfaces.

.. |License MIT| image:: https://go-shields.herokuapp.com/license-MIT-blue.png

