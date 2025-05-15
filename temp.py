from tk_base_utils import get_abs_file_path
import pandas as pd

file_path_str  = '$/src/tk_openai_sdk_agent/data/ip名称聚类.xlsx'
file_path = get_abs_file_path(file_path_str)

sheets = pd.read_excel(file_path, sheet_name=None)

count = 0
all_data = []
# 遍历每个 Sheet 的数据
for sheet_name, data in sheets.items():
  all_data.append(data)

df = pd.concat(all_data, ignore_index=True)

print(f'{df}')
