import os
import rawpy
import imageio
from PIL import Image, ImageEnhance, ImageOps

def process_image(image_path):
  try:
    with rawpy.imread(image_path) as raw:
      rgb = raw.postprocess(use_camera_wb=True)
      img = Image.fromarray(rgb)

      r, g, b = img.split()

      r_enhancer = ImageOps.autocontrast(r)
      g_enhancer = ImageOps.autocontrast(g)
      b_enhancer = ImageOps.autocontrast(b)

      r = ImageEnhance.Contrast(r_enhancer).enhance(1.0)
      g = ImageEnhance.Contrast(g_enhancer).enhance(1.0)
      b = ImageEnhance.Contrast(b_enhancer).enhance(1.0)
      
      img = Image.merge("RGB", (r, g, b))

      output_filename = os.path.splitext(image_path)[0] + '.jpg'
      imageio.imsave(output_filename, rgb)
      img.save(output_filename, 'JPEG', quality=95)

  except Exception as e:
    print(f"Error processing {image_path}: {e}")

for filename in os.listdir('.'):
  if filename.lower().endswith('.dng'):
    process_image(filename)
