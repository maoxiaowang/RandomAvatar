# coding=utf-8
import os
import random
from datetime import datetime

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
                 (3,))
        return random.choice(modes)

    @staticmethod
    def _file_name(size):
        """
        Generate a name for avatar image file
        Simply use datetime string as filename, jpg as suffix
        :return:
        """
        datetime_str = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return '%s_%dx%d.%s' % (datetime_str, size, size, 'jpg')

    def generate_avatar(self, size, fp, min_border=10):
        """
        Generate a random square avatar
        :param size: width / height (px)
        :param min_border: px
        :param fp: where new image file to save, without filename
        :return: a new file name
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
                    for y in range(chunk*h, chunk*(h+1)):
                        draw.point((x, y), fill=color)

        fn = self._file_name(size)
        new_avatar = os.path.join(fp, fn)
        new_image.save(new_avatar, 'jpeg')
        return new_avatar

    def generate_avatar_thumbs(self, avatar, sizes=(40, 100)):
        """
        Generate avatar thumbs, like 100x100, 40x40
        :param avatar: avatar file path
        :param sizes: sizes of avatar thumbs to be generated
        """
        thumbs = []

        for size in sizes:
            assert isinstance(size, int), 'Integers are expected'
        img = Image.open(avatar)
        path = os.path.dirname(avatar)
        for size in sizes:
            filename = self._file_name(size)
            new_img = img.resize((size, size), Image.ANTIALIAS)
            _ = os.path.join(path, filename)
            new_img.save(_)
            thumbs.append(_)
        return thumbs


if __name__ == '__main__':
    a = Avatar()
    _ = a.generate_avatar(256, '')
    a.generate_avatar_thumbs(_)
