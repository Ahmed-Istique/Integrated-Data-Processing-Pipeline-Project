import json
import os
import base64
from datetime import datetime
from labelme import utils
import numpy as np

def json_to_coco(json_files, output_file):
    coco = {
        "info": {
            "description": "COCO Dataset",
            "url": "",
            "version": "1.0",
            "year": datetime.now().year,
            "contributor": "",
            "date_created": datetime.now().strftime("%Y/%m/%d")
        },
        "licenses": [
            {
                "url": "",
                "id": 1,
                "name": "Unknown"
            }
        ],
        "images": [],
        "annotations": [],
        "categories": []
    }
    
    # Get all categories
    categories = {}
    category_id = 1
    
    # First pass: collect all categories
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            for shape in data['shapes']:
                if shape['label'] not in categories:
                    categories[shape['label']] = category_id
                    coco['categories'].append({
                        "id": category_id,
                        "name": shape['label'],
                        "supercategory": "none"
                    })
                    category_id += 1
    
    # Second pass: create images and annotations
    image_id = 1
    annotation_id = 1
    
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Add image
        coco['images'].append({
            "id": image_id,
            "width": data['imageWidth'],
            "height": data['imageHeight'],
            "file_name": data['imagePath'],
            "license": 1,
            "flickr_url": "",
            "coco_url": "",
            "date_captured": ""
        })
        
        # Add annotations
        for shape in data['shapes']:
            points = shape['points']
            
            # Convert points to segmentation format
            segmentation = []
            for point in points:
                segmentation.extend([point[0], point[1]])
            
            # Calculate bounding box [x, y, width, height]
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            bbox = [
                float(min(x_coords)),
                float(min(y_coords)),
                float(max(x_coords) - min(x_coords)),
                float(max(y_coords) - min(y_coords))
            ]
            
            # Calculate area
            area = bbox[2] * bbox[3]
            
            coco['annotations'].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": categories[shape['label']],
                "segmentation": [segmentation],
                "area": area,
                "bbox": bbox,
                "iscrowd": 0
            })
            annotation_id += 1
        
        image_id += 1
    
    # Save COCO JSON
    with open(output_file, 'w') as f:
        json.dump(coco, f, indent=2)
    
    print(f"✅ Converted {len(json_files)} images to {output_file}")
    print(f"📊 Statistics:")
    print(f"   - Images: {len(coco['images'])}")
    print(f"   - Annotations: {len(coco['annotations'])}")
    print(f"   - Categories: {len(coco['categories'])}")
    print(f"   - Categories: {[cat['name'] for cat in coco['categories']]}")

if __name__ == "__main__":
    # Get all JSON files in current directory
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not json_files:
        print("❌ No JSON files found in current directory!")
    else:
        output_file = "coco_annotations.json"
        json_to_coco(json_files, output_file)