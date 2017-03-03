#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import cv2
import sys
import os

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

https://github.com/opencv/opencv/tree/master/data
http://alereimondo.no-ip.org/OpenCV/34/
https://www.leightley.com/face-and-eye-detection-with-python-static-image/


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
    self.width = self.right - self.left
    self.height = self.bottom - self.top

  def __repr__(self):
    return '(' + str(self.left) + ', ' + str(self.top) + ', ' + str(self.right) + ', ' + str(self.bottom) + ')'

  def __str__(self):
    return self.__str__()

class CropFaces:
  
  def __init__(self, zoom='AUTO', output=None):
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/haarcascade_frontalface_alt.xml")

    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/haarcascade_eye.xml)
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/haarcascade_frontalface_alt.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/haarcascade_frontalface_alt2.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/haarcascade_frontalface_default.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/haarcascade_profileface.xml")

    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/haarcascade_upperbody.xml")

    self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/haarcascade_frontalface_alt_tree.xml")

    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/Downloads/frontalFace10/haarcascade_frontalface_alt_tree.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/Downloads/frontalFace10/HS.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/Downloads/frontalFace10/parojosG.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/Downloads/frontalFace10/parojos.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/Downloads/frontalFace10/Mouth.xml")

    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/2haarcascade_frontalface_alt.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/2haarcascade_frontalface_alt2.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/2haarcascade_frontalface_alt_tree.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/2haarcascade_frontalface_default.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/HS.xml")
    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/almacen/ORLAS/cropfaces/cropfaces/parojosG.xml")


    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/Downloads/frontalFace10/frontalEyes35x16.xml")


    #self.cascade = cv2.CascadeClassifier("/home/jmramoss/Downloads/frontalFace10/ojoD.xml")

    self.cv_scaleFactor = 1.1
    self.cv_minNeighbors = 3
    self.cv_flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    self.cv_size = (20, 20)

  def cropBox (self, imagePath, box):
    original = Image.open(imagePath)
    cropped = original.crop((box.left, box.top, box.right, box.bottom))
    cropped.save("img1.png", "PNG")

  def crop (self, image):
    box = self.detectBoxFaces(image)
    if box is not None:
      self.cropBox(image, box)
  
  def detectBoxFaces (self, image):
    result = None
    faces = self.detectFaces(image)
    result = self.mergeFaces(image, faces)
    return result

  def detectFaces(self, imagePath):
    result = list()

    img = cv2.imread(imagePath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = cv2.calcHist(gray, 3)
    #rects = self.cascade.detectMultiScale(gray, self.cv_scaleFactor, self.cv_minNeighbors, self.cv_flags, self.cv_size)
    #rects = self.cascade.detectMultiScale(gray, self.cv_scaleFactor, self.cv_minNeighbors, self.cv_flags)
    rects = self.cascade.detectMultiScale(gray, self.cv_scaleFactor, self.cv_minNeighbors, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))
    #rects = self.cascade.detectMultiScale(gray, self.cv_scaleFactor, self.cv_minNeighbors)
    #rects = self.cascade.detectMultiScale(img)
    rects = [] if len(rects) == 0 else rects
    print rects
    #rects[:, 2:] += rects[:, :2]
    #print rects
    for x1, y1, x2, y2 in rects:
      box = BoxArea(x1, y1, x1+x2, y1+y2)
      cv2.rectangle(img, (box.left, box.top), (box.right, box.bottom), (127, 255, 0), 2)
      result.append(box)

    newName = os.path.basename(imagePath) + '.detected.jpg'
    cv2.imwrite(newName, img);
    print result
    
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

  def cropOrla (self, image, mode='AUTO'):
    box = self.detectBoxFaces(image)
    if box is not None:
      self.cropBoxOrla(image, box, mode)

  def cropBoxOrla (self, imagePath, box, mode='AUTO'):
    original = Image.open(imagePath)
    '''
    fHead = 1.10#1.10#1.10
    fSide = 1.10#1.10#1.10
    fBottom = 3.3#2.90#2.10
    '''
    '''
    fHead = 1.10
    fSide = 1.10
    fBottom = 1.8
    '''
    '''
    fHead = 0.7
    fSide = 1.10
    fBottom = 2.3
    '''
    '''
    fHead = 0.6
    fSide = 1.10
    fBottom = 2.5
    '''
    '''
    fHead = 0.6
    fSide = 1.10
    fBottom = 2.7
    '''
    fHead = 0.6
    fSide = 1.10
    fBottom = 2.6
    if mode == 'NEAR':
      fHead = 0.6
      fSide = 1.10
      fBottom = 2.3
    if mode == 'MIDDLE':
      fHead = 0.6
      fSide = 1.10
      fBottom = 2.6
    if mode == 'FAR':
      fHead = 0.6
      fSide = 1.10
      fBottom = 2.9
    width = box.width
    height = box.height

    newbox = BoxArea(box.left - int(fSide*width), box.top - int(fHead*height), box.right + int(fSide*width), box.bottom + int(fBottom*height))
    cropped = original.crop((newbox.left, newbox.top, newbox.right, newbox.bottom))
    #cropped.save("img1.png", "PNG")
    #cropped.save("img1.jpg", "jpeg")
    #cropped.save("img1.jpg", "jpeg", quality=100, optimize=True, progressive=True)
    newFileFolder = os.path.dirname(imagePath)
    oldFileName = os.path.basename(imagePath)
    extIdx = oldFileName.rindex('.')
    fileExt = oldFileName[extIdx+1:]
    newFileName = oldFileName[0:extIdx] + '_orla' + '.' + fileExt
    newFile = os.path.join(newFileFolder, newFileName)
    cropped.save(newFile, "jpeg", quality=100, optimize=True, progressive=True)

  def cropOrlas (self, folder, prefix):
    files = os.listdir(folder)
    modes = ['NEAR', 'MIDDLE', 'FAR']
    modeIdx = 0
    for filename in files:
      if filename.startswith(prefix):
        fullpath = os.path.join(folder, filename)
        mode = modes[modeIdx%len(modes)]
        self.cropOrla(fullpath, mode)
        modeIdx += 1


#python -c "import sys; import svgmanager; svgmanager.SvgManager.generate(sys.argv)"
#./cropfaces.py /home/jmramoss/almacen/ORLAS/orlas_infantiles/infantil_5b teacher
if __name__ == '__main__':
  cropFaces = CropFaces()
  #cropFaces.cropOrla(sys.argv[1])
  cropFaces.cropOrlas(sys.argv[1], sys.argv[2])

