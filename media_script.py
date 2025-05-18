import os
import shutil

scene_name = "RecursiveTreeStructure"
quality = "480p15"

project_root = os.getcwd()
media_dir = os.path.join(project_root, "media")
output_dir = os.path.join(project_root, "output")

video_src = os.path.join(media_dir, "videos", "main", quality)
image_src = os.path.join(media_dir, "images", "main")

os.makedirs(output_dir, exist_ok=True)

# Copy final videos
if os.path.exists(video_src):
    for file in os.listdir(video_src):
        if file.endswith(".mp4"):
            shutil.copy2(os.path.join(video_src, file), output_dir)
            
else:
    print("No video directory found:", video_src)

# Copy final images
if os.path.exists(image_src):
    for file in os.listdir(image_src):
        if file.endswith(".png"):
            shutil.copy2(os.path.join(image_src, file), output_dir)
else:
    print("No image directory found:", image_src)

print("Final videos and images copied to:", output_dir)