import math

class Vector(object):
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

        
    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z )
        
            
    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z )
        
            
    def __mul__(self, factor):
        return Vector(
            self.x * factor,
            self.y * factor,
            self.z * factor)
            
            
    def __mod__(self, v):
        return Vector(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x)
        
            
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        
        return self
        
            
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        
        return self
        
            
    def __imul__(self, factor):
        self.x *= factor
        self.y *= factor
        self.z *= factor
        
        return self
        
        
    def __abs__(self):
        mag = self.x * self.x + self.y * self.y + self.z * self.z
        
        if mag == 1 or mag == 0:
            return mag
            
        return math.sqrt(mag)
            
            
    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)
        
        
    def unit(self):
        ret = Vector(self.x, self.y, self.z)
        mag = self.__abs__()
        ret.x = self.x/mag
        ret.y = self.y/mag
        ret.z = self.z/mag
        
        return ret
        
        
    def to_spherical(self):
        r = self.__abs__()
        
        if r == 0:
            return
        
        t = math.acos(self.z/r)
        a = math.atan2(self.y, self.x)
        
        self.x = r 
        self.y = t
        self.z = a
        
        
    def to_cartesian(self):
        x = self.x * math.cos(self.z) * math.sin(self.y)
        y = self.x * math.sin(self.z) * math.sin(self.y)
        z = self.x * math.cos(self.y)
        
        self.x = x
        self.y = y
        self.z = z
        
        
        
        
            
def main():
    #debug
    a = Vector(1,2,3)
    b = Vector(3,2,1)

    c = a+b
    d = a-b
    e = a*2

    print a
    print b
    print c
    print d
    print e

    print "iterative"

    print a
    a += b
    print a
    a -= b
    print a
    a *= 2
    print a
    
    print "magnitude"
    print "|{0}|={1}".format(b,abs(b))
    
    print "a={0}".format(a)
    print "test = a"
    test = a
    print "test={0}".format(test)
    
    print "Cross Product {0}%{1}".format(a,b)
    print a%b
    
    
if __name__ == "__main__":
    main()
