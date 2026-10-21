import unittest
from PIL import Image, ImageDraw
from p10_extension_art import source_rectangles


class SourcePartitionTests(unittest.TestCase):
    def test_effect_can_cross_regular_grid_without_being_cut(self):
        image=Image.new('RGBA',(400,500))
        draw=ImageDraw.Draw(image)
        for row in range(5):
            for col in range(4):
                draw.rectangle((col*100+35,row*100+20,col*100+65,row*100+75),fill=(80,100,150,255))
            # Third pose's effect reaches into the fourth nominal cell,
            # but ends before that pose's body. Preserve the whole effect.
            draw.rectangle((260,row*100+35,318,row*100+55),fill=(250,150,20,255))
        frames=source_rectangles(image)
        self.assertEqual(len(frames),20)
        coverage=Image.new('L',image.size)
        for i,f in enumerate(frames):
            x,y,w,h=f['rect']
            self.assertGreater(w,0);self.assertGreater(h,0)
            if i%4==2:self.assertGreaterEqual(x+w,319)
            if i%4==3:self.assertGreaterEqual(x,319)
            # All source pixels belong to exactly one full rectangle.
            region=coverage.crop((x,y,x+w,y+h))
            self.assertIsNone(region.getbbox())
            coverage.paste(255,(x,y,x+w,y+h))
        self.assertEqual(coverage.getextrema(),(255,255))

    def test_empty_pose_is_rejected(self):
        with self.assertRaises(ValueError):source_rectangles(Image.new('RGBA',(400,500)))

    def test_faint_fringe_does_not_make_gutter_cut_solid_tail(self):
        image=Image.new('RGBA',(400,500))
        draw=ImageDraw.Draw(image)
        for row in range(5):
            for col in range(4):
                draw.rectangle((col*100+25,row*100+20,col*100+75,row*100+75),fill=(80,100,150,255))
            # A long opaque tail crosses every candidate gutter except x>=120.
            # More faint pixels there must not outweigh the actual anatomy.
            draw.rectangle((70,row*100+40,119,row*100+41),fill=(80,100,150,255))
            draw.rectangle((120,row*100,124,row*100+99),fill=(150,80,200,8))
        frames=source_rectangles(image)
        for row in range(5):
            self.assertGreaterEqual(frames[row*4]['rect'][2],120)


if __name__=='__main__':unittest.main()
