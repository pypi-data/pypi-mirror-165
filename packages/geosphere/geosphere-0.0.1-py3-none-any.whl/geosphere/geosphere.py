from math import sin, cos, asin, acos, pi

"""
Longitude increases to the east, decreases to the west and lies in (-180, 180].
Latitude increases to the north, decreases to the south and lies in [-90, 90].
An angle of 1 degree at the center of the earth cuts out an arc 60 nm long.
A nautical mile is 6076.12 feet long.
One foot subtends an angle of 2.7429e-06 radians
Bearing and longitude are meaningless at the poles. 
There is no meaningful bearing from a point to its antipode.
"""

def safe(x):
    if x > 1.0:
        return 1.0
    if x < -1.0:
        return -1.0
    return x

def reduce(x):
    return (x + 180) % 360 - 180

def distance_bearing(lat1_deg, long1_deg, lat2_deg, long2_deg):
    """
    Return the distance in nautical miles and the bearing in degrees from the
    location given by the first lat-long pair to the location given by the
    second lat-long pair.  If the points are too close together the bearing
    is 0.  If the first point is at a pole, the bearing is 0 or 180, as
    appropriate.  If the points are too close to being antipodes the bearing
    is not defined and is returned as 0.
    """
    rad = pi/180
    long_diff = reduce(long2_deg*rad - long1_deg*rad)
    lat1, lat2 = lat1_deg*rad, lat2_deg*rad
    cos_dist = (cos(lat1) * cos(lat2) * cos(long_diff) + sin(lat1) * sin(lat2))
    dist = acos(cos_dist)
    if lat1_deg > 89.9: # North pole
        bearing = pi 
    elif lat1_deg < -89.9: # South pole
        bearing = 0
    elif dist < 1.0e-7 or dist > pi - 1.0e-7: # Same or antipodes
        bearing = 0
    else:
        cos_bearing = (
            (cos(lat1)*sin(lat2) - cos(long_diff)*sin(lat1)*cos(lat2)) / sin(dist))
        bearing = acos(safe(cos_bearing))
        # Reverse the bearing if needed.
        if sin(long_diff)*cos(lat1)*cos(lat2) < 0:
            bearing = 2*pi - bearing
    return 60.0*dist/rad, bearing/rad % 360

def destination(lat_degrees, long_degrees, distance_nm, bearing_degrees):
    """
    Return the latitude and longitude of the location reached by traveling
    distance_nm nautical miles along the great circle which passes through the
    location with given latitude and longitude, having the given bearing.
    """
    rad = pi / 180
    start_lat = lat_degrees * rad
    bearing = (bearing_degrees % 360) * rad
    distance = (distance_nm * rad) / 60
    assert 0 < distance < pi
    sin_lat = (cos(start_lat) * cos(bearing) * sin(distance) +
               sin(start_lat) * cos(distance))
    lat = asin(safe(sin_lat))
    cos_long = (-sin(start_lat)*cos(bearing)*sin(distance) +
                cos(start_lat)*cos(distance)) / cos(lat)
    long = acos(safe(cos_long))
    if bearing > pi:
        long = -long
    return lat / rad, reduce(long_degrees + long / rad)
    
def test(lat_deg, long_deg, distance_nm, bearing_deg):
    lat2, long2 = destination(lat_deg, long_deg, distance_nm, bearing_deg)
    distance, bearing = distance_bearing(lat_deg, long_deg, lat2, long2)
    print(distance_nm, distance)
    print(bearing_deg, bearing)

