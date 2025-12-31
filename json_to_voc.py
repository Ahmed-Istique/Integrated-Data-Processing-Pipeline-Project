import json
import xml.etree.ElementTree as ET
import os
from pathlib import Path

def json_to_voc_xml(json_file, output_dir):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create XML structure
    annotation = ET.Element('annotation')
    
    # Add folder and filename
    folder = ET.SubElement(annotation, 'folder')
    folder.text = 'VOC2007'
    
    filename = ET.SubElement(annotation, 'filename')
    filename.text = data['imagePath']
    
    # Add source
    source = ET.SubElement(annotation, 'source')
    ET.SubElement(source, 'database').text = 'Unknown'
    
    # Add image size
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(data['imageWidth'])
    ET.SubElement(size, 'height').text = str(data['imageHeight'])
    ET.SubElement(size, 'depth').text = '3'
    
    # Add segmented
    ET.SubElement(annotation, 'segmented').text = '0'
    
    # Add objects (bounding boxes)
    for shape in data['shapes']:
        obj = ET.SubElement(annotation, 'object')
        ET.SubElement(obj, 'name').text = shape['label']
        ET.SubElement(obj, 'pose').text = 'Unspecified'
        ET.SubElement(obj, 'truncated').text = '0'
        ET.SubElement(obj, 'difficult').text = '0'
        
        # Create bounding box from points
        bndbox = ET.SubElement(obj, 'bndbox')
        points = shape['points']
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        
        ET.SubElement(bndbox, 'xmin').text = str(int(min(x_coords)))
        ET.SubElement(bndbox, 'ymin').text = str(int(min(y_coords)))
        ET.SubElement(bndbox, 'xmax').text = str(int(max(x_coords)))
        ET.SubElement(bndbox, 'ymax').text = str(int(max(y_coords)))
    
    # Create XML file
    xml_filename = Path(json_file).stem + '.xml'
    xml_path = Path(output_dir) / xml_filename
    
    # Write XML file
    tree = ET.ElementTree(annotation)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)
    print(f"✅ Created: {xml_path}")

# Main conversion
if __name__ == "__main__":
    output_dir = "voc_xml_annotations"
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert all JSON files in current directory
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not json_files:
        print("❌ No JSON files found in current directory!")
    else:
        for json_file in json_files:
            json_to_voc_xml(json_file, output_dir)
        print(f"🎉 Converted {len(json_files)} JSON files to VOC XML format!")