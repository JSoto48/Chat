from PIL import Image
from django.core.exceptions import ValidationError
import os



def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f'Allowed maximum accepted dimensions are 70x70 pixels, your image is {img.size}'
                )



def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            f'Unsupported file extension. Accepted extensions: {valid_extensions}'
        )


