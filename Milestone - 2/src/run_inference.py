import os
import torch
from torchvision import transforms
from PIL import Image
from srcnn_architecture import SRCNN

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MILESTONE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
TEST_DIR = os.path.join(MILESTONE_DIR, "test")
OUTPUT_DIR = os.path.join(MILESTONE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load trained model
MODEL_PATH = os.path.join(MILESTONE_DIR, "models", "srcnn_trained_model.pth")
model = SRCNN().to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.eval()

# Transforms
to_tensor = transforms.ToTensor()
to_pil = transforms.ToPILImage()

def downscale_upscale(img, lr_size=(64, 64), hr_size=(256, 256)):
    # Create blurry LR image by downscaling then upscaling
    lr = img.resize(lr_size, Image.BICUBIC)
    return lr.resize(hr_size, Image.BICUBIC)  # bicubic upscaled

def run_inference():
    images = [f for f in os.listdir(TEST_DIR) if f.lower().endswith(".png")]
    if not images:
        print("No test images found in test folder!")
        return

    for img_file in images:
        img_path = os.path.join(TEST_DIR, img_file)
        print(f"Processing: {img_path}")
        hr = Image.open(img_path).convert("RGB")

        # Blurry input
        lr_upscaled = downscale_upscale(hr)

        # SRCNN enhanced output
        lr_tensor = to_tensor(lr_upscaled).unsqueeze(0).to(device)
        with torch.no_grad():
            sr_tensor = model(lr_tensor)
        sr_img = to_pil(sr_tensor.squeeze(0).cpu().clamp(0, 1))

        # Save side-by-side comparison: Blurry | Enhanced
        comparison = Image.new("RGB", (hr.width * 2, hr.height))
        comparison.paste(lr_upscaled, (0, 0))   # Left: Blurry input
        comparison.paste(sr_img, (hr.width, 0))  # Right: SRCNN enhanced

        # Save with original test image name
        out_path = os.path.join(OUTPUT_DIR, f"comparison_{img_file}")
        comparison.save(out_path)
        print(f"Saved comparison image: {out_path}")

if __name__ == "__main__":
    run_inference()
