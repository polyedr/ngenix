# NGENIX test
import os
import string
import secrets
import shutil
import random as rand
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import xml.etree.ElementTree as ET


# save data to archive
def save_file_zip(idx, path, data):
    # create filenames
    filepath = os.path.join(path, f"data-{idx:04d}.xml")
    zip_index = idx // 100  # Create index for 50 archives
    archivepath = os.path.join(path, f"archive-{zip_index:02d}.zip")
    # open the zip file
    with ZipFile(archivepath, "a", compression=ZIP_DEFLATED) as handle:
        # save the data
        handle.writestr(filepath, data)
        # report progress
        print(f".archived {filepath}")


# generate a random string
def generate_line():
    num = 20  # define the length of the string
    # a secure calculation of the random string with secrets library
    line = "".join(
        secrets.choice(string.ascii_letters + string.digits) for x in range(num)
    )
    return line


# generate file data of 10K lines each with 10 data points
def generate_xml_file_data():
    root = ET.Element("root")  # Initialize root

    var_id = ET.SubElement(root, "var")  # Create a first var element
    var_id.set("name", "id")
    line = generate_line()  # Generate a random string
    var_id.set("value", line)

    var_level = ET.SubElement(root, "var")  # Create a second var element
    var_level.set("name", "level")
    rndnumber = rand.randint(1, 100)  # Generate a random number
    var_level.set("value", str(rndnumber))

    objects = ET.SubElement(root, "objects")  # Create objects element

    rndrange = rand.randint(1, 10)  # Generate a random range
    for _ in range(rndrange):
        object_ = ET.SubElement(objects, "object")  # Create object element

        line = generate_line()  # Generate a random string
        object_.set("name", line)

    # Convert an element tree to string before printing
    etstring = ET.tostring(root, short_empty_elements=False).decode("utf-8")
    return etstring


# generate 5K files in 50 archives
def generate_all_files(path="tmp"):
    # create a local directory to save files
    if os.path.exists(path):
        shutil.rmtree(path)  # Clear the directory if exists

    os.makedirs(path)

    # create all files and save them to archives
    for i in range(5000):
        # generate data
        data = generate_xml_file_data()
        # save xml files to archives
        save_file_zip(i, path, data)


if __name__ == "__main__":
    # entry point, generate all of the files
    generate_all_files()
