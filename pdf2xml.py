import requests
import config
import time
import argparse
import os


grobid_address = config.grobid['host']
grobid_path = config.grobid['path']
grobid_port = config.grobid['port']


aParser = argparse.ArgumentParser(
    description='Convert PDFs to TEI XML.')

aParser.add_argument(
    "-i",
    "--in-dir",
    required=True,
    help="Directory with PDFs")

aParser.add_argument(
    "-o",
    "--out-dir",
    required=True,
    help="Directory where output files will be stored.")


settings = vars(aParser.parse_args())
in_dir = settings["in_dir"]
out_dir = settings["out_dir"]


def grobid(file_path, grobid_address, grobid_path, grobid_port):

    payload = {'input': file_path}
    data = {'consolidateHeader': '0',
            'consolidateCitations': '0'
            }

    try:
        endpoint = "http://{0}/:{1}{2}/api/processFulltextDocument".format(
            grobid_address,
            grobid_port,
            grobid_path
        )

        response = requests.post(endpoint,
                                 files=payload,
                                 data=data,
                                 timeout=1200)
        status_code = response.status_code

        if status_code == 503:
            time.sleep(1)
            return grobid(file_path, grobid_address, grobid_path, grobid_port)

        if status_code != 200:
            raise Exception("""
                            GROBID could not process document,
                            returned status code %r
                            """ % status_code)

        working_xml = response.content.decode("utf-8")
        return working_xml
    except requests.exceptions.ConnectionError as e:
        print("GROBID connection error. Is it running?")
        raise e


def write_output(filename, data):
    xml_filename = filename + ".xml"
    with open(xml_filename, 'w') as f:
        f.write(data)


for filename in os.listdir(in_dir):
    xml = grobid(filename, grobid_address, grobid_path, grobid_port)
    write_output(filename, xml)
