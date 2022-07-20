# -*- coding: utf-8 -*-


import argparse
import os
import shutil
# from script import ShellCommand
import subprocess
import re
import time

identity = "com.idprt.tspl.printer.mac.driver"
version = "1.3.3"
bundle_name = "idprt-tspl-printer-mac-driver"
codesign_identity = "Developer ID Application: Xiamen Hanin Electronic Technology Co., Ltd. (976NLVLZMW)"
install_sign_identity = "Developer ID Installer: Xiamen Hanin Electronic Technology Co., Ltd. (976NLVLZMW)"
developer_name = "ios@prttech.com"
developer_password = "solr-vnoz-tzpu-pdmr"
developer_team = "976NLVLZMW"

# 删除build文件
# 遍历/filter文件下目录使用make编译执行文件
# 当前目录make build将上一次生成二进制文件复制到/roots/usr/libexec/cups/filter目录
# ppd文件压缩
# 遍历/roots/usr/libexec/cups/filter文件夹下执行文件，添加权限，代码签名
# /scripts目录遍历脚本，添加权限
# pkgbuild生成安装包->pkgbuild生成卸载安装包
# productbuild打包并签名
# xcrun请求包认证
# 循环查询认证结果


def excute_shell(command: str, verbose: bool = False):
    params = {"text": True}
    program = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, **params)
    outputs = []
    while program.poll() is None:
        # 当程序退出时，似乎会读取到一个空字符串
        item = program.stdout.readline()
        if verbose:
            print(item, end="")
        outputs.append(item)
    return program.returncode, "".join(outputs)


def parse_argv():
    __parse = argparse.ArgumentParser()
    __parse.add_argument("--identity", required=True, help="包id")
    __parse.add_argument("--version", required=True, help="版本")
    __parse.add_argument("--bundle_name", required=True, help="包名")
    __parse.add_argument("--codesign_identity", help="代码签名id")
    __parse.add_argument("--install_sign_identity", help="安装包签名id")
    __parse.add_argument("--developer_account", help="开发账号")
    __parse.add_argument("--developer_password", help="开发账号密码")
    __parse.add_argument("--developer_team", help="开发团队id")
    __parse.add_argument("--skip-rebuild-filter", help="是否重新编译filter文件夹", action="store_true")
    __parse.add_argument("--skip-notarize", help="是否公证pkg文件，测试使用", action="store_true")

    return __parse.parse_args()


def get_notarize_info(request_uuid: str, function):
    global developer_name, developer_password
    notarize_result_cmd = "xcrun altool --notarization-info {0} " \
                          "--username {1} " \
                          "--password {2}"
    notarize_result_cmd = notarize_result_cmd.format(request_uuid, developer_name, developer_password)
    print("查询认证结果")
    flag, result = excute_shell(notarize_result_cmd, verbose=True)
    if flag != 0:
        print("认证信息查询失败")
        exit(-1)
    pairs = re.findall("\\w[^\\n]*?: [^\\n]+", result, re.RegexFlag.DOTALL)
    dic = dict()
    for pair in pairs:
        items = pair.split(": ")
        dic[items[0]] = items[1]
    status = dic["Status"]
    if status is None:
        print("notarization info Status not found")
        exit(-1)
    else:
        if status == "in progress":
            print("稍后查询...")
            time.sleep(30)
            get_notarize_info(request_uuid, function)
        elif status == "success":
            function(dic)
        else:
            exit(-1)


def staple_ticket(package: str, notarize_info: dict):
    # 打开安装包目录
    os.system("open {0}".format(notarize_info["LogFileURL"]))
    cmd = "xcrun stapler staple {0}".format(package)
    print(cmd)
    flag, result = excute_shell(cmd, verbose=True)
    if flag != 0:
        exit(-1)


if __name__ == '__main__':

    if not os.path.exists("build"):
        os.mkdir("build")

    argv = parse_argv()

    identity = argv.identity
    version = argv.version
    bundle_name = argv.bundle_name

    if argv.codesign_identity is not None:
        codesign_identity = argv.codesign_identity

    if argv.install_sign_identity is not None:
        install_sign_identity = argv.install_sign_identity

    if argv.developer_account is not None:
        developer_account = argv.developer_account

    if argv.developer_password is not None:
        developer_password = argv.developer_password

    if argv.developer_team is not None:
        developer_team = argv.developer_team

    home = subprocess.getoutput("pwd")

    if not argv.skip_rebuild_filter:
        src_dir = home + "/filter"
        for src in os.listdir(src_dir):
            item_path = "{0}/{1}".format(src_dir, src)
            print(item_path)
            if os.path.isdir(item_path):
                cmd = "cd {0};make clean;make".format(item_path)
                print(cmd)
                flag, result = excute_shell(cmd)
                if flag != 0:
                    print("{0} 失败".format(cmd))
                    exit(-1)

    cmd = "make clean;make build"
    print(cmd)
    flag, result = excute_shell(cmd)
    if flag != 0:
        print("{0} make clean;make build 失败".format(home))
        exit(-1)

    ppd_dir = "{0}/roots/Library/Printers/PPDs/Contents/Resources".format(home)

    for item in os.listdir(ppd_dir):
        if item.endswith(".ppd"):
            cmd = "gzip {0}/{1}".format(ppd_dir, item)
            print(cmd)
            os.system(cmd)

    code_dir = "{0}/roots/usr/libexec/cups/filter".format(home)
    for item in os.listdir(code_dir):
        if item.startswith("."):
            continue
        item_path = code_dir + "/" + item

        cmd = "chmod 755 {0}".format(item_path)
        print(cmd)
        flag, result = excute_shell(cmd, verbose=True)
        if flag != 0:
            print("{0}文件权限修改失败".format(item))
            exit(-1)

        cmd = "codesign --force --verify --verbose " \
              "--sign \"{0}\" " \
              "{1} --deep --options runtime --timestamp"
        cmd = cmd.format(codesign_identity, item_path)
        print(cmd)
        flag, result = excute_shell(cmd, verbose=True)
        if flag != 0:
            print("{0}代码签名失败".format(item))
            exit(-1)

    # 给脚本文件添加权限
    script_path = "{0}/scripts".format(home)
    for item in os.listdir(script_path):
        if item.startswith("."):
            continue
        script_dir = script_path + "/" + item
        print(script_dir)
        for script_item in os.listdir(script_dir):
            if script_item.startswith("."):
                continue
            item_path = script_dir + "/" + script_item
            print(item_path)
            cmd = "chmod 755 {0}".format(item_path)
            print(cmd)
            flag, result = excute_shell(cmd, verbose=True)
            if flag != 0:
                print("{0}文件权限修改失败".format(item))
                exit(-1)

    install_cmd = "pkgbuild " \
                  "--root roots/ " \
                  "--scripts scripts/install " \
                  "--identifier {0}.Install " \
                  "--version {1} " \
                  "--ownership recommended " \
                  "build/{2}.pkg"
    install_cmd = install_cmd.format(identity, version, bundle_name)
    print(install_cmd)
    flag, result = excute_shell(install_cmd, verbose=True)
    if flag != 0:
        print("Install包导出失败")
        exit(-1)

    uninstall_cmd = "pkgbuild " \
                    "--nopayload " \
                    "--scripts scripts/uninstall " \
                    "--identifier {0}.Uninstall " \
                    "--version {1} " \
                    "--ownership recommended " \
                    "build/uninstall-{2}.pkg"
    uninstall_cmd = uninstall_cmd.format(identity, version, bundle_name)
    print(uninstall_cmd)
    flag, result = excute_shell(uninstall_cmd, verbose=True)
    if flag != 0:
        print("Uninstall包导出失败")
        exit(-1)

    result_pkg = "{0}-v{1}.pkg".format(bundle_name, version)
    package_cmd = "productbuild " \
                  "--distribution Distribution.xml " \
                  "--package-path build " \
                  "--resources resources " \
                  "--identifier {0} " \
                  "--version {1} " \
                  "--sign \"{2}\" " \
                  "build/{3}"
    package_cmd = package_cmd.format(identity, version, install_sign_identity, result_pkg)
    print(package_cmd)
    flag, result = excute_shell(package_cmd, verbose=True)
    if flag != 0:
        print("打包失败")
        exit(-1)

    if not argv.skip_notarize:
        notarize_cmd = "xcrun altool --notarize-app " \
                       "--primary-bundle-id {0} " \
                       "--username {1} " \
                       "--password {2} " \
                       "--file build/{3} " \
                       "-itc_provider {4} &> tmp"
        notarize_cmd = notarize_cmd.format(identity, developer_name, developer_password, result_pkg,
                                           developer_team)
        print(notarize_cmd)
        flag, result = excute_shell(notarize_cmd, verbose=True)
        if flag != 0:
            print("包认证失败")
            exit(-1)

        file = open("tmp")
        request_uuid = ""
        for item in file:
            if item.startswith("RequestUUID = "):
                items = item.split(" = ")
                print(items)
                request_uuid = items[1][:-1]
        if len(request_uuid) == 0:
            print("RequestUUID not found in tmp")
            exit(-1)

        get_notarize_info(request_uuid,
                          lambda info: staple_ticket("build/{0}".format(result_pkg), info))
