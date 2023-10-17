class MyPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class MyCurve:
    def __init__(self, p1=None, p2=None):
        self.p1 = p1
        self.p2 = p2

class Bezier:
    def __init__(self, p1=None, p2=None, ctrl=None):
        self.p1 = p1
        self.p2 = p2
        self.ctrl = ctrl
        
class MyModel:
    def __init__(self):
        self.m_verts = []
        self.m_curves = []
        self.m_beziers = []


    def setVerts(self, x, y):
        self.m_verts.append(MyPoint(x, y))

    def setCurve(self, x1, y1, x2, y2):
        self.m_curves.append(MyCurve(MyPoint(x1, y1), MyPoint(x2, y2)))

    def getCurves(self):
        return self.m_curves

    def getVerts(self):
        return self.m_verts

    def isEmpty(self):
        return len(self.m_verts) == 0 and len(self.m_curves) == 0
    
    def setBezier(self, x1, y1, x2, y2, ctrl_x, ctrl_y):
        self.m_beziers.append(Bezier(MyPoint(x1, y1), MyPoint(x2, y2), MyPoint(ctrl_x, ctrl_y)))

    def getBeziers(self):
        return self.m_beziers

    def getBoundBox(self):
        xs = [v.x for v in self.m_verts] + [c.p1.x for c in self.m_curves] + [c.p2.x for c in self.m_curves]
        ys = [v.y for v in self.m_verts] + [c.p1.y for c in self.m_curves] + [c.p2.y for c in self.m_curves]

        # Verifica se xs e ys não estão vazios antes de retornar min e max
        if xs and ys:
            return min(xs), max(xs), min(ys), max(ys)
        else:
            # Retornar caixa delimitadora padrão se xs ou ys estiverem vazios
            return 0.0, 10.0, 0.0, 10.0

