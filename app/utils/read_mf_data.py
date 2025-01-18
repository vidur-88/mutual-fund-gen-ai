from pathlib import Path
import pandas as pd

from app.utils.excel_to_json import map_data_to_scheme_name


class ReadMFData(object):
    def __init__(self):
        self.all_files_path = []
        self.data_based_on_scheme_name = {}

    def get_all_files(self, root_dir):
        path = Path(root_dir)
        for file_path in path.iterdir():
            if file_path.is_file():
                self.all_files_path.append(file_path)
            else:
                self.get_all_files(file_path)

    def read_mf_data(self):
        for file_path in self.all_files_path:
            # print(file_path, file_path.name)
            if "xlsx" in file_path.name:
                # print(file_path)
                pd_mf_data = pd.read_excel(file_path)
                map_data_to_scheme_name(self.data_based_on_scheme_name, pd_mf_data)

    def get_mf_data(self):
        return list(self.data_based_on_scheme_name.values())


if __name__ == "__main__":
    rmf = ReadMFData()
    rmf.get_all_files("../../resource")
    print(len(rmf.all_files_path))
    rmf.read_mf_data()
    print(rmf.get_mf_data())
