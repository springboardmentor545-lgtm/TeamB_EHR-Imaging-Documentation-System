import os
import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from PIL import Image
import numpy as np
from srcnn_architecture import SRCNN

# --------------------
# Paths
# --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # src/
MILESTONE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
TRAIN_DIR = os.path.join(MILESTONE_DIR, "train")
HR_DIR = os.path.join(TRAIN_DIR, "HR")
LR_DIR = os.path.join(TRAIN_DIR, "LR")
MODEL_DIR = os.path.join(MILESTONE_DIR, "models")
OUT_DIR = os.path.join(MILESTONE_DIR, "outputs")
SAMPLES_DIR = os.path.join(OUT_DIR, "samples")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SAMPLES_DIR, exist_ok=True)

# --------------------
# Hyperparams
# --------------------
PATCH_SIZE = 64
PATCH_EPOCHS = 150    # pretraining on patches
FULL_EPOCHS = 50      # fine-tuning on full images
BATCH_SIZE_PATCH = 16
BATCH_SIZE_FULL = 2
LR = 1e-4
VAL_SPLIT = 0.10
SEED = 42
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
sample_interval = 20

# --------------------
# Utilities
# --------------------
def psnr_batch(pred, target, max_val=1.0):
    mse = torch.mean((pred - target) ** 2, dim=[1,2,3])
    psnr = 10.0 * torch.log10((max_val ** 2) / (mse + 1e-10))
    return psnr.mean().item()

def tensor_to_pil(t):
    t = t.clamp(0,1).cpu().numpy()
    t = np.transpose(t, (1,2,0))
    t = (t * 255.0).round().astype(np.uint8)
    return Image.fromarray(t)

def get_key(fname: str):
    """
    Normalize filenames to a base key used to match HR/LR pairs.
    Removes common suffixes like _HR, _LR, _HR_aug, _LR_aug and file extension.
    Lowercases for robust matching.
    """
    name = fname.lower()
    # strip extension
    for ext in (".png", ".jpg", ".jpeg"):
        if name.endswith(ext):
            name = name[: -len(ext)]
            break
    # remove known suffixes
    for suf in ("_hr_aug", "_lr_aug", "_hr", "_lr"):
        if name.endswith(suf):
            name = name[: -len(suf)]
            break
    return name

def _list_image_files(folder):
    """
    Return list of image filenames in folder (not full paths).
    Accepts png/jpg/jpeg.
    """
    if not os.path.exists(folder):
        return []
    return [f for f in os.listdir(folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg")) and os.path.isfile(os.path.join(folder, f))]

def collect_pairs(hr_dir, lr_dir, patches_only=True):
    """
    Collect matching (lr_path, hr_path) pairs.
    If patches_only=True, only keep keys that contain 'patch' in their base key.
    Otherwise, keep keys that DON'T contain 'patch'.
    """
    hr_files = _list_image_files(hr_dir)
    lr_files = _list_image_files(lr_dir)

    hr_map, lr_map = {}, {}
    for f in hr_files:
        hr_map[get_key(f)] = f
    for f in lr_files:
        lr_map[get_key(f)] = f

    # intersection of keys present in both
    common_keys = set(hr_map.keys()) & set(lr_map.keys())
    if patches_only:
        common = sorted([k for k in common_keys if 'patch' in k])
    else:
        common = sorted([k for k in common_keys if 'patch' not in k])

    pairs = []
    for k in common:
        lr_file = lr_map[k]
        hr_file = hr_map[k]
        pairs.append((os.path.join(lr_dir, lr_file), os.path.join(hr_dir, hr_file)))
    return pairs

# --------------------
# Dataset
# --------------------
class PairDataset(Dataset):
    def __init__(self, pairs, transform=None):
        self.pairs = pairs
        # default transform: convert to tensor and normalize to [0,1]
        self.transform = transform or transforms.ToTensor()

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        lr_path, hr_path = self.pairs[idx]
        lr = Image.open(lr_path).convert('RGB')
        hr = Image.open(hr_path).convert('RGB')
        if lr.size != hr.size:
            lr = lr.resize(hr.size, Image.BICUBIC)
        return self.transform(lr), self.transform(hr)

# --------------------
# Training function
# --------------------
def run_training(model, train_loader, val_loader, optimizer, criterion, scheduler,
                 start_epoch, end_epoch, phase_name="patch"):

    best_val_loss = float('inf')
    best_path = os.path.join(MODEL_DIR, f"srcnn_best_{phase_name}.pth")
    last_path = os.path.join(MODEL_DIR, f"srcnn_last_{phase_name}.pth")

    for epoch in range(start_epoch, end_epoch + 1):
        # ---- Train ----
        model.train()
        running_loss, batches = 0.0, 0
        for lr_imgs, hr_imgs in train_loader:
            lr_imgs, hr_imgs = lr_imgs.to(DEVICE), hr_imgs.to(DEVICE)
            preds = model(lr_imgs)
            loss = criterion(preds, hr_imgs)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item(); batches += 1
        scheduler.step()
        train_loss = running_loss / (batches if batches > 0 else 1)

        # ---- Validation ----
        model.eval()
        val_loss_acc, val_batches, val_psnr_acc = 0.0, 0, 0.0
        with torch.no_grad():
            for lr_imgs, hr_imgs in val_loader:
                lr_imgs, hr_imgs = lr_imgs.to(DEVICE), hr_imgs.to(DEVICE)
                preds = model(lr_imgs)
                loss = criterion(preds, hr_imgs)
                val_loss_acc += loss.item()
                val_psnr_acc += psnr_batch(preds, hr_imgs)
                val_batches += 1
        val_loss = val_loss_acc / (val_batches if val_batches > 0 else 1)
        val_psnr = val_psnr_acc / (val_batches if val_batches > 0 else 1)

        print(f"[{phase_name} {epoch}] train_loss={train_loss:.6f}  val_loss={val_loss:.6f}  val_PSNR={val_psnr:.3f}")

        # Save models
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), best_path)
            print(f"  -> saved best model at {best_path}")
        torch.save(model.state_dict(), last_path)

        # Save sample visuals
        if epoch % sample_interval == 0 or epoch == start_epoch:
            try:
                sample_lr, sample_hr = next(iter(val_loader))
                sample_lr = sample_lr.to(DEVICE)
                with torch.no_grad():
                    sample_sr = model(sample_lr)
                for i in range(min(4, sample_lr.size(0))):
                    lr_img = tensor_to_pil(sample_lr[i])
                    sr_img = tensor_to_pil(sample_sr[i])
                    hr_img = tensor_to_pil(sample_hr[i])
                    W, H = lr_img.size
                    canvas = Image.new('RGB', (W*3, H))
                    canvas.paste(lr_img, (0,0))
                    canvas.paste(sr_img, (W,0))
                    canvas.paste(hr_img, (W*2,0))
                    out_file = os.path.join(SAMPLES_DIR, f"{phase_name}_epoch{epoch:03d}_sample{i}.png")
                    canvas.save(out_file)
            except StopIteration:
                pass

# --------------------
# Main train procedure (2-stage)
# --------------------
def train():
    torch.manual_seed(SEED)
    random.seed(SEED)

    # diagnostic prints
    print("====================================================")
    print("SRCNN training starting")
    print(f"Device: {DEVICE}")
    print(f"HR_DIR: {HR_DIR}")
    print(f"LR_DIR: {LR_DIR}")
    print("====================================================")

    # show counts (helpful)
    hr_list = _list_image_files(HR_DIR)
    lr_list = _list_image_files(LR_DIR)
    print(f"Found {len(hr_list)} image files in HR_DIR, {len(lr_list)} in LR_DIR")
    if len(hr_list) == 0 or len(lr_list) == 0:
        print("❌ One of the HR/LR folders is empty or not present. Please check paths.")
        print("HR files:", hr_list[:10])
        print("LR files:", lr_list[:10])
        return

    # -------- Stage 1: Patch pretraining --------
    patch_pairs = collect_pairs(HR_DIR, LR_DIR, patches_only=True)

    # If no patch images found, we have two sensible options:
    #  - fall back to full images (common case for many datasets)
    #  - or skip patch stage and go to full stage (we choose to fall back)
    if len(patch_pairs) == 0:
        print("⚠️ No patch pairs found — falling back to full-image pairs for pretraining.")
        patch_pairs = collect_pairs(HR_DIR, LR_DIR, patches_only=False)

    if len(patch_pairs) == 0:
        print("❌ ERROR: No matching HR/LR pairs found for either patch or full mode.")
        print("Make sure your HR and LR folders contain matching files with same base names.")
        print("Example: HR/image1_HR.png  LR/image1_LR.png")
        return

    print(f"Stage 1 (pretraining) - using {len(patch_pairs)} pairs")
    dataset_p = PairDataset(patch_pairs)
    n_val = max(1, int(len(dataset_p) * VAL_SPLIT))
    train_ds, val_ds = random_split(dataset_p, [len(dataset_p)-n_val, n_val])
    print(f"Stage 1 (patch pretraining): {len(train_ds)} train, {len(val_ds)} val")

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE_PATCH, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE_PATCH, shuffle=False)

    model = SRCNN().to(DEVICE)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=60, gamma=0.5)

    run_training(model, train_loader, val_loader, optimizer, criterion, scheduler,
                 start_epoch=1, end_epoch=PATCH_EPOCHS, phase_name="patch")

    # -------- Stage 2: Full-image fine-tuning --------
    full_pairs = collect_pairs(HR_DIR, LR_DIR, patches_only=False)
    if len(full_pairs) == 0:
        print("⚠️ Warning: No full image pairs found, skipping fine-tune stage.")
        return

    print(f"Stage 2 (full fine-tune) - using {len(full_pairs)} pairs")
    dataset_f = PairDataset(full_pairs)
    n_val = max(1, int(len(dataset_f) * VAL_SPLIT))
    train_ds, val_ds = random_split(dataset_f, [len(dataset_f)-n_val, n_val])
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE_FULL, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE_FULL, shuffle=False)

    optimizer = optim.Adam(model.parameters(), lr=LR/10)  # smaller LR for fine-tune
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.5)

    print(f"Stage 2 (full fine-tune): {len(train_ds)} train, {len(val_ds)} val")
    run_training(model, train_loader, val_loader, optimizer, criterion, scheduler,
                 start_epoch=1, end_epoch=FULL_EPOCHS, phase_name="full")

    print("🎯 Training complete! Models saved under:", MODEL_DIR)

if __name__ == "__main__":
    train()
