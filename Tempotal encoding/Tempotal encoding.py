import pandas as pd
import re

# 定义读取CSV文件的函数
def read_csv_with_fallback(filepath):
    delimiters = [',', ';', '\t']
    for delimiter in delimiters:
        try:
            df = pd.read_csv(filepath, header=None, delimiter=delimiter, on_bad_lines='skip')
            return df
        except pd.errors.ParserError as e:
            print(f"Failed to read with delimiter '{delimiter}': {e}")
    raise ValueError("Unable to read the CSV file with the given delimiters.")

# 读取CSV文件
df = read_csv_with_fallback("D:/csvv/IMSLP526371-PMLP165737-Seitz_Opus-13_Piano_01.csv")

# 初始化ni
ni = 0

# 用Regular Expression查找'数字_数字'格式的信息
pattern = re.compile(r'(\d+)_(-?\d+(\.\d+)*)')

# 找到'_'前的最大的数字信息，记为min(A)
max_num_before_underscore = 0
for row in df.itertuples(index=False):
    for item in row:
        if isinstance(item, str):
            match = pattern.match(item)
            if match:
                num_before_underscore = int(match.group(1))
                if num_before_underscore > max_num_before_underscore:
                    max_num_before_underscore = num_before_underscore

min_A = max_num_before_underscore

# 重新编码规则 F(ni) = (ni+1, ni+min(A)/此时'_'前的数字)
def encode(match, ni, min_A):
    num_before = int(match.group(1))
    num_after_parts = match.group(2).split('.')
    new_ni = ni + 1
    ni = ni + min_A // num_before

    encoded_parts = []
    for part in num_after_parts:
        encoded_parts.append(f"({new_ni},{ni})_{part}")

    return encoded_parts, ni

# 创建新的DataFrame以存储重新编码后的数据
new_data = []

# 重新编码
for row in df.itertuples(index=False):
    new_row = []
    for item in row:
        if isinstance(item, str):
            match = pattern.match(item)
            if match:
                encoded_parts, ni = encode(match, ni, min_A)
                new_row.extend(encoded_parts)
            else:
                new_row.append(item)
        else:
            new_row.append(item)
    new_data.append(new_row)

# 找到最宽的行，并设置所有行的列数相同
max_columns = max(len(row) for row in new_data)
for row in new_data:
    if len(row) < max_columns:
        row.extend([None] * (max_columns - len(row)))

# 将数据转换为DataFrame并保存
new_df = pd.DataFrame(new_data)
new_df.to_csv("D:/csii/lk0.csv", index=False, header=False)
