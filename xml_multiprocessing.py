import os
import csv
from zipfile import ZipFile
from io import TextIOWrapper
import xml.etree.ElementTree as ET
import multiprocessing as mp
import time


# Parse a file in zip without the unpacking
def parse_zipfin(zipfin, filename):
    # Read the archived file to memory
    fin = TextIOWrapper(zipfin.open(filename))
    tree = ET.parse(fin)
    root = tree.getroot()

    id_ = ""
    level = ""
    objects = []

    for variable in root.findall(".//var"):
        if (variable.attrib["name"]) == "id":
            id_ = variable.attrib["value"]
        if (variable.attrib["name"]) == "level":
            level = variable.attrib["value"]

    for variable in root.findall(".//object"):
        object_name = variable.attrib["name"]

        objects.append(object_name)

    return id_, level, objects


def zip_parse(zipfile, levels, object_names):
    # Initialize dictionaries to store zip data
    with ZipFile(zipfile) as zipfin:
        for filename in zipfin.infolist():
            id_, level, objects = parse_zipfin(zipfin, filename)
            levels[id_] = level
            object_names[id_] = objects

    return levels, object_names


# iterate over files in the directory
def list_directory(directory="tmp"):  # Assign directory
    # Initialize dictionaries to store data before csv printing
    my_files = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # Checking if it is a file
        if os.path.isfile(f):
            my_files.append(f)

    # Initialize an iterable for the starmap multiprocessing
    all_combos = []
    for key in my_files:
        all_combos.append([key, {}, {}])
    with mp.Pool(min(mp.cpu_count(), len(all_combos))) as pool:  # number of workers
        results = pool.starmap(zip_parse, all_combos, chunksize=1)  # Get results

    # Print levels to csv
    with open("levels.csv", "w") as csvfile:
        fieldnames = ["id", "level"]
        # Create a CSV dictionary writer and add the header with field names
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        # Print levels
        for result in results:
            levels = result[0]  # The first item is the levels item
            for key, value in levels.items():
                writer.writerow([key, value])

    # Print object names to csv
    with open("object_names.csv", "w") as csvfile:
        fieldnames = ["id", "object_name"]  # Add the header with field names
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        # Print object_names
        for result in results:
            object_names = result[1]  # The second item is the object names item
            for key, value in object_names.items():
                for name in value:
                    writer.writerow([key, name])


if __name__ == "__main__":
    start_time = time.time()
    list_directory()
    print("time elapsed: {:.2f}s".format(time.time() - start_time))
    print(mp.cpu_count())
