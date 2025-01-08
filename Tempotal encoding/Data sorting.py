import os
import csv

def load_label_map(label_map_path):
    label_map = {}
    with open(label_map_path, 'r') as f:
        for line in f:
            number, label = line.strip().split()
            label_map[int(number)] = label
    return label_map

def findSortedPosition(theList, target):
    low = 0
    high = len(theList) - 1
    while low <= high:
        mid = (high + low) // 2
        if theList[mid] == target:
            return mid
        elif target < theList[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return low

def process_txt_files(txt_folder, label_map_path, output_folder):
    label_map = load_label_map(label_map_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for txt_file in os.listdir(txt_folder):
        if txt_file.endswith('.txt'):
            txt_path = os.path.join(txt_folder, txt_file)
            output_csv_path = os.path.join(output_folder, txt_file.replace('.txt', '.csv'))
            process_single_txt(txt_path, label_map, output_csv_path)

def process_single_txt(txt_path, label_map, output_csv_path):
    C = ['Gclef', 'Fclef', 'Cclef', 'High_Gclef', 'DHigh_Gclef', 'Lower_Gclef', 'DLower_Gclef', 'Soprano_Cclef',
         'M_Soprano_Cclef', 'Tensor_Cclef', 'High_Fclef', 'DHigh_Fclef', 'Lower_Fclef', 'DLower_Fclef', 'Tensor_Fclef']
    cc = []
    math_list = []
    Name_y_x = []

    with open(txt_path, 'r') as f:
        for line in f.readlines():
            line = line.strip().split()
            cls, X, Y, W, H = int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4])
            name = label_map.get(cls, 'Unknown')
            box_ymid = (Y + (Y + H)) / 2
            box_xmid = (X + (X + W)) / 2
            Name_y_x.append((name, box_ymid, box_xmid))

            if name in C:
                cc.append((name, Y, Y + H))

    cc = sorted(cc, key=lambda x: x[1])
    for i in range(len(cc)):
        if i > 0:
            math_list.append(((cc[i][1] + cc[i-1][2]) / 2) + 0.0001)

    _list = [[] for _ in range(len(math_list) + 1)]
    for symbol in Name_y_x:
        symbol_ymid = symbol[1]
        index = findSortedPosition(math_list, symbol_ymid)
        _list[index].append(symbol)

    with open(output_csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for ii in range(len(_list)):
            line = sorted(_list[ii], key=lambda x: x[2])
            writer.writerow([symbol[0] for symbol in line])

if __name__ == '__main__':
    txt_folder = r"D:/txtt"
    label_map_path = r"D:/shujuji/label_map.txt"
    output_folder = r"D:/csvv"
    process_txt_files(txt_folder, label_map_path, output_folder)
