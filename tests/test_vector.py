import unittest

from svg2png import vector


# vector.base
# =====================================
class TestA1_Transform(unittest.TestCase):
    def test_a(self):
        # constructor
        # -----------
        translate, scale = (10, 20), (1.5, 2.0)
        t = vector.Transform(translate=translate, scale=scale)
        self.assertTrue(t.translate == (10, 20) and t.scale == (1.5, 2.0))


class TestA2_Point(unittest.TestCase):
    def test_a(self):
        # constructor
        # -----------

        # valid constructor 1
        p = vector.Point((10, 20))
        self.assertTrue(p.x == 10 and p.y == 20)

    def test_b(self):
        # special operations
        # ------------------

        # __getitem__
        a = vector.Point((10, 20))
        self.assertTrue(a[0] == 10 and a[1] == 20)
        self.assertRaises(IndexError, a.__getitem__, 2)

        # __iter__
        a = vector.Point((10, 20))
        self.assertTrue(tuple(a) == (10, 20))

        # __eq__
        a = vector.Point((10, 20))
        self.assertTrue(a == (10, 20))

        # __add__ and __sub__
        a = vector.Point((10, 20))
        b = vector.Point((30, 50))
        c = a + b
        self.assertTrue(c.x == 40 and c.y == 70)
        c = a - b
        self.assertTrue(c.x == -20 and c.y == -30)

        # __iadd__ and __isub__
        a = vector.Point((10, 20))
        b = vector.Point((30, 50))
        a += b
        self.assertTrue(a.x == 40 and a.y == 70)
        a -= b
        self.assertTrue(a.x == 10 and a.y == 20)

    def test_c(self):
        # operations
        # ----------

        # transform
        a = vector.Point((10, 20))
        b = a.transform(vector.Transform((1, 2), (2, 3)))
        self.assertTrue(b.x == 21 and b.y == 62)


class TestA3_BBox(unittest.TestCase):
    def test_a(self):
        # constructor
        # -----------

        # valid constructor 1
        b = vector.BBox((10, 20, 30, 40))
        self.assertTrue((b.left, b.top) == (10, 20))
        self.assertTrue((b.width, b.height) == (30, 40))

        # valid constructor 2
        b = vector.BBox((30, 20))
        self.assertTrue((b.left, b.top) == (0, 0))
        self.assertTrue((b.width, b.height) == (30, 20))

    def test_b(self):
        # special operations
        # ------------------

        # indexing
        b = vector.BBox((10, 20, 30, 40))
        self.assertTrue(b[0] == 10 and b[1] == 20)
        self.assertTrue(b[2] == 30 and b[3] == 40)
        self.assertRaises(IndexError, b.__getitem__, 4)

        # iterable
        b = vector.BBox((10, 20, 30, 40))
        self.assertTrue(tuple(b) == (10, 20, 30, 40))

    def test_c(self):
        # operations
        # ----------

        # properties
        b = vector.BBox((10, 20, 30, 40))
        self.assertTrue(b.offset == (10, 20))
        self.assertTrue(b.size == (30, 40))
        self.assertTrue(b.center == (25, 40))

        # sub_bbox test -> centers are same
        b = vector.BBox((10, 20, 30, 40))
        c = b.get_sub_bbox((0.5, 0.5), "MM")
        self.assertTrue(c.center == b.center)


# vector.draw
# =====================================
class TestB1_RenderSurface(unittest.TestCase):
    def test_a(self):
        # constructor
        # -----------
        r = vector.RenderSurface((100, 200))
        r = vector.RenderSurface([100, 200])
        self.assertTrue(r.image.size == (100, 200))
        self.assertTrue(r.cmap("#f0f0f0") == "#f0f0f0")


class TestB2_1_DrawablePath(unittest.TestCase):
    def test_a(self):
        # constructor
        # -----------
        d = vector.DrawablePath("e12")

    def test_b(self):
        # operations
        # ----------

        # absolute system
        d = vector.DrawablePath("e12")
        d.moveto((10, 20), rel=False)
        self.assertTrue(d.current_pos == (10, 20))
        self.assertTrue(len(d.subpaths[-1]) == 1)
        self.assertTrue(len(d.subpaths) == 1)

        d.lineto((20, 30), rel=False)
        self.assertTrue(d.current_pos == (20, 30))
        self.assertTrue(len(d.subpaths[-1]) == 2)
        self.assertTrue(len(d.subpaths) == 1)

        d.closepath()
        self.assertTrue(d.current_pos == (10, 20))
        self.assertTrue(len(d.subpaths[-1]) == 3)
        self.assertTrue(len(d.subpaths) == 1)

        # relative system
        d.moveto((10, 20), rel=True)
        self.assertTrue(d.current_pos == (20, 40))
        self.assertTrue(len(d.subpaths[-1]) == 1)
        self.assertTrue(len(d.subpaths) == 2)

        d.lineto((10, 20), rel=True)
        self.assertTrue(d.current_pos == (30, 60))
        self.assertTrue(len(d.subpaths[-1]) == 2)
        self.assertTrue(len(d.subpaths) == 2)

        d.closepath()
        self.assertTrue(d.current_pos == (20, 40))
        self.assertTrue(len(d.subpaths[-1]) == 3)
        self.assertTrue(len(d.subpaths) == 2)


class TestB3_DrawableObjectStore(unittest.TestCase):
    def test_a(self):
        # constructor
        # -----------
        o = vector.DrawableObjectStore((100, 200))

    def test_b(self):
        # special operations
        # ------------------
        # __len__, __iter__, __getitem__
        o = vector.DrawableObjectStore((100, 200))
        o.append("a1", vector.DrawablePath("a1"))
        o.append("a2", vector.DrawablePath("a2"))
        self.assertTrue(len(o) == len(list(o)) == 2)
        self.assertTrue(o[0].elem_id == "a1")

    def test_c(self):
        # operation
        # ---------

        # create, create_draft, get_draft
        o = vector.DrawableObjectStore((100, 100))
        a1 = vector.DrawablePath("a1")
        a2 = vector.DrawablePath("a2")
        a3 = vector.DrawablePath("a3")

        o.append("a1", a1, render=True)
        o.append("a2", a2, render=False)
        o.append("d3", a3, render=False)
        o.append("a3", a3, render=True)

        self.assertTrue([i.elem_id for i in o] == ["a1", "a3"])
        self.assertTrue(o.get("d3").elem_id == "a3")
        self.assertRaises(KeyError, o.get, "a4")

        # clear
        o.clear()
        self.assertTrue(len(o) == 0)
        self.assertRaises(KeyError, o.get, "a1")


def main():
    unittest.main()


if __name__ == "__main__":
    main()