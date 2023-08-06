from hwp5.xmlmodel import Hwp5File
from hwp5.proc.xml import xmldump_nested


class BytesData:
    def __init__(self):
        self.data = b""

    def write(self, bytechunk):
        self.data += bytechunk


def hwp_to_xmlstr(hwp_file_path):
    try:
        hwp = Hwp5File(hwp_file_path)
        out = BytesData()
        xmldump_nested(hwp, out)

        return out.data.decode("utf8")
    except:
        with open(hwp_file_path, "r") as f:
            return f.read()
