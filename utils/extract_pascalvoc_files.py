from PIL import Image
from converter import json2pascalvoc
import json
import cv2
import numpy as np
import os

# open labels json
with open("./data/label.json", "r") as f:
    data = json.loads(f.read())

# generates array of annotations objects for images in folder split
def generate_json4split(images_arr, data, folder_name):
    """
        images_arr: array containing names of images in folder split
        data: array of all annotation objects (label.json)
        folder_name: folder split name
    """
    # intialize final data array
    data_arr = list()

    for  i ,label_record in enumerate(data):
        try:
            # capture filename
            filename = label_record["filename"]
            # proceed preprocessing if filename is known (in images array).
            if filename in images_arr:
                #specify dataset path
                path = f"beans/{folder_name}/{filename}"
                # Extract image width and height
                img = Image.open(f"./data/dataset/{folder_name}/{filename}")
                width, height = img.size
                # initialize bounding box objects' array
                annotations = list()
                # retrieve all attributes
                regions = label_record["regions"]
                disease_class = label_record["file_attributes"]["Class"]
                has_other_symptoms = label_record["file_attributes"]["Has Other Symptoms"]
                severity = label_record["file_attributes"]["Severity"]
                variety = label_record["variety"]
                age = label_record["age"]
                district = label_record["district"]
                subcounty = label_record["subcounty"]
                date_time = label_record["date_time"]
                # format bounding box objects
                for region in regions:
                    try:
                        # extract region attributes 
                        xmin = region["shape_attributes"]["x"]
                        ymin = region["shape_attributes"]["y"]
                        xmax = xmin+region["shape_attributes"]["width"]
                        ymax = ymin+region["shape_attributes"]["height"]
                        infection_stage = region["region_attributes"]["Infection Stage"] if region["region_attributes"]["Infection Stage"] else "unspecified"
                        # add region to regions array
                        annotations.append({
                            "name": disease_class,
                            "pose": "unspecified",
                            "truncated": 0,
                            "difficult": 0,
                            "bndbox": {
                                "xmin": xmin,
                                "ymin": ymin,
                                "xmax": xmax,
                                "ymax": ymax
                            },
                            "infection_stage": infection_stage
                        })
                    except KeyError as e:
                        continue
                data_arr.append({
                    "annotation": {
                        "folder": folder_name,
                        "filename": filename,
                        "path": path,
                        "source": {

                            "database": "Lacuna Agric Beans Dataset Makerere AI Lab"
                        },
                        "size": {
                            "width": width,
                            "height": height,
                            "depth": 3
                        },
                        "segmented": 0,
                        "object": annotations,
                        "class": disease_class,
                        "has_other_symptoms": has_other_symptoms,
                        "severity": severity,
                        "variety": variety,
                        "age": age,
                        "district": district,
                        "subcounty": subcounty,
                        "date_time": date_time
                    }
                })
        except KeyError as e:
            print(e)
            continue
    return data_arr

def generate_pascalvocs():
    print("Generating pascal VOC fomat files")
    # get array of split folder names
    folder_splits = [i for i in os.listdir("./data/dataset") if (("1" in i) or ("2" in i))]

    for folder in folder_splits:
        # read all image names
        folder_images = os.listdir(f"./data/dataset/{folder}")
        # generate annotations object for this split
        folder_data_arr = generate_json4split(folder_images, data, folder)
        # writing annotations to json
        with open(f"./data/{folder}.json","w") as f:
            json.dump({"data": folder_data_arr}, f)
        # generate pascal VOC formats
        json2pascalvoc.convertJson2Pascal(f"./data/{folder}.json", f"./data/dataset/{folder}")