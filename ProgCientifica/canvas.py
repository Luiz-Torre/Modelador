from PyQt5 import QtOpenGL
from PyQt5.QtCore import QPointF
from OpenGL.GL import *
from hetool.he.hecontroller import HeController
from hetool.he.hemodel import HeModel
from hetool.geometry.segments.line import Line
from hetool.geometry.point import Point
from hetool.compgeom.tesselation import Tesselation

class Canvas(QtOpenGL.QGLWidget):
    def __init__(self):
        super().__init__()
        self._model = None
        self._hmodel = HeModel()
        self._controller = HeController(self._hmodel)
        self.m_w, self.m_h = 0, 0
        self.m_L, self.m_R, self.m_B, self.m_T = -1000.0, 1000.0, -1000.0, 1000.0
        self.list = None
        self.m_buttonPressed = False
        self.moved = False
        self.m_pt0, self.m_pt1 = QPointF(0.0, 0.0), QPointF(0.0, 0.0)

    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
        self.list = glGenLists(1)

    def _set_projection(self):
        glViewport(0, 0, self.m_w, self.m_h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def resizeGL(self, _width, _height):
        self.m_w, self.m_h = _width, _height
        bounds = self._model.getBoundBox() if self._model and not self._model.isEmpty() else None
        if bounds:
            self.m_L, self.m_R, self.m_B, self.m_T = bounds
            self.scaleWorldWindow(1.1)
        else:
            self.scaleWorldWindow(1.0)
        self._set_projection()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glCallList(self.list)
        glDeleteLists(self.list, 1)
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        
        # Desenhe a linha temporária apenas se o botão do mouse estiver pressionado
        if self.m_buttonPressed:
            pt0_U, pt1_U = map(self.convertPtCoordsToUniverse, [self.m_pt0, self.m_pt1])
            glColor3f(1.0, 1.0, 0.0)
            glBegin(GL_LINES)
            glVertex2f(pt0_U.x(), pt0_U.y())
            glVertex2f(pt1_U.x(), pt1_U.y())
            glEnd()

        if not self._hmodel.isEmpty():
            for pat in self._hmodel.getPatches():
                triangs = Tesselation.tessellate(pat.getPoints())
                glColor3f(1.0, 0.0, 1.0)
                for tri in triangs:
                    glBegin(GL_TRIANGLES)
                    for point in tri:
                        glVertex2d(point.getX(), point.getY())
                    glEnd()
            
            glColor3f(0.0, 0.0, 1.0)
            for curves in self._hmodel.getSegments():
                p1, p2 = curves.getPointsToDraw()
                glBegin(GL_LINES)
                glVertex2f(p1.getX(), p1.getY())
                glVertex2f(p2.getX(), p2.getY())
                glEnd()
            
        glEndList()

    def setModel(self, model):
        self._model = model

    def fitWorldToViewport(self):
        if not self._hmodel.isEmpty():
            self.m_L, self.m_R, self.m_B, self.m_T = self._model.getBoundBox()
            self.scaleWorldWindow(1.10)
            self._set_projection()
            self.update()


    def scaleWorldWindow(self, _scaleFac):
        cx, cy = (self.m_L + self.m_R) / 2.0, (self.m_B + self.m_T) / 2.0
        vpr = self.m_h / self.m_w
        sizex = (self.m_R - self.m_L) * _scaleFac
        sizey = (self.m_T - self.m_B) * _scaleFac
        sizex = max(sizex, sizey / vpr)
        sizey = sizex * vpr
        self.m_L, self.m_R = cx - (sizex * 0.5), cx + (sizex * 0.5)
        self.m_B, self.m_T = cy - (sizey * 0.5), cy + (sizey * 0.5)
        self._set_projection()

    def convertPtCoordsToUniverse(self, _pt):
        dX, dY = self.m_R - self.m_L, self.m_T - self.m_B
        mX, mY = _pt.x() * dX / self.m_w, (self.m_h - _pt.y()) * dY / self.m_h
        return QPointF(self.m_L + mX, self.m_B + mY)

    def mousePressEvent(self, event):
        self.m_buttonPressed = True
        self.m_pt0 = event.pos()

    def mouseMoveEvent(self, event):
        if self.m_buttonPressed:
            self.moved = True
            self.m_pt1 = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if not self.moved:
            return
        
        pt0_U, pt1_U = map(self.convertPtCoordsToUniverse, [self.m_pt0, self.m_pt1])

        segment = Line(Point(pt0_U.x(), pt0_U.y()), Point(pt1_U.x(), pt1_U.y()))
        
        self._controller.insertSegment(segment, 0.1)
        
        self.m_buttonPressed, self.moved = False, False
        self.m_pt0, self.m_pt1 = QPointF(0.0, 0.0), QPointF(0.0, 0.0)
        
        self.update()
