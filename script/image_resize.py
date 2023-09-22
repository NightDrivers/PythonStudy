import imghdr
import json
import os
from PIL import Image


def image_file_resize(src_dir_path, dst_dir_path):
    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)
    for item in os.listdir(src_dir_path):
        relative_subpath = item
        resolute_subpath = "{0}/{1}".format(src_dir_path, item)
        if os.path.isdir(resolute_subpath):
            dst_item_dir = "{0}/{1}".format(dst_dir_path, item)
            image_names = os.listdir(resolute_subpath)
            if len(image_names) == 0:
                print("{0} 没有图片".format(resolute_subpath))
                continue
            if not os.path.exists(dst_item_dir):
                os.mkdir(dst_item_dir)
            for image_name in image_names:
                relative_image_path = "{0}/{1}".format(relative_subpath, image_name)
                resolute_image_path = "{0}/{1}".format(resolute_subpath, image_name)
                if imghdr.what(resolute_image_path) is not None:
                    img = Image.open(resolute_image_path)
                    aspect_ratio = img.width / img.height
                    min_size = 300
                    dst_image = img
                    if min(img.width, img.height) > min_size:
                        if img.width > img.height:
                            dst_height = min_size
                            dst_width = int(min_size * aspect_ratio)
                        else:
                            dst_height = int(min_size / aspect_ratio)
                            dst_width = min_size
                        dst_image = img.resize((dst_width, dst_height))
                    try:
                        if dst_image.mode == 'RGBA':
                            dst_image = dst_image.convert('RGB')
                        dst_image_name = "{0}/{1}/{2}".format(dst_dir_path, item, image_name)
                        ext = os.path.splitext(dst_image_name)[1].lower()
                        dst_image.save(dst_image_name)
                        # print("{0} ok".format(dst_image_name))
                    except Exception as e:
                        print(dst_image_name)
                        print(dst_image.mode)
                        print(ext)
                        print(e)
                    # print("width: {0} height: {1}".format(dst_width, dst_height))


def scale_image_podspec_generate():
    dic = dict()
    for item in os.listdir("./"):
        relative_subpath = item
        resolute_subpath = "./{0}".format(item)
        if os.path.isdir(resolute_subpath):
            images = list()
            for image_name in os.listdir(resolute_subpath):
                relative_image_path = "{0}/{1}".format(relative_subpath, image_name)
                resolute_image_path = "{0}/{1}".format(resolute_subpath, image_name)
                if imghdr.what(resolute_image_path) is not None:
                    images.append(image_name)
                    # print(imghdr.what(resolute_image_path))
                else:
                    os.remove(resolute_image_path)
            dic[item] = images
            print("     - assets/壹佳一图库/{0}/".format(relative_subpath))
    with open("config.json", "w") as file:
        file.write(json.dumps(dic, ensure_ascii=False))


if __name__ == '__main__':
    src_dir = "/Users/ldc/Desktop/图库图片裁剪/src/壹佳一图库"
    dst_dir = "/Users/ldc/Desktop/图库图片裁剪/dst/壹佳一图库"
    image_file_resize(src_dir, dst_dir)

