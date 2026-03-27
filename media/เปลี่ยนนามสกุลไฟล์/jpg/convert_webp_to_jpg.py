import os
from PIL import Image

folder = "."

for file in os.listdir(folder):

    if file.lower().endswith(".webp"):

        webp_path = os.path.join(folder, file)
        jpg_path = os.path.join(folder, file.replace(".webp", ".jpg"))

        img = Image.open(webp_path).convert("RGB")
        img.save(jpg_path, "JPEG", quality=95)

        print(f"แปลง {file} → {file.replace('.webp','.jpg')}")

print("แปลงครบแล้ว")