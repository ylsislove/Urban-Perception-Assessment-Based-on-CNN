import math

class WebCoordSystemTransform(object):
    def __init__(self):
        self.pi = 3.14159265358979324
        self.a =  6378245.0
        self.ee = 0.00669342162296594323

    def outOfChina(self, lat, lon):
        if lon < 72.004 or lon > 137.8347:
            return True
        if lat < 0.8293 or lat > 55.8271:
            return True
        return False

    def transformLat(self, x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * self.pi) + 20.0 * math.sin(2.0 * x * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * self.pi) + 40.0 * math.sin(y / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * self.pi) + 320 * math.sin(y * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def transformLon(self, x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * self.pi) + 20.0 * math.sin(2.0 * x * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * self.pi) + 40.0 * math.sin(x / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * self.pi) + 300.0 * math.sin(x / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def wgs2gcj(self, wgLat, wgLon):
        if self.outOfChina(wgLat, wgLon):
            return wgLat, wgLon
        dLat = self.transformLat(wgLon - 105.0, wgLat - 35.0)
        dLon = self.transformLon(wgLon - 105.0, wgLat - 35.0)
        radLat = wgLat / 180.0 * self.pi
        magic = math.sin(radLat)
        magic = 1 - self.ee * magic * magic
        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtMagic) * self.pi)
        dLon = (dLon * 180.0) / (self.a / sqrtMagic * math.cos(radLat) * self.pi)
        mgLat = wgLat + dLat
        mgLon = wgLon + dLon
        return mgLat, mgLon

    def gcj2wgs(self, mglat, mglon):
        # 二分法
        glat, glon = self.wgs2gcj(mglat, mglon)
        dlat = glat - mglat
        dlon = glon - mglon
        wglat = mglat - dlat
        wglon = mglon - dlon
        return wglat, wglon

    def gcj2bd09(self, mglat, mglon):
        x, y = mglon, mglat 
        z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * self.pi)
        theta = math.atan2(y, x) + 0.000003 * math.cos(x * self.pi)
        bdlon = z * math.cos(theta) + 0.0065
        bdlat = z * math.sin(theta) + 0.006
        return bdlat, bdlon

    def bd092gcj(self, bdlat, bdlon):
        x = bdlon - 0.0065
        y = bdlat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.pi)
        mglon = z * math.cos(theta)
        mglat = z * math.sin(theta)
        return mglat, mglon

    def bd092wgs(self, bdlat, bdlon):
        mglat, mglon = self.bd092gcj(bdlat, bdlon)
        wglat, wglon = self.gcj2wgs(mglat, mglon)
        return wglat, wglon

    def wgs2bd09(self, wglat, wglon):
        mglat, mglon = self.wgs2gcj(wglat, wglon)
        bdlat, bdlon = self.gcj2bd09(mglat, mglon)
        return bdlat, bdlon
