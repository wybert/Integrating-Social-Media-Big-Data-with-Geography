import os
import shutil
from tqdm import tqdm
path = "heavyai_storage/var/lib/heavyai/storage/export"
out_path = "RyanProject/tweets/2015_new"
os.makedirs(out_path, exist_ok=True)
for sub_dir in tqdm(list(os.listdir(path))):
    sub_path = os.path.join(path, sub_dir)
    for file in tqdm(list(os.listdir(sub_path))):
        file_path = os.path.join(sub_path, file)
        shutil.copy(file_path, out_path)
print("Done")

