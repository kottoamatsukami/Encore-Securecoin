from PIL import Image, ImageFont


class ASCIIAnimator(object):

    def __init__(self, intensity_multiplier: int) -> None:
        assert intensity_multiplier > 0 and isinstance(intensity_multiplier, int)
        self.intensity_multiplier = intensity_multiplier

    def get_ascii_art_from_image(self, image_path: str) -> str:
        image = Image.open(image_path)
        ascii_image = self.__convert_image_to_ascii(image)
        return ascii_image

    def __convert_image_to_ascii(self, image):
        font = ImageFont.load_default()
        _, _, chr_x, chr_y = font.getbbox(chr(32))
        weights = []
        for i in range(32, 127):
            chr_image = font.getmask(chr(i))
            ctr = 0
            for y in range(chr_y):
                for x in range(chr_x):
                    if chr_image.getpixel((x, y)) > 0:
                        ctr += 1
            weights.append(float(ctr) / (chr_x * chr_y))

        output = ""
        img_x, img_y = image.size
        img_x, img_y = int(img_x / chr_x), int(img_y / chr_y)
        pixels = image.resize((img_x, img_y), Image.BICUBIC).convert("L").load()
        for y in range(img_y):
            for x in range(img_x):
                w = float(pixels[x, y]) / 255 / self.intensity_multiplier
                wf = -1.0
                k = -1
                for i in range(len(weights)):
                    if abs(weights[i] - w) <= abs(wf - w):
                        wf = weights[i]
                        k = i
                output += chr(k + 32)
            output += "\n"
        return output