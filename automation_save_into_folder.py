import os
import replicate
from dotenv import load_dotenv
import base64
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve the Replicate API token from environment variables
replicate_api_token = os.getenv('REPLICATE_API_TOKEN')

# Ensure the API token is available
if replicate_api_token is None:
    raise ValueError("REPLICATE_API_TOKEN environment variable is not set")

# Set the token in the replicate client
client = replicate.Client(api_token=replicate_api_token)

# Directory containing input images
input_images_folder = r"C:\Users\hp\Documents\testCases"

# Directory to save output images
output_images_folder = r"C:\Users\hp\Documents\processed_images"

# Create the output directory if it doesn't exist
os.makedirs(output_images_folder, exist_ok=True)

# List all files in the input directory
input_image_files = os.listdir(input_images_folder)

# Process each input image file
for filename in input_image_files:
    # Construct the full path to the input image file
    input_image_path = os.path.join(input_images_folder, filename)

    # Read input image file and encode to base64
    with open(input_image_path, 'rb') as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        image_data_uri = f"data:application/octet-stream;base64,{data}"

    # Define input parameters for the model
    input_data = {
        "image": image_data_uri
    }

    try:
        # Run the model
        output = client.run(
            "jingyunliang/swinir:660d922d33153019e8c263a3bba265de882e7f4f70396546b6c9c8f9d47a021a",
            input=input_data
        )

        # Save the output image to the output directory
        output_image_url = output
        output_image_data = requests.get(output_image_url).content
        output_image_path = os.path.join(output_images_folder, f"{filename.split('.')[0]}_processed.jpg")

        with open(output_image_path, 'wb') as output_file:
            output_file.write(output_image_data)

        print(f"Processed {filename}. Saved as: {output_image_path}")

    except replicate.exceptions.ReplicateError as e:
        print(f"Error processing {filename}: {e}")

print("Processing complete.")
