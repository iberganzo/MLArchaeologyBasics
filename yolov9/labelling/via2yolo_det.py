import os
import json
import argparse

def via_rect_to_yolo(folder_path, outFolder, xSize, ySize):
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)

    for filename in os.listdir(folder_path):
        if filename.endswith(('.json', '.JSON')):
            json_file = os.path.join(folder_path, filename)
            with open(json_file) as f:
                data = json.load(f)

            for filename_img, image_data in data.items():
                filename2, _ = os.path.splitext(filename_img)
                print("Processed image: ", filename2)
                regions = image_data.get('regions', [])

                for region in regions:
                    shape_attributes = region.get('shape_attributes', {})
                    if shape_attributes.get('name') == 'rect':
                        x = shape_attributes.get('x', 0)
                        y = shape_attributes.get('y', 0)
                        width = shape_attributes.get('width', 0)
                        height = shape_attributes.get('height', 0)

                        # Convertir a YOLO (normalizado)
                        x_center = (x + width / 2) / xSize
                        y_center = (y + height / 2) / ySize
                        width_norm = width / xSize
                        height_norm = height / ySize

                        values = [0, round(x_center, 4), round(y_center, 4), round(width_norm, 4), round(height_norm, 4)]
                        result = ' '.join(map(str, values))

                        outpath = os.path.join(outFolder, filename2 + '.txt')
                        with open(outpath, 'a' if os.path.exists(outpath) else 'w') as file1:
                            file1.write(result + '\n')


def main():
    parser = argparse.ArgumentParser(description='VIA Rect to YOLO Format')
    parser.add_argument('--img', nargs=2, metavar=('xSize', 'ySize'), type=int, required=True, help='Image size in pixels horizontally and vertically')   
    args = parser.parse_args()
    xSize, ySize = args.img
    
    folder = 'via'
    outFolder = "yolo_det"
    via_rect_to_yolo(folder, outFolder, xSize, ySize)

if __name__ == "__main__":
    main()
