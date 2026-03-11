import os
import random
import shutil

# Source directories
SOURCE_BASE = "data/mushrooms/test"

# Destination directory
DEST_BASE = "game_images"

# Classes
CLASSES = ["edible", "poisonous"]

# Create destination folders
for cls in CLASSES:
    os.makedirs(os.path.join(DEST_BASE, cls), exist_ok=True)


def collect_images(label):

    source_dir = os.path.join(SOURCE_BASE, label)
    dest_dir = os.path.join(DEST_BASE, label)

    species_folders = [
        f for f in os.listdir(source_dir)
        if not f.startswith(".") and os.path.isdir(os.path.join(source_dir, f))
    ]

    copied = 0

    for species in species_folders:

        species_path = os.path.join(source_dir, species)

        images = [
            f for f in os.listdir(species_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if not images:
            continue

        chosen_image = random.choice(images)

        src = os.path.join(species_path, chosen_image)

        # Rename to avoid filename collisions
        dst_name = f"{species}_{chosen_image}"
        dst = os.path.join(dest_dir, dst_name)

        shutil.copy(src, dst)

        copied += 1

    print(f"{label}: copied {copied} images")


for label in CLASSES:
    collect_images(label)

print("Game dataset created successfully.")
