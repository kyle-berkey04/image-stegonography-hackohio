from PIL import Image
import math

def compute_distance(color1, color2):
  """
  Compute the distance between two colors.
  :author: Kyle
  :param (int, int, int) color1: The first color.
  :param (int, int, int) color2: The second color.
  :return: The distance between the vector spaces of the two colors.
  """
  
  # Squared differences
  red = (color1[0]-color2[0])**2
  blue = (color1[1]-color2[1])**2
  green = (color1[2]-color2[2])**2

  # distance
  return math.sqrt(red + blue + green)

def find_closest_color(color_dict, color):
  """
  Finds the closest color in the color dictionary to the given color.
  :author: Kyle
  :param {(int,int,int) : int} color_dict: The color dictionary.
  :param (int,int,int) color: The color to find the closest colors for.
  :return: The color tuple for the closest color in the color dictionary.
  """
  
  # greater than closest color
  min = compute_distance((0,0,0),(0xFF, 0xFF, 0xFF)) + 1

  closest_color = (-1, -1, -1)

  for key in color_dict.keys():
    # calculate distance
    distance = compute_distance(key, color)

    # check if closest
    if distance <=  min and distance != 0:
      min = distance
      closest_color = key

  return closest_color

def get_close_colors(color_dict, color):
  """
  Finds the colors in the dictionary close to the given color
  :author: Kavyan
  :param {(int,int,int) : int} color_dict: The color dictionary.
  :param (int,int,int) color: The color to find the closest colors for.
  :return: The count of colors close to that color.
  """
  
  # confidence for "close colors"
  EPSILON = math.sqrt(3)

  colors = set()

  for key in color_dict.keys():
    # calculate distance
    distance = compute_distance(key, color)

    # check if closest
    if distance <=  EPSILON and distance > 0:
      colors.add(key)

  return colors

def extract_common_colors(color_dict, count):
  """
  Extracts the top count colors from a color dictionary.
  :author: Kavyan, Alec
  :param {(int,int,int) : int} color_dict: The color dictionary to extract the colors from.
  :param int count: The number of colors to extract.
  :return: A dictionary of the RGB tuples to their counts, of size count or less.
  """

  top_colors = {}
  color_dict_copy = color_dict.copy()

  found = 0
  while found < count and found < len(color_dict):

    # Find max value in dictionary thats not in top_Colors
    max_color = max(color_dict_copy, key=color_dict_copy.get)
    max_color_val = color_dict_copy[max_color]

    # Add to top_Colors
    top_colors[max_color] = max_color_val
    
    # Remove from temp dict
    del color_dict_copy[max_color]

    found += 1
        
  return top_colors
  
def extract_colors(image):
  """
  Extracts the colors from an image file. 
  :author: Kavyan
  :param Image image: The image file.
  :return: A dictionary of the RGB tuples to their counts.
  """
  color_dict = {}
  width, height = image.size
  pixels = image.load()

  # Iterate over all pixels in image
  for i in range(width):
    for j in range(height):
      rgba = pixels[i,j]
      rgb = (rgba[0],rgba[1],rgba[2])

      # If the color is in color_dict, increment the count
      if rgb in color_dict:
        color_dict[rgb] = color_dict.get(rgb) + 1

      # else add the color of the pixel
      else:
        color_dict[rgb] = 1

  return color_dict

def rotate_image(image, degrees):
  """
  Rotates an image 0, 90°, 180°, or 270° counter-clockwise.
  :author: Kyle
  :param Image image: The image file.
  :param int degrees: The degrees to rotate it. Must be 0, 90, 180, or 270.
  :return: the rotated image
  """
  return image.rotate(degrees, expand=True)

def mirror_image(image):
  """
  Flips the image across the vertical.
  :author: Kyle
  :param Image image: The image file.
  :return: the flipped image
  """

  # Flip the image from left to right
  return image.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

def bit_string_to_bytes(bits):
  """
  Converts a string of bits to bytes.
  :author: Alec
  :param string bits: The bits to convert
  :return: the bytes that are encoded.
  """
  # pad bit string such that length is divisible by the # of bits in a byte
  BITS_IN_BYTE = 8
  bits = bits.ljust(math.ceil(len(bits) / BITS_IN_BYTE) * BITS_IN_BYTE, '0')
  byte_strings = [bits[i:i+BITS_IN_BYTE] for i in range(0, len(bits), BITS_IN_BYTE)]

  # convert bit string to bytes, return
  result = b''
  for byte_string in byte_strings:
    result += int(byte_string, 2).to_bytes(1, 'big')
  return result

def extract_binary(image, BASE_COLOR, red, green, blue, reversed):
  """
  Extracts the binary data from an image. The base color is the color in which
  the binary is encoded, and the last bit contains binary data. Reads from left
  to right, then top to bottom.
  :author: Alec
  :param Image image: The image file.
  :param (int, int, int) BASE_COLOR: The base color containing the data.
  :param bool red: whether red bit should be considered
  :param bool green: whether red bit should be considered
  :param bool blue: whether red bit should be considered
  :param bool reversed: whether rgb should actually be bgr
  :return: The binary data encoded as a bytes object, padded with 0s at the end.
  """

  # max distance between encrypted data and the base color
  CRYPT_DIST = math.sqrt(red + green + blue)

  width, height = image.size
  pixels = image.load()
  data = ""
  
  # iterate over pixels
  for y in range(height):
    for x in range(width):
      # determine if color is in range
      if compute_distance(BASE_COLOR, pixels[x, y]) <= CRYPT_DIST:
        # append r, g, and b bits in that order
        rgba = pixels[x, y]
        (r, g, b) = (rgba[0], rgba[1], rgba[2])
        if not reversed:
          if red: data += str(r & 1)
          if green: data += str(g & 1)
          if blue: data += str(b & 1)
        else:
          if blue: data += str(b & 1)
          if green: data += str(g & 1)
          if red: data += str(r & 1)

  data_bytes = bit_string_to_bytes(data)
  return data_bytes
  
def bytes_to_bit_string(bytes):
  """
  Converts bytes to a string of bits.
  :author: Alec
  :param Bytes bytes: The bytes to convert
  :return: the bytes as a bit string
  """
  data = ""
  BITS_IN_BYTE = 8
  for b in bytes:
    for bit_offset in range(BITS_IN_BYTE -1, -1, -1):
        bit = (b >> bit_offset) & 1
        data += str(bit)
  return data

def write_binary(image, bytes, BASE_COLOR, red, green, blue, reversed):
  """
  Writes the binary data to an image. The base color is the color in which
  the binary should be encoded, and the last bit should contain binary data. Reads from left
  to right, then top to bottom.
  :author: Alec
  :param Image image: The image file.
  :param Bytes bytes: The raw data to write.
  :param (int, int, int) BASE_COLOR: The base color to contain the data.
  :param bool red: whether red bit should contain bits
  :param bool green: whether green bit should contain bits
  :param bool blue: whether blue bit should contain bits
  :param bool reversed: whether rgb should be bgr
  :return: The updated image.
  """

  # extract info about image
  width, height = image.size
  pixels = image.load()
  
  # set up data variable to read from bytes
  data = bytes_to_bit_string(bytes)
  data_idx = 0

  # initialize new image object 
  new_image = Image.new(image.mode, image.size)
  
  # iterate over pixels
  new_pixels = []
  for y in range(height):
    for x in range(width):
      # determine if color is the base color
      rgba = pixels[x,y]
      (r, g, b) = (rgba[0], rgba[1], rgba[2])
      if BASE_COLOR == (r, g, b):
        if not reversed:
          if red and data_idx < len(data):
            r &= ~1
            r |= data[data_idx] == '1'
            data_idx += 1
          if green and data_idx < len(data):
            g &= ~1
            g |= data[data_idx] == '1'
            data_idx += 1
          if blue and data_idx < len(data):
            b &= ~1
            b |= data[data_idx] == '1'
            data_idx += 1
        else:
          if blue and data_idx < len(data):
            b &= ~1
            b |= data[data_idx] == '1'
            data_idx += 1
          if green and data_idx < len(data):
            g &= ~1
            g |= data[data_idx] == '1'
            data_idx += 1
          if red and data_idx < len(data):
            r &= ~1
            r |= data[data_idx] == '1'
            data_idx += 1

        pixels[x,y] = (r,g,b)
      new_pixels.append((r,g,b))
  
  new_image.putdata(new_pixels)        
  return new_image

def is_top_heavy(data, BASE_COLOR):
  """
  Determines whether a list is "top heavy", meaning its data is likely on the left.
  :param 
  """
  left_0_len = 0
  for i in range(len(data)):
    if data[i] != BASE_COLOR:
      break
    left_0_len += 1
  
  right_0_len = 0
  for i in range(len(data) - 1, -1, -1):
    if data[i] != BASE_COLOR:
      break
    right_0_len += 1
  
  return left_0_len < right_0_len



def get_top_heaviness(image, BASE_COLOR, CRYPT_DIST):
  """
  Determines whether the top has more data than the bottom.
  Author: Kavyan
  :param Image image: image to search
  :param (int, int, int) BASE_COLOR: the color which represents 0
  :param CRYPT_DIST: the maximum distance from the color that data could be
  :return: a score of 'top-heaviness' 0-1
  NOTE: the height of the data to search is the range in which there exists either data or
  zeros. For example, the entire data could be a white region at the bottom, but the image
  could still be "top heavy" if within that region the data is at the top.
  """

  width, height = image.size
  pixels = image.load()

  # iterate through the coloumn space of the image
  # initialize master list of "top-heaviness" for each column
  top_heaviness = []
  for x in range(width):
    # initialize empty list of data in column
    col_data = []
    # loop through column, appending all 0s and data to list
    all_zeros = True
    for y in range(height):
      rgba = pixels[x,y]
      (r, g, b) = (rgba[0], rgba[1], rgba[2])
      if(compute_distance((r,g,b),BASE_COLOR) <= CRYPT_DIST):
        if not (r,g,b) == BASE_COLOR:
          all_zeros = False
        col_data.append((r,g,b))
    # determine "top-heaviness" of list, and append to master list
    if all_zeros:
      top_heavy = -3
    else:
      top_heavy = is_top_heavy(col_data, BASE_COLOR)
    top_heaviness.append(top_heavy)
    
  # compute whole top heaviness as percent, using master list
  heaviness_sum = sum(top_heaviness)
  if heaviness_sum < 0:
    heaviness_sum = 0
  return heaviness_sum / len(top_heaviness)

  
  
def is_mirrored(image, BASE_COLOR, CRYPT_DIST):
  """
  determines if a top-heavy image is mirrored, in that it should be
  read from right-to-left.
  :author: Kavyan
  :param Image image: The top-heavy image to parse.
  :param (int, int, int) BASE_COLOR: The color representing 0.
  :param float CRYPT_DIST: the acceptable distance from the base color.
  :return: True iff data is read right-to-left.
  """
  
  width, height = image.size
  pixels = image.load()
  
  row = -1
  for y in range(height):
    all_zeros = True
    for x in range(width):
      if compute_distance(pixels[x,y],BASE_COLOR) <= CRYPT_DIST and pixels[x,y] != BASE_COLOR:
        all_zeros = False
        break
    if all_zeros:
      row = y - 1
      break
  if row == -1:
    row = height - 1

  # get a list of all the data in row including the 0s
  data = []
  for x in range(width):
    if(compute_distance(pixels[x,row],BASE_COLOR) <= CRYPT_DIST):
        data.append(pixels[x,row])

  # return whether that list is top heavy
  return not is_top_heavy(data, BASE_COLOR)

def guess_base_color(image):
  """
  Guesses the base color from an image.
  :author: Alec
  :param Image image: the image to parse
  :return: the guessed base color and its distance (int,int,int), int
  """

  # this can be updated
  COLOR_COUNT = 30
  colors = extract_common_colors(extract_colors(image), COLOR_COUNT)
  
  guessed_color = (-1, -1, -1)
  max_close = 0

  # extract colors
  for color in colors.keys():
    close_color_count = len(get_close_colors(colors, color))
    if close_color_count > max_close:
      max_close = close_color_count
      guessed_color = color
  
  # guess a max distance
  if max_close == 1:
    max_distance = 1
  else:
    max_distance = math.sqrt(3)
    
  return (guessed_color, max_distance)

def guess_direction_info(image):
  """
  Guesses direction info from image.
  :author: Alec
  :param Image image: image to parse
  :return: bool horiz_first, bool top_to_bottom, bool left_to_right
  """

  BASE_COLOR, CRYPT_DIST = guess_base_color(image)
  max_top_heaviness = 0
  top_heavy_degrees = 0
  for degrees in [0, 90, 180, 270]:
    test_image = rotate_image(image, degrees)
    top_heaviness = get_top_heaviness(test_image, BASE_COLOR, CRYPT_DIST)
    if top_heaviness > max_top_heaviness:
      max_top_heaviness = top_heaviness
      top_heavy_degrees = degrees

  top_heavy_image = rotate_image(image, top_heavy_degrees)
  if top_heavy_degrees % 180 == 0:
    horiz_first = True
    top_to_bottom = top_heavy_degrees == 0
    left_to_right = not is_mirrored(top_heavy_image, BASE_COLOR, CRYPT_DIST)
  else:
    horiz_first = False
    left_to_right = top_heavy_degrees == 90
    top_to_bottom = not is_mirrored(top_heavy_image, BASE_COLOR, CRYPT_DIST)
  return horiz_first, top_to_bottom, left_to_right
  

def get_binary_data():
  """
  Gets binary data from user file input
  :author: Kyle
  :return: binary object with data from file
  """
  data_path = input("Data file path: ")
  data_file = open(data_path, "rb")
  data = data_file.read()
  return data

def prompt_direction_info():
  """
  Prompts user for image direction info
  :author: Kyle
  :return: bool horiz_first, bool top_to_bottom, bool left_to_right
  """
  horiz_first = input("Horizontal or vertical first? (h/v): ") == "h"
  top_to_bottom = input("Top to bottom or bottom to top? (tb/bt): ") == "tb"
  left_to_right = input("Left to right or right to left? (lr,rl): ") == "lr"
  return horiz_first, top_to_bottom, left_to_right
  
def to_direction(image, direction_info):
  """
  Position image in a specified direction
  :author: Alec
  :param Image image: image to be positioned
  :param direction_info (bool horiz_first, bool top_to_bottom, bool left_to_right): direction info of image
  :return: image positioned to direction
  """

  mirrored = not (direction_info[0] ^ direction_info[1] ^ direction_info[2])
  if mirrored:
    image = mirror_image(image)
    direction_info = (direction_info[0], direction_info[1] ^ (not direction_info[0]), direction_info[2] ^ direction_info[0])
  
  if direction_info[1] and not direction_info[2]:
    image = rotate_image(image, 270)
  elif not direction_info[1] and not direction_info[2]:
    image = rotate_image(image, 180)
  elif not direction_info[1] and direction_info[2]:
    image = rotate_image(image, 90)
  
  return image
  



def encrypt(bytes, image, horiz_first, top_to_bottom, left_to_right, BASE_COLOR, red, green, blue, reversed):
  """
  Encrypts inputted data into image using settings defined by input
  :author: Kyle
  :param Bytes bytes: binary data to be encrypted
  :param Image image: image to encrypt data into
  :param bool horiz-first: Encrypt data horizontally or vertically
  :param bool top_to_bottom: Encrypt data top to bottom or bottom to top
  :param bool left_to_right: Encrypt data left to right or right to left
  :param (int, int, int) BASE_COLOR: Base color to encrypt data to
  :param bool red: whether red should be included or not
  :param bool blue: whether blue should be included or not
  :param bool green: whether green should be included or not
  :param bool reversed: whether rgb should be bgr
  :return: image with encrypted data
  """

  # Position Image so starting position is top left corner, going from left to right then top to bottom
  image = to_direction(image, (horiz_first, top_to_bottom, left_to_right))
  
  image = write_binary(image, bytes, BASE_COLOR, red, green, blue, reversed)

  image = to_direction(image, (horiz_first, left_to_right, top_to_bottom))

  return image
    

def decrypt_auto(image):
  """
  Decrypts image automatically, by trying all possibilities
  :param Image image: image to decrypt
  :return: Bytes bytes: decrypted binary data
  """
  horiz_first, top_to_bottom, left_to_right = guess_direction_info(image)

  (BASE_COLOR, _) = guess_base_color(image)
  COLOR_COUNT = 30
  close_colors = get_close_colors(extract_common_colors(extract_colors(image), COLOR_COUNT), BASE_COLOR)
  
  red, blue, green = False, False, False
  # loop through close colors
  for color in close_colors:
    if(color[0] & 1 == 1):
      red = True
    if(color[1] & 1 == 1):
      green = True
    if(color[2] & 1 == 1):
      blue = True

  return decrypt(image,horiz_first,top_to_bottom,left_to_right,BASE_COLOR,red,green,blue,False)

  

def decrypt(image, horiz_first, top_to_bottom, left_to_right, BASE_COLOR, red, green, blue, reversed):
  """
  Decrypts image using settings defined by input
  :author: Kyle
  :param Image image: image to decrypt
  :param bool horiz-first: Decrypt data horizontally or vertically
  :param bool top_to_bottom: Decrypt data top to bottom or bottom to top
  :param bool left_to_right: Decrypt data left to right or right to left
  :param bool reversed: whether rgb should be bgr
  :return: Bytes bytes: decrypted binary data
  """
  # Position Image so starting position is top left corner, going from left to right then top to bottom
  image = to_direction(image, (horiz_first, top_to_bottom, left_to_right))
  
  binary = extract_binary(image, BASE_COLOR, red, green, blue, reversed)

  return binary

def main():
  """
  Prompts for the following:
  :author: Kyle
  File path
    | Encryption mode?
        Horizontal or vertical first?
        Top to bottom or bottom to top?
        Left to right or right to left?
        Data to send?
        Base color
        Include red?
        Include green?
        Include blue?
    | Decrpytion mode?
        | Automatic?
        | Manual?
            Horizontal or vertical first?
            Top to bottom or bottom to top?
            Left to right or right to left?
            Base color
            Include red?
            Include green?
            Include blue?
  """
  file_path = input("Image name: ")
  original_image = Image.open(file_path)
  encrypt_mode = input("Encryption? (y/n): ") == "y"
  
  if encrypt_mode: # encryption mode
    horiz_first, top_to_bottom, left_to_right = prompt_direction_info()
    # data 
    data = get_binary_data()
    print("Base color to encode in RGB")
    BASE_COLOR = (
      int(input("Red color value (0-255): ")), 
      int(input("Green color value (0-255): ")), 
      int(input("Blue color value (0-255): "))
    )
    red = input("Include red bit? (y/n): ") == "y"
    green = input("Include green bit? (y/n): ") == "y"
    blue = input("Include blue bit? (y/n): ") == "y"
    reversed = input("Reversed (rgb -> bgr)? (y/n): ") == "y"
    output = encrypt(data, original_image, horiz_first, top_to_bottom, left_to_right, BASE_COLOR, red, green, blue, reversed)
    out_file_path = input("Encryption complete, enter file path for image: ")
    output.save(out_file_path)
  else: 
    automatic = input("Try automatic decryption, or manual? (a/m): ") == "a"
    if automatic:
      output = decrypt_auto(original_image)
    else: # try manual decryption settings
      # (bool horiz_first, bool top_to_bottom, bool left_to_right)
      horiz_first, top_to_bottom, left_to_right = prompt_direction_info()
      red = input("Include red bit? (y/n): ") == "y"
      green = input("Include green bit? (y/n): ") == "y"
      blue = input("Include blue bit? (y/n): ") == "y"
      print("Base color to decrypt in RGB")
      BASE_COLOR = (
        int(input("Red color value (0-255): ")), 
        int(input("Green color value (0-255): ")), 
        int(input("Blue color value (0-255): "))
      )
      reversed = input("Reversed (rgb -> bgr)? (y/n): ") == "y"
      output = decrypt(original_image, horiz_first, top_to_bottom, left_to_right, BASE_COLOR, red, green, blue, reversed)


    out_file_path = input("Decryption complete, enter file path for output: ")
    with open(out_file_path, "wb") as file:
      file.write(output)

if __name__=="__main__":
  main()