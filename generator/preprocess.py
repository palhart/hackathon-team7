import base64
import os
from pdf2image import convert_from_path
import shutil




def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

def convert_input(pdf_path, image_dir):
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)
    os.makedirs(image_dir)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        file_name = os.path.join(image_dir, f'page{i+1}.jpeg')
        image.save(file_name, 'JPEG')
        print(f'Image saved as {file_name}')
    return images

def get_images_path(image_dir):
    return [os.path.join(image_dir, image) for image in os.listdir(image_dir) if image.endswith('.jpeg')]


if __name__ == '__main__':
    pdf_path = '/data/Webslides_Q324_Final.pdf'
    image_dir = '/data/images'
    convert_input(pdf_path, image_dir)