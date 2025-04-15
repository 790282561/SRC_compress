import os
import re

# 文件路径
folder_path = r'.\src_files'  # 原文件集
compression_path = r'.\src_comp'  # 压缩后文件集

# 读写参数
pattern_1 = r'(,\s*E1\s*0,\s*E2\s*0,\s*E3\s*0,\s*E4\s*0)'
pattern_2 = r'(,\s*A\s*0,\s*B\s*90,\s*C\s*-45,\s*E1\s*0,\s*E2\s*0,\s*E3\s*0,\s*E4\s*0)'
pattern_3 = r'^LIN'

# 压缩10M以上文件需要的变量
index_list = []  # 文件行数列表
content_list = []  # 文件内容列表
content_list_change = []  # 文件更改后内容列表

# 遍历文件夹
def TraversalFolder(folder_path):
    all_files_path = []
    all_files_path_size = []
    for root, dirs, files in os.walk(folder_path):
        # 遍历当前文件夹下的所有文件
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.path.getsize(file_path)
            all_files_path.append(file_path)
            all_files_path_size.append(file_size)
    return [all_files_path, all_files_path_size]

def ChangeText(file_path, pattern_1, pattern_2):
    index_list = []
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i,line in enumerate(lines):
            if re.search(pattern_2, line):
                index_list.append(i)
            else:
                pass

    filename = compression_path + "\\" + os.path.basename(file_path)  # 获取当前文件名称，用于后续文件保存命名

    n = 0
    for j in range(len(index_list)):
        if j == 0:
            pass
        elif j <= 2:
            lines[index_list[j]] = re.sub(pattern_1, '', lines[index_list[j]])
        else:
            n += 1
            print(n, len(index_list))
            lines[index_list[j]] = re.sub(pattern_2, '', lines[index_list[j]])

    lines = ''.join(lines)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(lines)

def change_num(text, num):
    result = re.split(r'[{}]+', text)
    a = result[1].split(',')

    if num <= 1:
        a[3],a[4],a[5] = ' A 0', ' B 90', ' C -45'
    elif num > 1:
        del a[3:6]
    b = ','.join(a)
    c = f"{result[0]}{{{b}}}{result[2]}"
    return c

if __name__ == '__main__':
    files = TraversalFolder(folder_path)[0]
    for f in files:
        ChangeText(f, pattern_1, pattern_1)


    files_compress, files_compress_size = TraversalFolder(compression_path)
    for i in range(len(files_compress_size)):
        if files_compress_size[i] > 9996374:  # 1兆文件为1048576字节，因此9.6兆文件为9996374
            file_path = files_compress[i]
            print(file_path + ' 该文件过大需要垂直打印')
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if re.search(pattern_3, line):
                        content_list.append(line)
                        index_list.append(i)
                    else:
                        pass
            for i in range(len(content_list)):
                content_list_change.append(change_num(content_list[i], i))

            # 输出结果
            for j in range(len(index_list)):
                lines[index_list[j]] = content_list_change[j]

            lines = ''.join(lines)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(lines)

            # 每次压缩文件后，清空列表
            index_list.clear()
            content_list.clear()
            content_list_change.clear()