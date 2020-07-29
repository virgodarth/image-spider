import io
import os
import sys

from PIL import Image


class ImageHandler:
    _image = None

    def __init__(self):
        pass

    def from_file(self, path: str):
        self._image = Image.open(path, 'r')

    def from_bytes(self, datum):
        self._image = Image.open(io.BytesIO(datum))

    def resize_by_width(self, widths, has_save: bool = False, output_dir: str = ''):
        img_sizes = [(width, int(width/self._image.width*self._image.height)) for width in widths]
        return self.resize(img_sizes, has_save, output_dir)

    def resize_by_length(self, heights, has_save: bool = False, output_dir: str = ''):
        img_sizes = [(int(height / self._image.height * self._image.width), height) for height in heights]
        return self.resize(img_sizes, has_save, output_dir)

    def resize(self, image_sizes, has_save: bool = False, output_dir: str = ''):
        resized_images = []
        for img_size in image_sizes:
            resized_image = self._image.resize(img_size)
            resized_images.append(resized_image)

            # save image
            if has_save:
                file_title, ext = os.path.splitext(self._image.filename)
                sep = '/' if sys.platform.startswith('linux') else '\\'
                org_path, filename = file_title.rsplit(sep, 1) if sep in file_title else '', file_title

                if output_dir:
                    org_path = output_dir

                base_filename = os.path.join(org_path, '{filename}_{height}x{width}{ext}')

                resized_image.save(base_filename.format(
                    filename=filename,
                    height=img_size[0],
                    width=img_size[1],
                    ext=ext))

        return resized_images

    def save(self, full_path: str = None):
        if not full_path:
            full_path = self._image.filename
        self._image.save(full_path)


if __name__ == '__main__':
    width_sizes = (24, 32, 64, 224, 480)
    img_path = 'C:\\VuMai\\YouTradeBackend\\youtrade_spider\\scripts\\abcdef_xyz.jpg'
    output_path = 'C:\\Users\\USER\\Desktop'

    if not os.path.exists(img_path) or not os.path.exists(output_path):
        raise FileExistsError('File path is not exists.')

    image_hdl = ImageHandler()
    image_hdl.from_file(img_path)
    image_hdl.resize_by_width(width_sizes, True, output_path)
