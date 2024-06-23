import os
import replicate
from dotenv import load_dotenv
import base64
import requests
from tkinter import Tk, filedialog
from PIL import Image

def get_input_folder():
    root = Tk()
    root.withdraw()  # Hide the root window
    input_folder = filedialog.askdirectory(title="Select Input Folder")
    root.destroy()  # Close the root window
    return input_folder

def increase_dpi(image_path, dpi=1200):
    try:
        with Image.open(image_path) as img:
            img.save(image_path, dpi=(dpi, dpi))
        print(f"Increased DPI of {image_path} to {dpi}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def process_images(input_images_folder, replicate_api_token):
    client = replicate.Client(api_token=replicate_api_token)
    output_folder = os.path.join(input_images_folder, "processed_images")

    os.makedirs(output_folder, exist_ok=True)

    input_image_files = os.listdir(input_images_folder)
    print(f"Starting the processing of images in {input_images_folder}...")

    for filename in input_image_files:
        input_image_path = os.path.join(input_images_folder, filename)
        if not os.path.isfile(input_image_path) or not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # Step 1: Process image with Replicate API
        with open(input_image_path, 'rb') as file:
            data = base64.b64encode(file.read()).decode('utf-8')
            image_data_uri = f"data:image/png;base64,{data}" if filename.lower().endswith('.png') else f"data:image/jpeg;base64,{data}"

        input_data = {"img": image_data_uri}

        try:
            print(f"Starting Replicate processing for {filename}")
            output = replicate.run(
                "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
                input=input_data,
            )

            output_image_url = output
            output_image_data = requests.get(output_image_url).content
            processed_image_path = os.path.join(output_folder, filename)

            with open(processed_image_path, 'wb') as output_file:
                output_file.write(output_image_data)

            print(f"Finished Replicate processing for {filename}. Saved as: {processed_image_path}")

            # Step 2: Increase DPI of the processed image
            print(f"Starting DPI increase for {filename}")
            increase_dpi(processed_image_path)
            print(f"Finished DPI increase for {filename}")

        except replicate.exceptions.ReplicateError as e:
            print(f"Error processing {filename} with Replicate API: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading processed image for {filename}: {e}")

    print("Image processing complete.")

if __name__ == "__main__":
    load_dotenv()
    replicate_api_token = os.getenv('REPLICATE_API_TOKEN')
    if replicate_api_token is None:
        raise ValueError("REPLICATE_API_TOKEN environment variable is not set")

    input_folder = get_input_folder()
    if not input_folder:
        raise ValueError("No input folder selected")

    # Process images: First apply Replicate API, then increase DPI
    process_images(input_folder, replicate_api_token)
