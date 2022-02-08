from utils import batch
from utils import extract_classes
from utils.combine_annotations import combine
from utils.extract_pascalvoc_files import generate_pascalvocs

def pipeline():
    print(f"pipeline started")
    # read classes
    classes = list()
    with open('./config/classes.txt') as f:
        classes = f.read().splitlines()
    als = classes[0]
    healthy = classes[1]
    bean_rust = classes[2]

    # load image names array (all images)
    data_dir = "./data/images"

    image_data_packager = extract_classes.ImageData(als, healthy, bean_rust, data_dir)
   
    # Create class folders
    batches = batch.load_batches()
    for b in batches:
        image_data_packager.package_images(b)

    image_data_packager.split_folders()

    combine()

    generate_pascalvocs()

    print("Data packaging complete")
if __name__== "__main__":
    pipeline()