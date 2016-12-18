#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import cv2

'''
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

'''

'''
http://fideloper.com/facial-detection
Install opencv:
  $ sudo apt-get update
  $ sudo apt-get install -y vim build-essential python-software-properties    # The Basics
  $ sudo apt-get install -y python-opencv python-numpy python-scipy        # OpenCV items

  $ wget http://eclecti.cc/files/2008/03/haarcascade_frontalface_alt.xml



'''

'''
zoom: AUTO, FAR, NEAR, MIDDLE
'''

class BoxArea:
  def __init__(self, left, top, right, bottom):
    self.left = left
    self.top = top
    self.right = right
    self.bottom = bottom

class CropFaces:
  def __init__(self, zoom='AUTO', output=None):
    self.image = image
    self.faces = list()
    self.selectedArea = None
    self.cascade = cv2.CascadeClassifier("/vagrant/detect/haarcascade_frontalface_alt.xml")
    self.cv_scaleFactor = 1.3
    self.cv_minNeighbors = 4
    self.cv_flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    self.cv_size = (20, 20)


  def cropBox (self, imagePath, box):
    original = Image.open(imagePath)
    cropped = original.crop((box.left, box.top, box.right, box.bottom))
    cropped.save("img1.png", "PNG")

  def crop (self, image):
    box = self.detectBoxFaces(image)
    self.cropBox(image, box)
  
  def detectBoxFaces (self, image):
    result = None
    faces = self.detectFaces(image)
    result = self.mergeFaces(image, faces)
    return result

  def detectFaces(imagePath):
    result = list()

    img = cv2.imread(imagePath)
    rects = self.cascade.detectMultiScale(img, self.cv_scaleFactor, self.cv_minNeighbors, self.cv_flags, self.cv_size)
    rects = [] if len(rects) == 0 else rects
    rects[:, 2:] += rects[:, :2]
    for x1, y1, x2, y2 in rects:
      box = BoxArea(x1, y1, x2, y2)
      result.append(box)
    
    return result

  def mergeFaces (self, imagePath, faces):
    result = None
    result = self.mergeAllFaces(imagePath, faces)
    return result

  def mergeAllFaces (self, imagePath, faces):
    result = None
    if len(faces) > 0:
      minLeft = None
      minTop = None
      maxRight = None
      maxBottom = None
      for face in faces:
        if minLeft is None or minLeft > face.left:
          minLeft = face.left
        if minTop is None or minTop > face.top:
          minTop = face.top
        if maxRight is None or maxRight < face.right:
          maxRight = face.right
        if maxBottom is None or maxBottom < face.bottom:
          maxBottom = face.bottom
      result = BoxArea(minLeft, minTop, maxRight, maxBottom)
    return result

#python -c "import sys; import svgmanager; svgmanager.SvgManager.generate(sys.argv)"
if __name__ == '__main__':
  cropFaces = CropFaces()
  cropFaces.crop(sys.argv)

