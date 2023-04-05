from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def presave_resize_image(instance):
    item = Image.open(instance.image)
    wid, hgt = item.size
    if wid > 1400 and hgt > 900:
        item = item.resize((1400,900))
        output_io_stream = BytesIO()
        item.save(output_io_stream, format='JPEG')
        output_io_stream.seek(0)

        instance.image = InMemoryUploadedFile(
            output_io_stream,
            'ImageField',
            instance.image.name,
            'image/jpeg',
            output_io_stream.getbuffer().nbytes,
            None
        )


def presave_quality_image(instance):
    item = Image.open(instance.image)
    output_io_stream = BytesIO()
    item.save(output_io_stream, format='JPEG', quality=65)
    output_io_stream.seek(0)
    instance.image = InMemoryUploadedFile(
        output_io_stream,
        'ImageField',
        instance.image.name,
        'image/jpeg',
        output_io_stream.getbuffer().nbytes,
        None
    )
