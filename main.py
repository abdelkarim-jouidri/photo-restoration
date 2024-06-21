import replicate
from dotenv import load_dotenv
import base64
load_dotenv()

with open(r"C:\Users\hp\Documents\testCases\comic.png", 'rb') as file:
  data = base64.b64encode(file.read()).decode('utf-8')
  image = f"data:application/octet-stream;base64,{data}"

input = {
    "image": image,
}

output = replicate.run(
    "jingyunliang/swinir:660d922d33153019e8c263a3bba265de882e7f4f70396546b6c9c8f9d47a021a",
    input=input
)
print(output)
#=> [{"file":"https://replicate.delivery/mgxm/1e3c0b87-01a7-4...