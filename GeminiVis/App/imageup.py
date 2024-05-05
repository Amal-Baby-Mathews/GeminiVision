import os
import sqlite3
import litellm
from PIL import Image  # for image compression
import dotenv
# Replace with your Gemini Vision API key and endpoint
load_dotenv()
GEMINI_VISION_API_KEY = os.getenv('GEMINI_VISION_API_KEY')
GEMINI_VISION_ENDPOINT = "https://api.gemini.ai/vision/v1/analyze"
from dotenv import load_dotenv


def connect_to_db():
  """Connects to the local SQLite database."""
  conn = sqlite3.connect('product_data.db')  # Replace with your desired database name
  return conn


def create_table(conn):
  """Creates a table named 'products' in the database."""
  cursor = conn.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    image_id TEXT PRIMARY KEY,
                    label TEXT,
                    description TEXT,
                    image_path TEXT
                  )''')
  conn.commit()


def insert_data(conn, image_id, description, image_path):
  """Inserts data into the 'products' table."""
  cursor = conn.cursor()
  cursor.execute('''INSERT INTO products (image_id, description, image_path)
                        VALUES (?, ?, ?)''', (image_id,  description, image_path))
  conn.commit()


def compress_image(image_path, output_path, quality=80):
  """Compresses an image using Pillow."""
  img = Image.open(image_path)
  # Move the compressed image to the desired location
  target_dir = 'C:\\Users\\amalb\\Amal Work\\GeminiVision\\GeminiVision\\GeminiVis\\uploaded_images'
  os.makedirs(target_dir, exist_ok=True)  # Create the target directory if it doesn't exist
  compressed_path = os.path.join(target_dir, output_path)
  img.save(compressed_path, quality=quality)
  return compressed_path


def analyze_image(image_path):

    """Analyze the image using the Gemini API."""
    os.environ["GEMINI_API_KEY"] = GEMINI_VISION_API_KEY
    prompt = 'Describe the image in a few sentences.'
    image_url = image_path  # Replace with the actual image URL or path

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }
    ]

    response = litellm.completion(
        model="gemini/gemini-pro-vision",
        messages=messages,
    )

    content = response.get('choices', [{}])[0].get('message', {}).get('content')
    return content


def upload_and_store_data(image_path, image_id):
  """
  Compresses, analyzes image, stores labels, description, and path in the database.

  Uses Gemini Vision API and stores locally compressed images.
  """
  conn = connect_to_db()
  create_table(conn)  # Create table if it doesn't exist

  # Compress image
  compressed_path = f'compressed_{image_id}.jpg'
  full_compressed_path=compress_image(image_path, compressed_path)

  # Analyze image with Gemini Vision API
  analysis_result = analyze_image(full_compressed_path)

  # Extract labels and description (replace with specific keys if different)
  description = analysis_result
  print(description)
  # Store data in database
  insert_data(conn, image_id, description, full_compressed_path)
  conn.close()
  print(f'Image compressed, analyzed, and data stored for ID: {image_id}')


# # Example usage
# image_path = 'path/to/your/image.jpg'
# image_id = 'unique_image_id'


def upload_multiple_images_from_folder(folder_path, start_id=0):
    """Uploads multiple images from a folder and stores them in the database.
    
    Args:
        folder_path (str): The path to the folder containing the images.
        start_id (int): The ID to start counting from (default is 0).
    """
    image_files = [f for f in os.listdir(folder_path)
                   if os.path.isfile(os.path.join(folder_path, f))
                   and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    for i, filename in enumerate(image_files, start=start_id):
        image_path = os.path.join(folder_path, filename)
        upload_and_store_data(image_path, str(i))


# upload_and_store_data(image_path, image_id)
