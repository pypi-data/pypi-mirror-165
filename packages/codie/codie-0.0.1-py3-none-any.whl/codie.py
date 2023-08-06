import math
import rhino3dm as rh
import shapely.geometry as sh

class Parser:
    def __init__(self, type="geoJson"):
        self._type = type

class Point3d:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
    
    @property
    def X(self):
        return self._x

    @X.setter
    def X(self, val):
        self._x = val
    
    @property
    def Y(self):
        return self._y

    @Y.setter
    def Y(self, val):
        self._y = val
    
    @property
    def Z(self):
        return self._z

    @Z.setter
    def Z(self, val):
        self._z = val

    def DistanceTo(self, other):
        return math.sqrt((other.X-self.X)**2 + (other.Y-self.Y)**2 + (other.Z-self.Z)**2)
    
    def copy(self):
        return Point3d(self.X, self.Y, self.Z)

    def translate(self, v):
        self.X += v.X
        self.Y += v.Y
        self.Z += v.Z
        return self
    
    def project(self, plane):
        origin = plane.Origin
        normal = Vector3d(*plane.Normal.get_geo())
        normal.unitize()

        v = Vector3d(*self.get_geo()) - Vector3d(*origin.get_geo()) 
        dist = v.dot(normal)

        normal *= dist

        projected_point = Vector3d(*self.get_geo()) - normal
        
        return Point3d(*projected_point.get_geo())

    def get_3dm_geo(self):
        return rh.Point3d(self.X, self.Y, self.Z)
    
    def get_shapely_geo(self):
        return sh.Point(self.X, self.Y)
    
    def __str__(self):
        return "Point3d: [{}, {}, {}]".format(self._x, self._y, self._z)

    def get_geo(self):
        return (self.X, self.Y, self.Z)
    
    def GetJson(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point3d",
                "coordinates": [self._x, self._y, self._z]
            },
            "properties": {
                "name": "Default"
            }
        }

class Vector3d:

    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
    
    @property
    def X(self):
        return self._x

    @X.setter
    def X(self, val):
        self._x = val
    
    @property
    def Y(self):
        return self._y

    @Y.setter
    def Y(self, val):
        self._y = val
    
    @property
    def Z(self):
        return self._z

    @Z.setter
    def Z(self, val):
        self._z = val

    def get_amp(self):
        return math.sqrt(self.X**2 + self.Y**2 + self.Z**2)
    
    def unitize(self):
        a = self.get_amp()
        self.X /= a
        self.Y /= a
        self.Z /= a
        return self
    
    def get_pt(self):
        return Point3d(self.X, self.Y, self.Z)
    
    def cross(self, other):
        x = self.Y * other.Z - self.Z * other.Y
        y = self.Z * other.X - self.X * other.Z
        z = self.X * other.Y - self.Y * other.X
        return Vector3d(x, y, z)

    def dot(self, other):
        # cp = self.get_amp() * other.get_amp() * math.cos(self.angle_to(other))
        cp = self.X * other.X + self.Y * other.Y + self.Z * other.Z
        return cp

    def angle_to(self, other):
        dot = self.dot(other)
        mult = (self.get_amp() * other.get_amp())
        # ensure value does not go out of valid range [-1, 1] due to floating point error
        if mult < 0.01:
            return 0.0
        v = min(1.0, max(-1.0, dot / mult))

        angle = math.acos(v)

        # angle = math.acos((self.X * other.X + self.Y * other.Y) /
        #                   (math.sqrt(self.X**2 + self.Y**2) * math.sqrt(other.X**2 + other.Y**2)))

        return angle

    def rotate(self, normal, theta):
        pt = self.get_pt().get_3dm_geo().Transform(rh.Transform.Rotation(theta, normal.get_3dm_geo(), rh.Point3d(0,0,0)))
        return Vector3d(pt.X, pt.Y, pt.Z)

    def __imul__(self, amt):
        self.X *= amt
        self.Y *= amt
        self.Z *= amt
        return self

    def __mul__(self, amt):
        x = self.X * amt
        y = self.Y * amt
        z = self.Z * amt
        return Vector3d(x, y, z)

    def __add__(self, other):
        x = self.X + other.X
        y = self.Y + other.Y
        z = self.Z + other.Z
        return Vector3d(x, y, z)

    def __sub__(self, other):
        x = self.X - other.X
        y = self.Y - other.Y
        z = self.Z - other.Z
        return Vector3d(x, y, z)
    
    def get_3dm_geo(self):
        return rh.Vector3d(self.X, self.Y, self.Z)

    def get_geo(self):
        return (self.X, self.Y, self.Z)

    def __str__(self):
        return "Vector3d: [{}, {}, {}]".format(self._x, self._y, self._z)


class Plane:

    def __init__(self, origin, normal, x_axis):
        self._origin = origin
        self._normal = normal
        self._x_axis = x_axis
    
    @property
    def Origin(self):
        return self._origin

    @Origin.setter
    def Origin(self, val):
        self._origin = val
    
    @property
    def Normal(self):
        return self._normal

    @Normal.setter
    def Normal(self, val):
        self._normal = val
    
    def get_x_axis(self):

        return self._x_axis

        x1 = self.Normal.X
        y1 = self.Normal.Y
        z1 = self.Normal.Z

        x2 = 1
        y2 = 2
        if z1 == 0:
            z2 = 0
        else:
            z2 = (-x1 * x2 - y1 * y2) / z1

        return Vector3d(x2, y2, z2)

    def get_local_pt(self, point):
        x_axis = self.get_x_axis()

        x_norm = Vector3d(*x_axis.get_geo())
        x_norm.unitize()

        n_norm = Vector3d(*self.Normal.get_geo())
        n_norm.unitize()

        diff = Vector3d(*point.get_geo()) - Vector3d(*self.Origin.get_geo())

        x = diff.dot(x_norm)
        y = diff.dot(n_norm.cross(x_norm))

        return (x, y)

class Line:

    def __init__(self, p1, p2):
        self._pts = [p1, p2]
    
    @property
    def StartPoint(self):
        return self._pts[0]

    @StartPoint.setter
    def StartPoint(self, pt):
        self._pts = [pt, self._pts[1]]
    
    @property
    def EndPoint(self):
        return self._pts[1]

    @EndPoint.setter
    def EndPoint(self, pt):
        self._pts = [self._pts[0], pt]
    
    @property
    def Length(self):
        return self.StartPoint.DistanceTo(self.EndPoint)

    def PointAt(self, t):
        pt = self.get_3dm_geo().PointAt(t)
        return Point3d(pt.X, pt.Y, pt.Z)
    
    def copy(self):
        return Line(self._pts[0].copy(), self._pts[1].copy())

    def translate(self, v):
        [pt.translate(v) for pt in self._pts]
        return self

    def Offset(self, plane, amount):
        v = self.get_vector()
        v = v.rotate(plane.Normal, math.pi/2)
        v.unitize()
        v *= amount
        self.translate(v)
        return self
    
    def intersect(self, other, tol=0.01, finite_segments=False):
        return rh.Intersection.LineLine(self.get_3dm_geo(), other.get_3dm_geo(), tol, finite_segments)
    
    def get_vector(self):
        p1 = self._pts[0]
        p2 = self._pts[1]
        return Vector3d(p2.X-p1.X, p2.Y-p1.Y, p2.Z-p1.Z)
    
    def get_3dm_geo(self):
        return rh.Line(self._pts[0].get_3dm_geo(), self._pts[1].get_3dm_geo())
    
    def GetJson(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Line",
                "coordinates": [
                    [self.StartPoint.X, self.StartPoint.Y, self.StartPoint.Z],
                    [self.EndPoint.X, self.EndPoint.Y, self.EndPoint.Z]
                ]
            },
            "properties": {
                "name": "Default"
            }
        }


class Vert:

    def __init__(self, pt, old_pt, dir, param, offset):
        self.pt = pt
        self.old_pt = old_pt
        self.link = None
        self.param = param
        self.next = None
        self.offset = offset
        self.dir = dir

    def get_offset(self):
        return self.offset

    def set_pt(self, pt):
        self.pt = pt

    def get_pt(self):
        return self.pt

    def get_old_pt(self):
        return self.old_pt

    def set_link(self, other):
        self.link = other

    def has_link(self):
        if self.link is not None:
            return True
        else:
            return False

    def get_link(self):
        return self.link

    def set_next(self, other):
        self.next = other

    def get_next(self):
        return self.next

class BoundingBox:
    def __init__(self, pts):
        self._pts = pts
    
    @property
    def Min(self):
        
        xs = [pt.X for pt in self._pts]
        ys = [pt.Y for pt in self._pts]
        zs = [pt.Z for pt in self._pts]

        return Point3d(min(xs), min(ys), min(zs))
    
    @property
    def Max(self):
        
        xs = [pt.X for pt in self._pts]
        ys = [pt.Y for pt in self._pts]
        zs = [pt.Z for pt in self._pts]

        return Point3d(max(xs), max(ys), max(zs))


class Polyline:
    def __init__(self, pts):
        self._pts = pts
    
    def ToArray(self):
        return self._pts

    def is_clockwise(self):
        return self.to_3dm_curve().ClosedCurveOrientation() == rh.CurveOrientation.Clockwise
    
    def reverse(self):
        self._pts.reverse()

    def get_plane(self):
        pts = self.ToArray()

        # https://web.ma.utexas.edu/users/m408m/Display12-5-4.shtml#:~:text=The%20normal%20to%20the%20plane,%C3%97(s%E2%88%92b).
        b = Vector3d(*pts[1].get_geo())
        r = Vector3d(*pts[2].get_geo())
        s = Vector3d(*pts[0].get_geo())
        normal = (r - b).cross(s - b)

        x_axis = s - b

        return Plane(s, normal, x_axis)

    def get_projected(self):

        plane = self.get_plane()

        return Polyline([pt.project(plane) for pt in self._pts])

    def get_local(self):

        plane = self.get_plane()

        return Polyline([Point3d(*plane.get_local_pt(pt), 0.0) for pt in self._pts])

    def get_shapely_polygon(self):

        local_poly = self.get_projected().get_local()

        return sh.Polygon([(pt.X, pt.Y) for pt in local_poly._pts])

    # def get_2d_geo(self):
        # return ()

    def to_3dm_curve(self):
        return rh.Curve.CreateControlPointCurve([pt.get_3dm_geo() for pt in self._pts], 1)

    def get_centroid(self):
        c = self.get_shapely_polygon().centroid
        return Point3d(c.x, c.y, self._pts[0].Z)

    def contains(self, point):

        plane = self.get_plane()

        local_poly = self.get_projected().get_local()
        local_point = plane.get_local_pt(point.project(plane))

        return (self.get_shapely_polygon().contains(sh.Point(local_point)), local_poly, Point3d(*local_point, 0.0))
    

    def GetBoundingBox(self, plane):
        pts = self._pts
        return BoundingBox(pts)


    def Offset(self, _plane, _distances, _tol):

        pts = self._pts[:-1]

        if type(_distances) != list:
            amounts = [_distances] * len(pts)
        else:
            amounts = _distances

        verts = []

        for i in range(len(pts)):
            p1 = pts[i-1]
            p2 = pts[i]
            p3 = pts[(i+1) % len(pts)]

            # CREATE NEW POINT FROM INTERSECTION OF OFFSET LINES
            ls = [Line(p1, p2), Line(p2, p3)]
            ls_t = [l.copy().Offset(_plane, amounts[i+j-1]) for j, l in enumerate(ls)]
            inter = ls_t[0].intersect(ls_t[1], 0.01, False)
            
            new_pt = ls_t[0].PointAt(inter[1])
            dir = ls[1].get_vector()
            v = Vert(new_pt, p2, dir, None, amounts[i])
            verts.append(v)

        # SET NEXT POINT IN VERT CHAIN
        for i in range(len(verts)):
            verts[i].set_next(verts[(i+1) % len(verts)])

        # FIND SELF-INTERSECTIONS

        # CREATE LISTS TO STORE VERTS GENERATED FROM SELF-INTERSECTIONS
        bin = []
        for i in range(len(verts)):
            bin.append([])

        new_verts = []

        # ITERATE OVER EVERY PAIR OF VERTS
        for i in range(len(verts)):
            for j in range(i, len(verts)):
                # SKIP IF TWO VERTS ARE WITHIN A SPACE OF EACH OTHER (SKIP CONSECUTIVE LINES)
                if i == j or i == (j - 1) % len(verts) or i == (j + 1) % len(verts):
                    continue

                p1 = verts[i]
                p2 = verts[(i+1) % len(verts)]
                p3 = verts[j]
                p4 = verts[(j+1) % len(verts)]

                # CREATE LINES FOR EDGES
                l1 = Line(p1.get_pt(), p2.get_pt())
                l2 = Line(p3.get_pt(), p4.get_pt())

                inter = l1.intersect(l2, 0.01, True)

                # IF SELF-INTERSECTION IS FOUND...
                if inter[0]:
                    v1 = Vert(l1.PointAt(inter[1]), p3.get_old_pt(
                    ), p3.dir, inter[1], p3.get_offset())
                    v2 = Vert(l2.PointAt(inter[2]), p1.get_old_pt(
                    ), p1.dir, inter[2], p1.get_offset())

                    new_verts.append(v1)
                    new_verts.append(v2)

                    v1.set_link(v2)
                    v2.set_link(v1)

                    # ADD NEW VERTS TO BINS
                    bin[i].append([v1, inter[1]])
                    bin[j].append([v2, inter[2]])

        # SORT BINS BY PARAMETERS
        for b in bin:
            b.sort(key=lambda x: x[1])

        for i in range(len(verts)):
            if len(bin[i]) == 0:
                continue

            # (RE)SET NEXT VERT FOR NEW VERTS
            set = [verts[i]] + [b[0]
                                for b in bin[i]] + [verts[(i+1) % len(verts)]]
            for j in range(len(set)-1):
                set[j].set_next(set[j+1])

        verts += new_verts

        # REBUILD POLYLINES BASED ON SELF-INTERSECTIONS

        new_polys = []

        while len(verts) > 0:
            poly = []

            v0 = verts.pop(0)
            v1 = v0
            poly.append(v1)

            c = 0
            while c < 100:
                v2 = v1.get_next()
                if v2 is v0:
                    break
                poly.append(v2)

                if v2.has_link():
                    v1 = v2.get_link()
                else:
                    v1 = v2

                c += 1

                if v1 in verts:
                    verts.remove(v1)

            if c > 100:
                break

            new_polys.append(poly)

        # SKIP NEW POLYS WITH REVERSED DIRECTION (CHECK 1)
        polys_out = []
        for poly in new_polys:
            pts = [v.get_pt() for v in poly]
            pl = Polyline(pts + [pts[0]])
            if pl.is_clockwise() != self.is_clockwise():
                continue
            polys_out.append(poly)

        # CLEAN POLYS (CHECK 2)
        # polys_cleaned = []
        # for poly in polys_out:
        #    c = 0
        #    b = True
        #    while b:
        #        b, new_poly = Polyline.clean_poly(poly)
        #        if len(new_poly) < 3:
        #            b = False
        #        poly = new_poly
        #
        #        if c > 100:
        #            break
        #        c += 1
        #
        #    if len(new_poly) < 3:
        #        continue
        #
        #    polys_cleaned.append(new_poly)

        polys_cleaned = polys_out

        # OUTPUT VERTS TO POLYLINE
        polys_final = []
        for poly in polys_cleaned:
            pts = [v.get_pt() for v in poly]
            polys_final.append(Polyline(pts + [pts[0].copy()]))
        
        return polys_final
    
    def GetJson(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[pt.X, pt.Y, pt.Z] for pt in self._pts]
                ]
            },
            "properties": {
                "name": "Default"
            }
        }




