import os
import json
import pandas as pd
import numpy as np

# helper function
def filter_dataframe(df):
    """Extracts columns of intrest"""
    df1 = df.copy()
    df1["images"] = (df1["image_1"]+" "
                     +df1["image_2"]+" "
                     +df1["image_3"]+" "
                     +df1["image_4"]+" "
                     +df1["image_5"]+" "
                     +df1["image_6"]+" "
                     +df1["image_7"]+" "
                     +df1["image_8"]+" "
                     +df1["image_9"]+" "
                     +df1["image_10"])
    return df1[["bean_variety", 
                "bean_plant_age", 
                "data_district", 
                "subcounty", 
                "comment", 
                "images", 
                "end_time"]]

def generate_attribute_value(attribute, object):
    try:
        attribute = object[attribute] if object[attribute] else "unspecified"
    except KeyError:
        attribute = "unspecified"
    return attribute


def combine():
    # store batches directory
    print("Combining all annotation objects")
    batches_dir = os.listdir("./data/batches")
    # load field data
    df1 = pd.read_excel("./data/field/trip1.xlsx")
    df1.fillna("", inplace=True)
    df2 = pd.read_excel("./data/field/trip2.xlsx")
    df2.fillna("", inplace=True)
    # filter dataframes
    trip1 = filter_dataframe(df1)
    trip2 = filter_dataframe(df2)

    # compile all image annotation dictionaries in one dictionary
    image_ids = list()
    images_dictionary = {}
    for batch in batches_dir:
        f = open(f"./data/batches/{batch}")
        data = json.load(f)
        batch_annotations_object = data["_via_img_metadata"]
        # add via annotation objects to images dictionary
        images_dictionary.update(batch_annotations_object)
        # add all via image ids to image ids' list
        image_ids += batch_annotations_object.keys()

    # create custom annotations list
    labels_array = list()
    for image in image_ids:
        # extract image name from via id
        image_name = image.split("/")[-1][:-2]
        # filter dataframes for rows where image name is contained in images string
        trip2_filter = trip2.loc[trip2["images"].str.contains(image_name, na=False)]
        trip1_filter = trip1.loc[trip1["images"].str.contains(image_name, na=False)]
        # select correct dataframe
        if len(trip2_filter):
            image_df = trip2_filter
        elif len(trip1_filter):
            image_df = trip1_filter
        else:
            continue
        # store field attributes in variables
        variety = image_df.iloc[0]["bean_variety"]
        age = int(image_df.iloc[0]["bean_plant_age"])
        district = image_df.iloc[0]["data_district"]
        date_time = image_df.iloc[0]["end_time"]
        subcounty = image_df.iloc[0]["comment"] if image_df.iloc[0]["comment"] else image_df.iloc[0]["subcounty"]
         # get image annotation object
        image_data = images_dictionary[image]
        # add field attributes
        image_data["variety"] = variety if variety else "unspecified"
        image_data["age"] = age if age else "unspecified"
        image_data["district"] = district if district else  "unspecified"
        image_data["date_time"] = date_time if date_time else "unspecified"
        image_data["subcounty"] = subcounty if subcounty else "unspecified"
        image_data["filename"] = image_name if image_name else "unspecified"
        # extract field data attributes
        image_data["filename"] = generate_attribute_value("filename", image_data)
        # parse file attribute values
        image_data["file_attributes"]["Class"] = generate_attribute_value("Class", image_data["file_attributes"])
        image_data["file_attributes"]["Has Other Symptoms"] = generate_attribute_value("Has Other Symptoms", image_data["file_attributes"])
        image_data["file_attributes"]["Severity"] = generate_attribute_value("Severity", image_data["file_attributes"])
        # add image data object to collective labels array
        labels_array.append(image_data)
    # write labels json
    with open("./data/label.json", "w") as f:
        json.dump(labels_array, f)