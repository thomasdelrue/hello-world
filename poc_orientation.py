from vector2 import *

v1 = Vector2(0, -10)
#v1.normalize()

v2 = Vector2(10, 0)
#v2.normalize()

v3 = Vector2(-10, 10)
#v3.normalize()


def angle(va, vb):
    dot = va.x * vb.x + va.y * vb.y
    print('\ncalculating angle')
    print('-----------------')
    print('va={} vb={} dot={}'.format(va, vb, dot))
    vam = va.get_magnitude()
    vbm = vb.get_magnitude()
    res = dot / vam / vbm
    print('|va|={} |vb|={} cos alpha={}'.format(vam, vbm, res))
    res = math.acos(res) * 180 / math.pi
    print('angle?={}'.format(res))
    

print(v1)
print(v2)
print(v3)

angle(v1, v2)
angle(v1, v3)


