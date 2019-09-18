from bs4 import BeautifulSoup
import os

data_dir = "/home/sean/jayne/docs/naser/"
min_length = 100


def get_grafs(xml_input):
    grafs_list = []
    soup = BeautifulSoup(xml_input, "lxml")
    grafs = soup.find_all('p')
    for graf in grafs:
        # TODO: clean the output and remove tags
        # DFL
        graf = graf.get_text()
        if len(graf) >= 100:
            grafs_list.append(graf)
    return grafs_list


def generate_filelist(data_dir):
    file_list = []
    for root, subdirs, files in os.walk(os.path.abspath(data_dir)):
        for file in files:
            if file[-3:] == "xml":
                file_list.append(os.path.join(root, file))
    return file_list


file_list = generate_filelist(data_dir)

for file in file_list:
    with open(file, 'r') as f:
        data = f.read()
    grafs = get_grafs(data)
    print(grafs)
