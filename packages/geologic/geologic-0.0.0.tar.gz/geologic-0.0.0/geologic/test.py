print("test.py was imported successfully")


from importlib import resources
import io


import pandas as pd
import os


with resources.open_text("geologic", "testtext.txt") as fp:
    print(fp)


with resources.open_text("geologic.data", "numbers.csv") as fp:
    print(fp)

print("All relevant things are done!")