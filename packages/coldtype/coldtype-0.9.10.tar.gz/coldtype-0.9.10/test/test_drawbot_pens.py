import unittest
from coldtype.drawbot import *

from PIL import Image
import drawBot as db
import imagehash
import contextlib

from coldtype.runon.runon import Runon

renders = Path("test/renders/drawbot")
renders.mkdir(parents=True, exist_ok=True)

def hash_img(path):
    if path.exists():
        return (
            imagehash.colorhash(Image.open(path)), 
            imagehash.average_hash(Image.open(path)))
    else:
        return -1

@contextlib.contextmanager
def test_image(test:unittest.TestCase, path, rect=Rect(300, 300)):
    img = (renders / path)
    hash_before = hash_img(img)
    if img.exists():
        img.unlink()
    test.assertEqual(img.exists(), False)

    with new_drawing(rect, save_to=img) as (i, r):
        yield (i, r)
        test.assertEqual(r.w, db.width())
        test.assertEqual(r.h, db.height())
    
    hash_after = hash_img(img)
    #test.assertEqual(hash_after, hash_before)
    #test.assertEqual(img.exists(), True)

class TestDrawbotPens(unittest.TestCase):
    def test_gs_pen(self):
        with test_image(self, "test_gs_pen.png") as (i, r):
            rr = Rect(0, 0, 100, 100)
            dp = (P()
                .declare(c:=75)
                .m(rr.pne).bxc(rr.ps, "se", c)
                .bxc(rr.pnw, "sw", c).cp()
                .align(r)
                .scale(1.2)
                .f(hsl(0.3, a=0.1))
                .s(hsl(0.9))
                .sw(5)
                | dbdraw)
            self.assertEqual(len(dp.v.value), 4)
            self.assertEqual(type(dp), P)

    def test_distribute_on_path(self):
        mistral = Font.Find("MistralD.otf")

        with test_image(self, "test_distribute.png", Rect(1000, 1000)) as (i, r):
            s = (StyledString("Hello", Style(mistral, 300))
                .pens()
                .f(hsl(0.3, s=1))
                .align(r)
                .chain(dbdraw))
            
            with db.savedState():
                db.fill(None)
                db.stroke(0)
                db.strokeWidth(1)
                db.rect(*s.ambit())
        
            circle = P().oval(r.inset(200)).reverse().rotate(0)
            s2 = (s.copy()
                .zero()
                .distribute_on_path(circle)
                .chain(dbdraw))
            
            self.assertEqual(s.f(), s2.f())


if __name__ == "__main__":
    unittest.main()