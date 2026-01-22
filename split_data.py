import os
import random
import shutil

# ------------------------
# CONFIG
# ------------------------
DATA_DIR = "data/mushrooms"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")
TEST_DIR = os.path.join(DATA_DIR, "test")

VAL_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42
# ------------------------

random.seed(RANDOM_SEED)

classes = ["edible", "poisonous"]

for cls in classes:
    train_class_dir = os.path.join(TRAIN_DIR, cls)
    val_class_dir = os.path.join(VAL_DIR, cls)
    test_class_dir = os.path.join(TEST_DIR, cls)

    os.makedirs(val_class_dir, exist_ok=True)
    os.makedirs(test_class_dir, exist_ok=True)

    # Each subfolder is a species
    species = [
        d for d in os.listdir(train_class_dir)
        if os.path.isdir(os.path.join(train_class_dir, d))
    ]

    random.shuffle(species)

    n_total = len(species)
    n_val = int(VAL_RATIO * n_total)
    n_test = int(TEST_RATIO * n_total)

    val_species = species[:n_val]
    test_species = species[n_val:n_val + n_test]
    train_species = species[n_val + n_test:]

    for sp in val_species:
        shutil.move(
            os.path.join(train_class_dir, sp),
            os.path.join(val_class_dir, sp)
        )

    for sp in test_species:
        shutil.move(
            os.path.join(train_class_dir, sp),
            os.path.join(test_class_dir, sp)
        )

    print(
        f"{cls}: "
        f"{len(train_species)} species train, "
        f"{len(val_species)} species val, "
        f"{len(test_species)} species test"
    )

print("✅ Species-level dataset split complete.")
