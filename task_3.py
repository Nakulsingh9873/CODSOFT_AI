from transformers import VisionEncoderDecoderModel
from transformers import ViTImageProcessor
from transformers import AutoTokenizer
from PIL import Image

# Load model and processor
model = VisionEncoderDecoderModel.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)

processor = ViTImageProcessor.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)

tokenizer = AutoTokenizer.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)

# Load image
image = Image.open("images/sample.jpg").convert("RGB")

# Convert image to model input
pixel_values = processor(
    images=image,
    return_tensors="pt"
).pixel_values

# Generate caption
output_ids = model.generate(
    pixel_values,
    max_length=30
)

caption = tokenizer.decode(
    output_ids[0],
    skip_special_tokens=True
)

print("Generated Caption:")
print(caption)