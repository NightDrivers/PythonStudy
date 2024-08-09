from PIL import Image


if __name__ == '__main__':
    home = "/Users/ldc/Downloads"
    icon_image_path = "{0}/{1}".format(home, "1024x1024.png")
    img = Image.open(icon_image_path)
    # size_list = [40, 58, 60, 76, 80, 87, 114, 120, 128, 136, 152, 167, 180, 192]
    size_list = [16, 32, 64, 128, 256, 512]
    for size in size_list:
        print(size)
        dst_image = img.resize((size, size))
        dst_image.save("{0}/icon_{1}_{1}.png".format(home, size))