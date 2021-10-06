# -*- coding: utf-8 -*-
import re
import argparse


def parse_argv():
    __parse = argparse.ArgumentParser()
    __parse.add_argument("file", help="文件名")
    __parse.add_argument("--tab-identation-width", type=int, default=4, help="代码Tab缩进宽度")
    __parse.add_argument("--connection", default="DBConnection", help="DBConnection实例名称")

    return __parse.parse_args()


if __name__ == "__main__":
    argv = parse_argv()
    source_file_path = argv.file
    source_file = open(source_file_path)
    tab_identation_width = argv.tab_identation_width
    connection = argv.connection
    print(tab_identation_width)

    file_prefix_text = ""
    class_name = ""
    super_class_name = ""
    identation_component_text = " " * tab_identation_width

    variables = []
    variable_declaration_codes = []

    for item in source_file:
        if len(class_name) == 0:
            match = re.match("class .+: .+{\n", item, re.RegexFlag.DOTALL)
            file_prefix_text += item
            if match is not None:
                # 这里可能没有父类
                temp = item[6:-3].split(": ")
                class_name = temp[0]
                super_class_name = temp[1]
                print(repr(temp))
                print(class_name)
                print(super_class_name)
        else:
            if item.startswith(identation_component_text + "var "):
                print(repr(item))
                if item.endswith("{\n"):
                    continue
                variable_declaration_codes.append(item)
                temp = item[8:-1]
            elif item.startswith(identation_component_text + "@objc var "):
                print(repr(item))
                if item.endswith("{\n"):
                    continue
                variable_declaration_codes.append(item)
                temp = item[14:-1]
            else:
                continue
            temp = temp.replace(" ", "")
            temp = "".join(re.split("//.+", temp))
            if temp.__contains__("="):
                if temp.__contains__(":"):
                    temp = temp.split("=")[0]
                    items = temp.split(":")
                    variables.append((items[0], items[1]))
                else:
                    items = temp.split("=")
                    variable_type = ""
                    if re.match("\\d+", items[1]) is not None:
                        variable_type = "Int"
                    elif re.match("\".?\"", items[1], re.RegexFlag.DOTALL):
                        variable_type = "String"
                    elif re.match(".+\\(\\)", items[1], re.RegexFlag.DOTALL):
                        variable_type = items[1][:-2]
                    elif re.match("true|false", items[1]):
                        variable_type = "Bool"
                    else:
                        print("暂不支持的变量声明格式: {0}".format(item))
                        continue
                    variables.append((items[0], variable_type))
            elif temp.__contains__(":"):
                items = temp.split(":")
                variables.append((items[0], items[1]))
            else:
                print("暂不支持的变量声明格式: {0}".format(item))
                continue

    source_file.close()
    if len(variables) == 0:
        print("没有找到声明的变量")
        exit(0)

    source_file = open(source_file_path, "wt")
    source_file.write(file_prefix_text)
    source_file.write("\n")
    for item in variable_declaration_codes:
        source_file.write(item)
    # TableColum
    source_file.write("\n")
    source_file.write(identation_component_text + "struct TableColumn {\n")
    for item in variables:
        print(item[0])
        print(item[1])
        source_file.write(identation_component_text*2 + "static let {0} = Expression<{1}>(\"{0}\")\n".format(item[0], item[1]))
    source_file.write(identation_component_text + "}\n")

    source_file.write("\n")
    source_file.write( identation_component_text + "static let table = Table(\"{0}\")\n".format(class_name))

    # create
    source_file.write("\n")
    source_file.write(identation_component_text + "static var create = {\n")
    source_file.write(identation_component_text*2 + "\n")
    source_file.write(identation_component_text*2 + "return table.create(temporary: false, ifNotExists: true, withoutRowid: false) {\n")
    for item in variables:
        source_file.write(identation_component_text*3 + "$0.column(TableColumn.{0})\n".format(item[0]))
    source_file.write(identation_component_text*2 + "}\n")
    source_file.write(identation_component_text + "}()\n")

    # all
    source_file.write("\n")
    source_file.write(identation_component_text + "static func all(_ predicate: Expression<Bool> = Expression<Bool>.init(value: true)) -> [{0}] ".format(class_name) + "{\n")
    source_file.write(identation_component_text * 2 + "\n")
    source_file.write(identation_component_text * 2 + "do {\n")
    source_file.write(identation_component_text * 3 + "let items = try {0}.prepare({1}.table.filter(predicate))\n".format(connection, class_name))
    source_file.write(identation_component_text * 3 + "let models = items.map({ " + "row -> {0} in\n".format(class_name))
    source_file.write(identation_component_text * 4 + "let item = {0}()\n".format(class_name))
    for item in variables:
        source_file.write(identation_component_text * 4 + "item.{0} = row[TableColumn.{0}]\n".format(item[0]))
    source_file.write(identation_component_text * 4 + "return item\n")
    source_file.write(identation_component_text * 3 + "})\n")
    source_file.write(identation_component_text * 3 + "return models\n")
    source_file.write(identation_component_text * 2 + "} catch {\n")
    source_file.write(identation_component_text * 3 + "print(error)\n")
    source_file.write(identation_component_text * 3 + "return []\n")
    source_file.write(identation_component_text * 2 + "}\n")
    source_file.write(identation_component_text + "}\n")

    # insert
    source_file.write("\n")
    source_file.write(identation_component_text + "func insert() throws {\n")
    source_file.write(identation_component_text * 2 + "\n")
    source_file.write(identation_component_text * 2 + "do {\n")
    source_file.write(identation_component_text * 3 + "let insert = {0}.table.insert(\n".format(class_name))
    for i in range(len(variables)):
        item = variables[i]
        source_file.write(identation_component_text * 4 + "TableColumn.{0} <- self.{0}".format(item[0]))
        if i == len(variables) - 1:
            source_file.write("\n")
        else:
            source_file.write(",\n")
    source_file.write(identation_component_text * 3 + ")\n")
    source_file.write(identation_component_text * 3 + "try {0}.run(insert)\n".format(connection))
    source_file.write(identation_component_text * 2 + "} catch {\n")
    source_file.write(identation_component_text * 3 + "print(error)\n")
    source_file.write(identation_component_text * 3 + "throw error\n")
    source_file.write(identation_component_text * 2 + "}\n")
    source_file.write(identation_component_text + "}\n")

    # delete
    source_file.write("\n")
    source_file.write(identation_component_text + "static func delete(_ predicate: Expression<Bool> = Expression<Bool>.init(value: true)) throws {\n")
    source_file.write(identation_component_text * 2 + "\n")
    source_file.write(identation_component_text * 2 + "do {\n")
    source_file.write(identation_component_text * 3 + "let delete = {0}.table.filter(predicate).delete()\n".format(class_name))
    source_file.write(identation_component_text * 3 + "try {0}.run(delete)\n".format(connection))
    source_file.write(identation_component_text * 2 + "} catch {\n")
    source_file.write(identation_component_text * 3 + "print(error)\n")
    source_file.write(identation_component_text * 3 + "throw error\n")
    source_file.write(identation_component_text * 2 + "}\n")
    source_file.write(identation_component_text + "}\n")

    # update
    source_file.write("\n")
    source_file.write(identation_component_text + "func update(_ predicate: Expression<Bool> = Expression<Bool>.init(value: true)) throws {\n")
    source_file.write(identation_component_text * 2 + "\n")
    source_file.write(identation_component_text * 2 + "do {\n")
    source_file.write(
        identation_component_text * 3 + "let update = {0}.table.filter(predicate).update(\n".format(class_name))
    for i in range(len(variables)):
        item = variables[i]
        source_file.write(identation_component_text * 4 + "TableColumn.{0} <- self.{0}".format(item[0]))
        if i == len(variables) - 1:
            source_file.write("\n")
        else:
            source_file.write(",\n")
    source_file.write(identation_component_text * 3 + ")\n")
    source_file.write(identation_component_text * 3 + "try {0}.run(update)\n".format(connection))
    source_file.write(identation_component_text * 2 + "} catch {\n")
    source_file.write(identation_component_text * 3 + "print(error)\n")
    source_file.write(identation_component_text * 3 + "throw error\n")
    source_file.write(identation_component_text * 2 + "}\n")
    source_file.write(identation_component_text + "}\n")

    # exist
    source_file.write("\n")
    source_file.write(identation_component_text + "static func exist(_ predicate: Expression<Bool> = Expression<Bool>.init(value: true)) -> Bool {\n")
    source_file.write(identation_component_text * 2 + "\n")
    source_file.write(identation_component_text * 2 + "do {\n")
    source_file.write(
        identation_component_text * 3 + "let items = try {0}.prepare({1}.table.filter(predicate))\n".format(connection, class_name))
    source_file.write(identation_component_text * 3 + "return items.first(where: { _ in true }) != nil\n")
    source_file.write(identation_component_text * 2 + "} catch {\n")
    source_file.write(identation_component_text * 3 + "print(error)\n")
    source_file.write(identation_component_text * 3 + "return false\n")
    source_file.write(identation_component_text * 2 + "}\n")
    source_file.write(identation_component_text + "}\n")

    # first item
    source_file.write("\n")
    source_file.write(identation_component_text + "static func firstItem(_ predicate: Expression<Bool> = Expression<Bool>.init(value: true)) -> {0}? ".format(class_name) + "{\n")
    source_file.write(identation_component_text * 2 + "\n")
    source_file.write(identation_component_text * 2 + "do {\n")
    source_file.write(identation_component_text * 3 + "let items = try {0}.prepare({1}.table.filter(predicate))\n".format(connection, class_name))
    source_file.write(identation_component_text * 3 + "if let item = items.first(where: { _ in true }) {\n")
    source_file.write(identation_component_text * 4 + "let model = {0}()\n".format(class_name))
    for item in variables:
        source_file.write(identation_component_text * 4 + "model.{0} = item[TableColumn.{0}]\n".format(item[0]))
    source_file.write(identation_component_text * 4 + "return model\n")
    source_file.write(identation_component_text * 3 + "}else {\n")
    source_file.write(identation_component_text * 4 + "return nil\n")
    source_file.write(identation_component_text * 3 + "}\n")
    source_file.write(identation_component_text * 2 + "} catch {\n")
    source_file.write(identation_component_text * 3 + "print(error)\n")
    source_file.write(identation_component_text * 3 + "return nil\n")
    source_file.write(identation_component_text * 2 + "}\n")
    source_file.write(identation_component_text + "}\n")

    source_file.write("}\n")
    source_file.close()
