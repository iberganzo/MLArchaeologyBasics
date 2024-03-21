import os
import json

def alternate_values(filename, all_points_x, all_points_y):
    print("filename: ", filename)
    valores = []
    valores.append(0)
    for i in range(len(all_points_x)):        
        valores.append(round(all_points_x[i]/512, 4))
        valores.append(round(all_points_y[i]/512, 4))
    
    outFolder = "yolo"
    outpath = os.path.join(outFolder, filename)

    result = ' '.join(map(str, valores))
    if not outpath.endswith('.txt'):
        outpath += '.txt'
    with open(outpath, 'a' if os.path.exists(outpath) else 'w') as file1:
        file1.write(result + '\n')

def process_json_file(json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    all_points_x = None
    all_points_y = None
    
    filenames = []
    for filename, image_data in data.items():
        filename_without_extension, _ = os.path.splitext(filename)
        regions = image_data.get('regions', [])
        for region in regions:
            shape_attributes = region.get('shape_attributes', {})
            if shape_attributes.get('name') == 'polygon':
                x_values = shape_attributes.get('all_points_x', [])
                y_values = shape_attributes.get('all_points_y', [])
                
                all_points_x = x_values
                all_points_y = y_values
                alternate_values(filename_without_extension, all_points_x, all_points_y)

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(('.json', '.JSON')):
            json_file = os.path.join(folder_path, filename)
            process_json_file(json_file)

folder = 'via'
process_folder(folder)
