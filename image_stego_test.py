import unittest
import image_stego
from PIL import Image

def pixilify(image):
  """
  "Pixilifies" an image, turning it into a 2D array of tuples for the pixels.
  :author: Alec
  :param Image image: the image to pixilify.
  :return: the pixilified image as [[(int,int,int),(int,int,int),...,(int,int,int)]...]
  """
  loaded_image = image.load()
  width, height = image.size
  pixilified = []
  for x in range(width):
    column = []
    for y in range(height):
      rgba = loaded_image[x,y]
      column.append((rgba[0], rgba[1], rgba[2]))
    pixilified.append(column)
  return pixilified

class TestMethods(unittest.TestCase):
    def test_compute_distance_1(self):
        color1 = (0,0,0)
        color2 = (0,0,2)
        actual = image_stego.compute_distance(color1, color2)
        expected = 2
        self.assertEqual(actual, expected)

    def test_find_closest_color_1(self):
        color_dict = {
            (0xFF,0xFF,0xFF) : 1,
            (0xFF,0xFF,0xFE) : 1,
            (0xFF,0xFF,0x00) : 1,
            (0x00,0x00,0x00) : 1,
            (0xEE,0xDD,0xFF) : 1,
            (0xAA,0xAA,0xAA) : 1,
            (0xFE,0xFE,0xFF) : 1,
            (0xFD,0xFD,0x01) : 1,
            (0x0F,0x0F,0x10) : 1,
            (0x10,0x10,0x10) : 1,
        }
        color = (0xFF, 0xFF, 0xFF)
        actual = image_stego.find_closest_color(color_dict, color)
        expected = (0xFF, 0xFF, 0xFE)
        self.assertEqual(actual, expected)

    def test_get_close_color_count_1(self):
        color_dict = {
            (0x0F, 0x10, 0x10) : 1,
            (0x10, 0x10, 0x10) : 1,
            (0x10, 0x11, 0x10) : 1,
            (0x10, 0x10, 0x11) : 1,
            (0x00, 0x00, 0x00) : 2,
            (0x11, 0x10, 0x10) : 2
        }
        color = (0x10, 0x10, 0x10)
        actual = len(image_stego.get_close_colors(color_dict, color))
        expected = 4
        self.assertEqual(actual, expected)

    def test_bit_string_to_bytes_1(self):
        bits = "01110100011001010111001101110100"
        actual = image_stego.bit_string_to_bytes(bits)
        expected = b'test'
        self.assertEqual(actual, expected)
    
    def test_bit_string_to_bytes_2(self):
        bits = "011101000110010101110011011101"
        actual = image_stego.bit_string_to_bytes(bits)
        expected = b'test'
        self.assertEqual(actual, expected)
    
    def test_bytes_to_bit_string_1(self):
        bytes = b'test'
        actual = image_stego.bytes_to_bit_string(bytes)
        expected = "01110100011001010111001101110100"
        self.assertEqual(actual, expected)

    def test_rotate_image1(self):
        black_top_right = Image.open("./images/100x100quarter_black_top_right.png")
        actual = pixilify(image_stego.rotate_image(black_top_right, 90))
        expected = pixilify(Image.open("./images/100x100quarter_black_top_left.png"))
        self.assertEqual(actual, expected)

    def test_rotate_image2(self):
        black_top_right = Image.open("./images/100x100quarter_black_top_right.png")
        actual = pixilify(image_stego.rotate_image(black_top_right, 180))
        expected = pixilify(Image.open("./images/100x100quarter_black_bottom_left.png"))
        self.assertEqual(actual, expected)

    def test_rotate_image3(self):
        black_top_right = Image.open("./images/100x100quarter_black_top_right.png")
        actual = pixilify(image_stego.rotate_image(black_top_right, 270))
        expected = pixilify(Image.open("./images/100x100quarter_black_bottom_right.png"))
        self.assertEqual(actual, expected)

    def test_mirror_image1(self):
        black_top_right = Image.open("./images/100x100quarter_black_top_right.png")
        actual = pixilify(image_stego.mirror_image(black_top_right))
        expected = pixilify(Image.open("./images/100x100quarter_black_top_left.png"))
        self.assertEqual(actual, expected)

    def test_extract_common_colors_1(self):
        color_dict = {
            (0xFF,0xFF,0xFF) : 10,
            (0xFF,0xFF,0xFE) : 9,
            (0xFF,0xFF,0x00) : 8,
            (0x00,0x00,0x00) : 7,
            (0xEE,0xDD,0xFF) : 6,
            (0xAA,0xAA,0xAA) : 5,
            (0xFE,0xFE,0xFF) : 4,
            (0xFD,0xFD,0x01) : 3,
            (0x0F,0x0F,0x10) : 2,
            (0x10,0x10,0x10) : 1,
        }
        actual = image_stego.extract_common_colors(color_dict, 5)
        expected = {
            (0xFF,0xFF,0xFF) : 10,
            (0xFF,0xFF,0xFE) : 9,
            (0xFF,0xFF,0x00) : 8,
            (0x00,0x00,0x00) : 7,
            (0xEE,0xDD,0xFF) : 6,
        }
        self.assertEqual(actual, expected)

    def test_extract_common_colors_2(self):
        color_dict = {
            (0xFF,0xFF,0xFF) : 10,
            (0xFF,0xFF,0xFE) : 9,
            (0xFF,0xFF,0x00) : 8,
            (0x00,0x00,0x00) : 7,
            (0xEE,0xDD,0xFF) : 6,
            (0xAA,0xAA,0xAA) : 5,
            (0xFE,0xFE,0xFF) : 4,
            (0xFD,0xFD,0x01) : 3,
            (0x0F,0x0F,0x10) : 2,
            (0x10,0x10,0x10) : 1,
        }
        actual = image_stego.extract_common_colors(color_dict, 10)
        expected = {
            (0xFF,0xFF,0xFF) : 10,
            (0xFF,0xFF,0xFE) : 9,
            (0xFF,0xFF,0x00) : 8,
            (0x00,0x00,0x00) : 7,
            (0xEE,0xDD,0xFF) : 6,
            (0xAA,0xAA,0xAA) : 5,
            (0xFE,0xFE,0xFF) : 4,
            (0xFD,0xFD,0x01) : 3,
            (0x0F,0x0F,0x10) : 2,
            (0x10,0x10,0x10) : 1,
        }
        self.assertEqual(actual, expected)

    def test_extract_common_colors_3(self):
        color_dict = {
            (0xFF,0xFF,0xFF) : 10,
            (0xFF,0xFF,0xFE) : 9,
            (0xFF,0xFF,0x00) : 8,
            (0x00,0x00,0x00) : 7,
            (0xEE,0xDD,0xFF) : 6,
            (0xAA,0xAA,0xAA) : 5,
            (0xFE,0xFE,0xFF) : 4,
            (0xFD,0xFD,0x01) : 3,
            (0x0F,0x0F,0x10) : 2,
            (0x10,0x10,0x10) : 1,
        }
        actual = image_stego.extract_common_colors(color_dict, 15)
        expected = {
            (0xFF,0xFF,0xFF) : 10,
            (0xFF,0xFF,0xFE) : 9,
            (0xFF,0xFF,0x00) : 8,
            (0x00,0x00,0x00) : 7,
            (0xEE,0xDD,0xFF) : 6,
            (0xAA,0xAA,0xAA) : 5,
            (0xFE,0xFE,0xFF) : 4,
            (0xFD,0xFD,0x01) : 3,
            (0x0F,0x0F,0x10) : 2,
            (0x10,0x10,0x10) : 1,
        }
        self.assertEqual(actual, expected)

    def test_extract_colors_50x50white(self):
        image = Image.open("./images/50x50white.png")
        actual = image_stego.extract_colors(image)
        expected = {(0xFF,0xFF,0xFF) : 2500}
        self.assertEqual(actual,expected)

    def test_extract_colors_100x100_quarter_black(self):
        image = Image.open("./images/100x100quarter_black_top_right.png")
        actual = image_stego.extract_colors(image)
        expected = {(0x00,0x00,0x00) : 2500,
                    (0xFF,0xFF,0xFF) : 7500}
        self.assertEqual(actual,expected)
    
    def test_write_binary(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
        ])
        actual = pixilify(image_stego.write_binary(image, b'ABCD', (0,0,0), True, True, True, False))
        # ABCD is 41 42 43 44 is 0100 0001 0100 0010 0100 0011 0100 0100 is 010 000 010 100 | 001 001 000 011 | 010 001 00

        expected = [
            [(0,1,0),(0,0,1),(0,1,0),(0,0,0)],
            [(0,0,0),(0,0,1),(0,0,1),(0,0,0)],
            [(0,1,0),(0,0,0),(0,0,0),(0,0,0)],
            [(1,0,0),(0,1,1),(0,0,0),(0,0,0)],
        ]
        self.assertEqual(actual, expected)

    def test_write_binary_2(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0xFF,0xFF,0xFF),(0xAA,0xAA,0xAA),(0xFF,0xFF,0xFF),(0xFF,0xFF,0xFF),
            (0xAA,0xAA,0xAA),(0xAA,0xAA,0xAA),(0xAA,0xAA,0xAA),(0xAA,0xAA,0xAA),
            (0xFF,0xFF,0xFF),(0xFF,0xFF,0xFF),(0xAA,0xAA,0xAA),(0xAA,0xAA,0xAA),
            (0xAA,0xAA,0xAA),(0xAA,0xAA,0xAA),(0xAA,0xAA,0xAA),(0xAA,0xAA,0xAA),
        ])
        actual = pixilify(image_stego.write_binary(image, b'ABCD', (0xAA,0xAA,0xAA), True, True, True, False))
        # ABCD is 41 42 43 44 is 0100 0001 0100 0010 0100 0011 0100 0100 is 010 | 000 010 100 001 | 001 000 | 011 010 001 00

        expected = [
            [(0xFF,0xFF,0xFF),(0xAA,0xAA,0xAA),(0xFF,0xFF,0xFF),(0xAA,0xAB,0xAB)],
            [(0xAA,0xAB,0xAA),(0xAA,0xAB,0xAA),(0xFF,0xFF,0xFF),(0xAA,0xAB,0xAA)],
            [(0xFF,0xFF,0xFF),(0xAB,0xAA,0xAA),(0xAA,0xAA,0xAB),(0xAA,0xAA,0xAB)],
            [(0xFF,0xFF,0xFF),(0xAA,0xAA,0xAB),(0xAA,0xAA,0xAA),(0xAA,0xAA,0xAA)],
        ]
        self.assertEqual(actual, expected)

    def test_extract_binary(self):
        # ABCD is 41 42 43 44 is 0100 0001 0100 0010 0100 0011 0100 0100 is 010 000 010 100 | 001 001 000 011 | 010 001 00
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,1,0),(0,0,0),(0,1,0),(1,0,0),
            (0,0,1),(0,0,1),(0,0,0),(0,1,1),
            (0,1,0),(0,0,1),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
        ])
        actual = image_stego.extract_binary(image, (0,0,0), True, True, True, False)

        expected = b'ABCD\x00\x00'
        self.assertEqual(actual, expected)

    def test_extract_binary2(self):
        # ABCD is 41 42 43 44 is 0100 0001 0100 0010 0100 0011 0100 0100 is 010 000 010 100 | 001 001 000 011 | 010 001 00
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0xFF,0xFF,0xFF),(0xAA,0xAB,0xAA),(0xFF,0xFF,0xFF),(0xFF,0xFF,0xFF),
            (0xAA,0xAA,0xAA),(0xAA,0xAB,0xAA),(0xAB,0xAA,0xAA),(0xAA,0xAA,0xAB),
            (0xFF,0xFF,0xFF),(0xFF,0xFF,0xFF),(0xAA,0xAA,0xAB),(0xAA,0xAA,0xAA),
            (0xAA,0xAB,0xAB),(0xAA,0xAB,0xAA),(0xAA,0xAA,0xAB),(0xAA,0xAA,0xAA),
        ])
        actual = image_stego.extract_binary(image, (0xAA,0xAA,0xAA), True, True, True, False)

        expected = b'ABCD\x00'
        self.assertEqual(actual, expected)

    def test_to_direction_1(self):
        image = Image.open("./images/100x100quarter_black_top_left.png")
        direction_info = (False, True, False)
        actual = pixilify(image_stego.to_direction(image, direction_info))
        expected = pixilify(Image.open("./images/100x100quarter_black_top_right.png"))
        self.assertEqual(actual, expected)
    
    def test_to_direction_2(self):
        image = Image.open("./images/100x100quarter_black_top_left.png")
        direction_info = (False, False, False)
        actual = pixilify(image_stego.to_direction(image, direction_info))
        expected = pixilify(Image.open("./images/100x100quarter_black_bottom_right.png"))
        self.assertEqual(actual, expected)
    
    def test_to_direction_3(self):
        image = Image.open("./images/100x100quarter_black_top_left.png")
        direction_info = (True, True, True)
        actual = pixilify(image_stego.to_direction(image, direction_info))
        expected = pixilify(Image.open("./images/100x100quarter_black_top_left.png"))
        self.assertEqual(actual, expected)

        
    def test_is_top_heavy_1(self):
        data = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),]
        
        BASE_COLOR = (0,0,0)
        
        actual = image_stego.is_top_heavy(data,BASE_COLOR)
        expected = False

        self.assertEqual(actual,expected)

    def test_is_top_heavy_2(self):
        data = [(1,1,1),(1,1,1),(1,1,1),(1,1,1),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),]
        
        BASE_COLOR = (0,0,0)
        
        actual = image_stego.is_top_heavy(data,BASE_COLOR)
        expected = True

        self.assertEqual(actual,expected)

    def test_is_top_heavy_3(self):
        data = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (1,1,1),(1,1,1),(1,1,1),(1,1,1),]
        
        BASE_COLOR = (0,0,0)
        
        actual = image_stego.is_top_heavy(data,BASE_COLOR)
        expected = False

        self.assertEqual(actual,expected)
        
    def test_is_mirrored_1(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,0,1),(0,0,1),(0,0,0),(1,8,0),
            (0,0,0),(0,0,0),(0,0,1),(0,1,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
        ])
        expected = True
        actual = image_stego.is_mirrored(image,(0,0,0),5)

        self.assertEqual(actual,expected) 

    def test_is_mirrored_1(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,0,1),(0,0,1),(0,0,0),(1,8,0),
            (1,0,0),(0,1,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
        ])
        expected = False
        actual = image_stego.is_mirrored(image,(0,0,0),5)

        self.assertEqual(actual,expected) 

    def test_is_mirrored_1(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,0,1),(0,0,1),(0,0,0),(1,8,0),
            (1,0,0),(0,1,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
        ])
        expected = False
        actual = image_stego.is_mirrored(image,(0,0,0),5)

        self.assertEqual(actual,expected) 

    def test_is_mirrored_1(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,0,1),(0,0,1),(0,0,0),(1,8,0),
            (1,0,0),(0,1,0),(0,1,0),(1,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
        ])
        expected = True
        actual = image_stego.is_mirrored(image,(0,0,0),5)

        self.assertEqual(actual,expected)

    def test_guess_direction_info_1(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,0,1),(0,0,1),(0,1,0),(1,1,0),
            (1,0,0),(0,1,0),(0,1,0),(1,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,1,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
        ])
        expected_horiz_first = True
        expected_top_to_bottom = True
        
        actual_horiz_first, actual_top_to_bottom, _ = image_stego.guess_direction_info(image)

        self.assertEqual(actual_top_to_bottom, expected_top_to_bottom)
        self.assertEqual(actual_horiz_first, expected_horiz_first)

    def test_guess_direction_info_2(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,0,1),(0,0,1),(0,0,1),(0,0,0),
            (1,0,0),(0,0,1),(0,1,0),(0,0,0),
            (1,0,0),(0,0,1),(0,1,0),(0,0,0),
            (0,1,0),(0,0,1),(0,0,1),(0,0,0),
        ])
        expected_horiz_first = False
        expected_left_to_right = True
        
        actual_horiz_first, _, actual_left_to_right = image_stego.guess_direction_info(image)

        self.assertEqual(actual_left_to_right, expected_left_to_right)
        self.assertEqual(actual_horiz_first, expected_horiz_first)
    
    def test_guess_direction_info_3(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (0,0,0),(0,0,0),(0,0,0),(0,0,0),
            (1,0,0),(1,0,0),(1,0,0),(0,1,0),
            (0,0,1),(0,0,1),(0,0,1),(0,0,1),
        ])
        expected_horiz_first = True
        expected_top_to_bottom = False
        
        actual_horiz_first, actual_top_to_bottom, _ = image_stego.guess_direction_info(image)

        self.assertEqual(actual_top_to_bottom, expected_top_to_bottom)
        self.assertEqual(actual_horiz_first, expected_horiz_first)

    def test_guess_direction_info_4(self):
        image = Image.new("RGB",(4,4))
        image.putdata([
            (0,0,0),(0,1,0),(0,0,1),(0,1,0),
            (0,0,0),(0,1,0),(0,0,1),(0,0,0),
            (0,0,0),(0,1,0),(0,1,0),(0,1,0),
            (0,0,0),(0,1,0),(0,1,0),(0,1,0),
        ])
        expected_horiz_first = False
        expected_left_to_right = False
        
        actual_horiz_first, _, actual_left_to_right = image_stego.guess_direction_info(image)

        self.assertEqual(actual_left_to_right, expected_left_to_right)
        self.assertEqual(actual_horiz_first, expected_horiz_first)
if __name__ == '__main__':
    unittest.main()