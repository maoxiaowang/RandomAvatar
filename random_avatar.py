# coding=utf-8
import os
import random
import time

from PIL import Image, ImageDraw


class UnavailableSize(Exception):
    pass


class Avatar(object):

    def __init__(self):
        pass

    @property
    def _random_color(self):
        return (random.randint(64, 192),
                random.randint(64, 192),
                random.randint(64, 192))

    @property
    def _random_mode(self):
        """
        There are five rows and columns of pixel chunks,
        therefor several fill mode could be used.
        """
        modes = ((1, 2, 3, 4, 5),
                 (1, 2, 4, 5),
                 (2, 3, 4),
                 (1, 3, 5),
                 (1, 5),
                 (2, 4),
                 (3,),
                 ())
        return random.choice(modes)

    @staticmethod
    def _file_name(size):
        """
        Generate a name for avatar image file
        Simply use datetime string as filename, jpg as suffix
        :return:
        """
        timestamp = str(int(time.time()))
        return '%s_%dx%d.%s' % (timestamp, size, size, 'jpg')

    def generate_avatar(self, fp, fn, size=256, min_border=10):
        """
        Generate a random square avatar
        :param size: width / height (px)
        :param min_border: px
        :param fp: path the new image file to save
        :param fn: new file name
        :return: path of new image
        """
        assert isinstance(size, int), 'Size is expected as a integer'

        # size - 2*border = chunk*5
        border = chunk = None
        for chunk in reversed(range(1, size)):
            border = (size - (chunk*5)) / 2
            # check if border is an integer larger than min border
            if str(border).split('.')[1] == '0' and border >= min_border:
                border = int(border)
                break
        if border is None:
            raise UnavailableSize

        new_image = Image.new('RGB', (size, size), (255, 255, 255))
        draw = ImageDraw.Draw(new_image)

        # fill new image with random color
        color = self._random_color
        for h in range(5):
            # get random fill mode for per chunk of columns
            mode = self._random_mode
            for i in mode:
                for x in range((border+1) + (i-1)*chunk, (border+1) + i*chunk):
                    for y in range((border + 1) + chunk * h, (border + 1) + chunk * (h + 1)):
                        draw.point((x, y), fill=color)

        new_avatar = os.path.join(fp, fn)
        if fp and not os.path.exists(fp):
            os.makedirs(fp)
        new_image.save(new_avatar, 'jpeg')
        return new_avatar

    @staticmethod
    def generate_thumb(origin, size, fn):
        """
        Generate avatar thumbs from avatar, like 100x100, 40x40
        :param origin: original avatar file path
        :param size: size of avatar thumbs to be generated
        :param fn: new filename
        """
        assert isinstance(size, int), 'Integers are expected'
        img = Image.open(origin)
        path = os.path.dirname(origin)

        new_img = img.resize((size, size), Image.ANTIALIAS)
        thumb_path = os.path.join(path, fn)
        new_img.save(thumb_path)
        return thumb_path


if __name__ == '__main__':
    a = Avatar()
    WORKING_DIR = r'D:\test'
    avatar = a.generate_avatar(fp=WORKING_DIR, fn='avatar.jpg', size=256)
    a.generate_thumb(avatar, size=100, fn='avatar_thumb_100x100.jpg')
    a.generate_thumb(avatar, size=40, fn='avatar_thumb_40x40.jpg')
