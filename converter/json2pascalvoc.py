import json
import xml.etree.ElementTree as ET


def convertJson2Pascal(file_path, xml_file_path=None):
    with open(file_path) as json_file:
        data = json.load(json_file)
        for image in data['data']:
            filename = str(image["annotation"]["filename"])
            print(f"Parsing {filename}")
            annotation = ET.Element("annotation")

            ET.SubElement(annotation, "folder", name="folder").text = image["annotation"]["folder"]
            ET.SubElement(annotation, "filename", name="filename").text = image["annotation"]["filename"]
            ET.SubElement(annotation, "path", name="path").text = image["annotation"]["path"]

            size = ET.SubElement(annotation, "size")
            ET.SubElement(size, "width", name="width").text = str(image["annotation"]["size"]["width"])
            ET.SubElement(size, "height", name="height").text = str(image["annotation"]["size"]["height"])
            ET.SubElement(size, "depth", name="depth").text = str(image["annotation"]["size"]["depth"])

            ET.SubElement(annotation, "class", name="class").text = image["annotation"]["class"]
            ET.SubElement(annotation, "hasOtherSymptoms", name="has other symptoms").text = image["annotation"]["has_other_symptoms"]
            ET.SubElement(annotation, "variety", name="variety").text = image["annotation"]["variety"]
            ET.SubElement(annotation, "age", name="age").text = str(image["annotation"]["age"])
            ET.SubElement(annotation, "district", name="district").text = str(image["annotation"]["district"])
            ET.SubElement(annotation, "subcounty", name="subcounty").text = str(image["annotation"]["subcounty"])
            ET.SubElement(annotation, "datetime", name="datetime").text = str(image["annotation"]["date_time"])

            for obj in image["annotation"]["object"]:
                object = ET.SubElement(annotation, "object")
                ET.SubElement(object, "name", name="name").text = obj["name"]
                bndbox = ET.SubElement(object, "bndbox")
                ET.SubElement(bndbox, "xmin", name="xmin").text = str(obj["bndbox"]["xmin"])
                ET.SubElement(bndbox, "ymin", name="ymin").text = str(obj["bndbox"]["ymin"])
                ET.SubElement(bndbox, "xmax", name="xmax").text = str(obj["bndbox"]["xmax"])
                ET.SubElement(bndbox, "ymax", name="ymax").text = str(obj["bndbox"]["ymax"])

            tree = ET.ElementTree(annotation)
            if xml_file_path is None:
                tree.write('/'.join(image["annotation"]["path"].split("/")[:-1]) + "/" +
                            image["annotation"]["filename"].split(".")[0] + ".xml")
            else:
                tree.write(xml_file_path+'/'+
                            image["annotation"]["filename"].split(".")[0] + ".xml")