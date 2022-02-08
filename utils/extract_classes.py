import os
from shutil import copyfile

class ImageData:
    def __init__(self, class1, class2, class3, data_dir):
        # class names
        self.class1 = class1
        self.class2 = class2
        self.class3 = class3
        # class folder names
        self.folder1 = "_".join(self.class1.split(" ")).lower()
        self.folder2 = "_".join(self.class2.split(" ")).lower()
        self.folder3 = "_".join(self.class3.split(" ")).lower()
        self.data_dir = data_dir
        self.images = os.listdir(data_dir)

    def package_images(self, batch):
        """Copies images to class folder \
            according to the class label in the batch"""
        # make dataset directories
        try:
            os.mkdir(f"./data/dataset/{self.folder1}")
            os.mkdir(f"./data/dataset/{self.folder2}")
            os.mkdir(f"./data/dataset/{self.folder3}")
        except FileExistsError:
            pass

        # iterating batch 
        for image in batch["_via_image_id_list"]:
            try:
                label = batch["_via_img_metadata"][image]["file_attributes"]["Class"]
                image = batch["_via_img_metadata"][image]["filename"].split("/")[-1]
                # check if image is in image data folder
                is_image_known = image in self.images

                #create source directory
                src = os.path.join(self.data_dir, image)

                # create destination directory
                if label == self.class1:
                    dst = f"./data/dataset/{self.folder1}/{image}"
                elif label == self.class2:
                    dst = f"./data/dataset/{self.folder2}/{image}"
                else:
                    dst = f"./data/dataset/{self.folder3}/{image}"
                # copy file
                if is_image_known:
                    copyfile(src, dst)
                    print(f"\n Copied from {src} to {dst}")
            except Exception as e:
                print(e)

    def split_image_list(self, image_list):
        if len(image_list) > 2500:
            split_1 = image_list[: 2501]
            split_2 = image_list[2501: ]
        else:
            split_1 = image_list
            split_2 = list()

        return split_1, split_2

    def populate_folder_split(self, src_name, dst_name, image_names_arr):
        # create destination folder
        folder = f"./data/dataset/{dst_name}"
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
        for image in image_names_arr:
            src = f"./data/dataset/{src_name}/{image}"
            dst = f"./data/dataset/{dst_name}/{image}"
            copyfile(src, dst)
            print(f"Copied {src} to {dst}")

    def split_folders(self):
        """Split class folder into sub folders consisting of not more than 2500 images"""
        # load all als images
        class1_images = os.listdir(f"./data/dataset/{self.folder1}")
        class2_images = os.listdir(f"./data/dataset/{self.folder2}")
        class3_images = os.listdir(f"./data/dataset/{self.folder3}")
        # split classes' images into 2 lists
        class1_1, class1_2 = self.split_image_list(class1_images)
        class2_1, class2_2 = self.split_image_list(class2_images)
        class3_1, class3_2 = self.split_image_list(class3_images)

        # create split folders' directories
        # class 1 (ALS)
        self.populate_folder_split(self.folder1, self.folder1+"_1", class1_1)
        self.populate_folder_split(self.folder1, self.folder1+"_2", class1_2)

        # class 2 (Healthy)
        self.populate_folder_split(self.folder2, self.folder2+"_1", class2_1)
        self.populate_folder_split(self.folder2, self.folder2+"_2", class2_2)

        # class 3 (ALS)
        self.populate_folder_split(self.folder3, self.folder3+"_1", class3_1)
        self.populate_folder_split(self.folder3, self.folder3+"_2", class3_2)