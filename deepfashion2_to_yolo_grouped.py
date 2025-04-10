#yolo segmentation data format 
#<class-index> <x1> <y1> <x2> <y2> ... <xn> <yn>
#deepfashion2 segmentation data format
#segmentation: [[x1,y1,...xn,yn],[ ]], where [x1,y1,xn,yn] represents a polygon and a single clothing item may contain more than one polygon.

# open the json files under a directory 
import os
import json
import glob
from PIL import Image
import argparse
def convert_deepfashion2_to_yolo(input_dir,images_dir, output_dir):
    """
    Convert DeepFashion2 annotations to YOLO segmentation format
    
    Args:
        input_dir: Directory containing DeepFashion2 JSON annotation files
        output_dir: Directory to save YOLO format annotation files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all JSON files in the input directory
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    
    for json_file in json_files:
        # read the json file
        with open(json_file, 'r') as f:
            data = json.load(f)
        # Get corresponding image path and dimensions
        image_id = os.path.splitext(os.path.basename(json_file))[0]
        image_path = os.path.join(images_dir, image_id + '.jpg')
        image = Image.open(image_path)
        width, height = image.size
        # Get the base filename without extension
        base_filename = os.path.splitext(os.path.basename(json_file))[0]
        output_file = os.path.join(output_dir, f"{base_filename}.txt")
        
        # Open output file for writing
        with open(output_file, 'w') as f_out:
            # select "item1" and "category_id"
            for key in data:
                    if key.startswith('item'):
                        item = data[key]
                        # Convert category_id to zero-based index (assuming DeepFashion2 starts at 1)
                        class_index = item['category_id'] - 1
                        segmentation = item['segmentation']
                        line = f"{class_index} "
                        # Process each polygon in the segmentation
                        for polygon in segmentation:
                            points = polygon  # [x1,y1,x2,y2,...,xn,yn]
                            normalized_points = []
                            
                            # Normalize coordinates
                            for i in range(0, len(points), 2):
                                x = points[i] / width
                                y = points[i+1] / height
                                normalized_points.extend([x, y])
                            
                            # Format line in YOLO format with 6 decimal places
                            line += f"{''.join(map(lambda p: f'{p:.6f}', normalized_points))} "
                        line = line.strip() + "\n"
                        f_out.write(line)

def main():
    # Define input and output directories

    train_input_dir = "datasets/coco/train_subset/annos"
    train_images_dir = "datasets/coco/train_subset/images"
    train_output_dir = "datasets/yolo/train/labels"
    val_input_dir = "datasets/coco/val_subset/annos"
    val_images_dir = "datasets/coco/val_subset/images"
    val_output_dir = "datasets/yolo/val/labels"
    # Convert annotations
    convert_deepfashion2_to_yolo(train_input_dir,train_images_dir, train_output_dir)
    print(f"Conversion completed. YOLO format annotations saved to {train_output_dir}")
    convert_deepfashion2_to_yolo(val_input_dir,val_images_dir, val_output_dir)
    print(f"Conversion completed. YOLO format annotations saved to {val_output_dir}")
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert DeepFashion2 annotations to YOLO format.")
    parser.add_argument("input_dir", type=str, help="Directory containing DeepFashion2 JSON annotation files")
    parser.add_argument("images_dir", type=str, help="Directory containing corresponding images")
    parser.add_argument("output_dir", type=str, help="Directory to save YOLO format annotation files")
    
    args = parser.parse_args()
    
    convert_deepfashion2_to_yolo(args.input_dir, args.images_dir, args.output_dir)
    print(f"Conversion completed. YOLO format annotations saved to {args.output_dir}")