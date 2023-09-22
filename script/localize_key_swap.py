

# 场景说明
# 平常开发，本地化使用的key值是中文，但是有一天要求将demo提供给外国人
# 此时使用中文作为key是不合适的，但是可以使用这个脚本将key转换为英文翻译文件中的英文(根据实际情况)
# 将项目中的对应本地化代码进行相应替换
# 翻译文件的值不能为空字符
import os


# 加载翻译文件内容
def load_localize_content(strings_file_path: str):
    content = dict()
    with open(strings_file_path) as file:
        for line in file:
            pairs = line.split(' = ')
            if len(pairs) == 2:
                if pairs[0].startswith('"'):
                    key = pairs[0][1:-1]
                else:
                    key = pairs[0]
                content[key] = pairs[1][1:-3]
    return content


def find_code_file(path: str, code_suffix: str, function):
    file_list = os.listdir(path)
    for item in file_list:
        path_new = path + "/" + item
        if os.path.isdir(path_new):
            find_code_file(path_new, code_suffix, function)
        elif os.path.isfile(path_new):
            if item.endswith(code_suffix):
                function(path_new)
        else:
            break


if __name__ == '__main__':
    path = "/Users/ldc/Desktop/git/KJZink/KJZink"
    strings_path = "/Users/ldc/Desktop/git/KJZink/KJZink/Resource/en.lproj/Localizable.strings"
    paths = list()
    find_code_file(path, '.swift', lambda result: paths.append(result))
    # print(paths)
    key_value_map = load_localize_content(strings_path)
    value_key_map = dict()
    for key in key_value_map.keys():
        print(key)
        value_key_map[key_value_map[key]] = key

    for path in paths:
        content = list()
        with open(path) as file:
            for line in file.readlines():
                temp = line
                for key in key_value_map.keys():
                    temp = temp.replace(key, key_value_map[key])
                content.append(temp)
        with open(path, mode="wt") as file:
            file.writelines(content)

    with open(strings_path, mode="wt") as file:
        for key in value_key_map.keys():
            file.write('"{0}" = "{1}";\n'.format(key, value_key_map[key]))
