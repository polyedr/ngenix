# NGENIX test project



```
<root>
<var name='id' value='<random unique string value>'/>
<var name='level' value='<random number from 1 to 100>'/>
<objects>
<object name='<random string value>'/>
<object name='<random string value>'/>
…
</objects>
</root>
```
Write a Python program that does the following:
1. Creates 50 zip archives, each containing 100 xml files with random data of the structure above.
Objects tag contains a random number (from 1 to 10) of nested object tags.

2. Processes the directory with received zip archives, parses nested xml files and generates 2 csv files:
First: id, level - one line for each xml file
Second: id, object_name - on a separate line for each object tag (it will turn out from 1 to 10 lines for each xml file)
It is highly desirable for the second task to use efficiently the multi-core processor resources.

## Getting Started

1. xml_archive_create.py   creates a bunch of zip archives at the temp folder
2. xml_zip_parse.py        parses the archives obtained from the temp folder, without multiprocessing
3. xml_multiprocessing.py  parses the archives obtained from the temp folder, with multiprocessing

### Prerequisites
#####  *Python 3.7 +*

Extra packages are not required

## Authors

* **Ivan Ishchukov**
