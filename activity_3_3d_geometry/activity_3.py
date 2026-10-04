import math
import random

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def distance_to(self, other):
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def subtract(self, other):
        return Point3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Point3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def octant(self):
        # Points on a coordinate plane are assigned to octant 0.
        if self.x == 0 or self.y == 0 or self.z == 0:
            return 0

        x_positive = self.x > 0
        y_positive = self.y > 0
        z_positive = self.z > 0

        # Standard sign-based octant numbering:
        # I:(+,+,+), II:(-,+,+), III:(-,-,+), IV:(+,-,+),
        # V:(+,+,-), VI:(-,+,-), VII:(-,-,-), VIII:(+,-,-)
        signs = (x_positive, y_positive, z_positive)
        mapping = {
            (True, True, True): 1,
            (False, True, True): 2,
            (False, False, True): 3,
            (True, False, True): 4,
            (True, True, False): 5,
            (False, True, False): 6,
            (False, False, False): 7,
            (True, False, False): 8,
        }
        return mapping[signs]

class Sphere3D:
    def __init__(self, center: Point3D, radius: float):
        self.center = center
        self.radius = radius

    def contains_point(self, p):
        return self.center.distance_to(p) <= self.radius

    def intersects_sphere(self, other):
        # Equivalent to dist <= r1+r2, written without sqrt for efficiency.
        dx = self.center.x - other.center.x
        dy = self.center.y - other.center.y
        dz = self.center.z - other.center.z
        dist_sq = dx * dx + dy * dy + dz * dz
        return dist_sq <= (self.radius + other.radius) ** 2

class AABB:
    def __init__(self, min_pt: Point3D, max_pt: Point3D):
        self.min_pt = min_pt
        self.max_pt = max_pt

    def intersects(self, other):
        return (
            self.min_pt.x <= other.max_pt.x and
            self.max_pt.x >= other.min_pt.x and
            self.min_pt.y <= other.max_pt.y and
            self.max_pt.y >= other.min_pt.y and
            self.min_pt.z <= other.max_pt.z and
            self.max_pt.z >= other.min_pt.z
        )

def example_3():
    p = Point3D(2, -1, 7)
    q = Point3D(1, -3, 5)
    return p.distance_to(q)

def example_5():
    # x²+y²+z²+4x-6y+2z+6=0
    # (x+2)² + (y-3)² + (z+1)² = 8
    center = Point3D(-2, 3, -1)
    radius = math.sqrt(8)
    return center, radius

def random_point():
    return Point3D(
        random.uniform(-100, 100),
        random.uniform(-100, 100),
        random.uniform(-100, 100)
    )

def make_random_sphere():
    return Sphere3D(random_point(), random.uniform(2, 15))

def make_aabb(center, half_size):
    return AABB(
        Point3D(center.x-half_size, center.y-half_size, center.z-half_size),
        Point3D(center.x+half_size, center.y+half_size, center.z+half_size)
    )

if __name__ == "__main__":
    print("=== Activity 3 Verification ===")

    d = example_3()
    print(f"Distance P(2,-1,7) to Q(1,-3,5): {d:.3f}")

    center, radius = example_5()
    print(
        f"Sphere center: ({center.x}, {center.y}, {center.z}), "
        f"radius: {radius:.3f}"
    )

    objects = [make_random_sphere() for _ in range(100)]
    sphere_collisions = 0

    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if objects[i].intersects_sphere(objects[j]):
                sphere_collisions += 1

    boxes = []
    for s in objects:
        boxes.append(make_aabb(s.center, s.radius))

    aabb_collisions = 0
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if boxes[i].intersects(boxes[j]):
                aabb_collisions += 1

    print(f"Sphere broad-phase intersections: {sphere_collisions}")
    print(f"AABB broad-phase intersections: {aabb_collisions}")
    print("Expected Example 3 result: 3.0")
    print("Expected Example 5 radius: sqrt(8) = 2.828")
