#it should read all the json files in the given directory 
# for each category, it should get a 1000 samples
# it should save the samples in a new json file in the target directory

#using the json file name to get the image path and save it in a new directory

import os
import json
import random
import shutil
from collections import defaultdict
import argparse

def filter_deepfashion2(input_dir, images_dir, output_dir, target_dir, samples_per_category=1000):
    """
    Filter DeepFashion2 dataset to get a fixed number of samples per category.

    Args:
        input_dir: Directory containing DeepFashion2 JSON annotation files.
        images_dir: Directory containing corresponding images.
        output_dir: Directory to save filtered JSON files.
        target_dir: Directory to save filtered images.
        samples_per_category: Number of samples to extract per category.
    """
    # Create output directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(target_dir, exist_ok=True)

    # Group samples by category
    category_samples = defaultdict(list)
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    for json_file in json_files:
        json_path = os.path.join(input_dir, json_file)
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        for key in data:
            if key.startswith('item'):
                item = data[key]
                category_id = item['category_id']
                # Filter items with viewpoint = 2 frontal
                if item.get('viewpoint') == 2:
                    category_samples[category_id].append(json_file)
    # Filter samples and save
    for category_id, files in category_samples.items():
        # Randomly select the required number of samples
        selected_files = random.sample(files, min(samples_per_category, len(files)))

        for json_file in selected_files:
            # Copy JSON file to output directory
            src_json_path = os.path.join(input_dir, json_file)
            dst_json_path = os.path.join(output_dir, json_file)
            shutil.copy(src_json_path, dst_json_path)

            # Copy corresponding image to target directory
            image_id = os.path.splitext(json_file)[0]
            src_image_path = os.path.join(images_dir, f"{image_id}.jpg")
            dst_image_path = os.path.join(target_dir, f"{image_id}.jpg")
            if os.path.exists(src_image_path):
                shutil.copy(src_image_path, dst_image_path)
        #output each category id and the number of samples in it
        print(f"Category {category_id}: {len(selected_files)} samples")
    print(f"Filtered dataset saved to {output_dir} and {target_dir}")

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter DeepFashion2 dataset.")
    parser.add_argument("--input_dir", required=True, help="Directory with JSON files")
    parser.add_argument("--images_dir", required=True, help="Directory with images")
    parser.add_argument("--output_dir", required=True, help="Directory to save filtered JSON files")
    parser.add_argument("--target_dir", required=True, help="Directory to save filtered images")
    parser.add_argument("--samples_per_category", type=int, default=1000, help="Number of samples per category")

    args = parser.parse_args()

    filter_deepfashion2(
        input_dir=args.input_dir,
        images_dir=args.images_dir,
        output_dir=args.output_dir,
        target_dir=args.target_dir,
        samples_per_category=args.samples_per_category
    )
