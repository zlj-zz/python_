from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont


class WatermarkStorage(FileSystemStorage):
    """Docstring for WatermarkStorage. """
    def save(self, name, content, max_length=None):
        """TODO: Docstring for save.

        :name: TODO
        :content: TODO
        :max_length: TODO
        :returns: TODO

        """
        if 'image' in content.content_type:
            # 添加水印
            image = self.watermark_with_text(content, 'zachary.com', 'red')
            content = self.convert_image_to_file(image, name)

        return super().save(name, content, max_length=max_length)

    def convert_image_to_file(self, image, name):
        """TODO: Docstring for convert_image_to_file.

        :image: TODO
        :name: TODO
        :returns: TODO

        """
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size,
                                    None)

    def watermark_with_text(self, file_obj, text, color, fontfamily=None):
        """TODO: Docstring for watermark_with_text.

        :file_obj: TODO
        :text: TODO
        :color: TODO
        :fontfamily: TODO
        :returns: TODO

        """
        image = Image.open(file_obj).convert('PGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        textWidth, textHeight = draw.textsize(text, font)
        # 计算横、纵轴位置
        x = (width - textWidth - margin) / 2
        y = (height - textHeight - margin) / 2
        draw.text((x, y), text, color, font)
        return image
