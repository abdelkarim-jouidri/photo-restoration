import replicate, os
from dotenv import load_dotenv
import base64
load_dotenv()
replicate_api_token = os.getenv('REPLICATE_API_TOKEN')

# Ensure the API token is available
if replicate_api_token is None:
    raise ValueError("REPLICATE_API_TOKEN environment variable is not set")

images_folder = r"C:\Users\hp\Documents\testCases"

# List all files in the directory
image_files = os.listdir(images_folder)

# Process each image file
for filename in image_files:
    # Construct the full path to the image file
    image_path = os.path.join(images_folder, filename)

    # Read image file and encode to base64
    with open(image_path, 'rb') as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        image_data_uri = f"data:application/octet-stream;base64,{data}"

    # Define input parameters for the model
    input_data = {
        "image": image_data_uri
    }

    try:
        # Run the model
        output = replicate.run(
            "jingyunliang/swinir:660d922d33153019e8c263a3bba265de882e7f4f70396546b6c9c8f9d47a021a",
            input=input_data
        )

        # Process or save the output as needed
        print(f"Processed {filename}. Output: {output}")

    except replicate.exceptions.ReplicateError as e:
        print(f"Error processing {filename}: {e}")

print("Processing complete.")
