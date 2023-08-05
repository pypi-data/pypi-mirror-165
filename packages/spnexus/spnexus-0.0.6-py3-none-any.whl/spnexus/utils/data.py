from .base import UtilBase


class CsvUtil(UtilBase):
    
    @staticmethod
    def load_csv(csv_path: str, field_definition: dict) -> list or bool:
        import csv
        import os
        from .dict import DictUtil

        if not len(str(csv_path).strip()):
            print(f'The import path is empty!')
            return False

        if not os.path.exists(csv_path):
            print(f'The import path does not exist. ({csv_path})')
            return False

        if not os.access(csv_path, os.R_OK):
            print(f'The import path can not be read by this process. ({csv_path})')
            return False

        csv_lines = []

        with open(csv_path, 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for line in reader:
                csv_lines.append(line)
            f.close()

        if not len(csv_lines):
            print(f'The import file is empty! ({csv_path})')
            return False

        header_included: bool = False

        if isinstance(csv_lines[0], list):
            for value in csv_lines[0]:
                if value in field_definition:
                    header_included = True

        if header_included:
            ordered_fields: list = ['_' if line == '' else line for line in csv_lines[0]]
            csv_lines.pop(0)
            print(f'Header row was detected. ({",".join(ordered_fields)})')
        else:
            ordered_fields: list = list(field_definition.keys())
            print(f'Header row was not detected, using default. ({",".join(ordered_fields)})')

        total_fields = len(ordered_fields)
        lines = []
        line_number: int = 1 if header_included else 0
        fi = DictUtil.index_fields(ordered_fields)

        for line in csv_lines:
            line_number += 1
            if len(line) != total_fields:
                print(f'The CSV file at {csv_path} has an invalid row at line {line_number}.')
                continue

            lines.append(DictUtil.map_fields(fi, line))

        return lines
