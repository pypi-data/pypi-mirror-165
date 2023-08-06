
from . import messages
from . import configuration

class UploadPicturesUtil:
    """

    Upload Pictures Utils

    """

    @staticmethod
    def profile_picture(instance, filename):
        name, file_extention = os.path.splitext(filename)
        name = 'user-{}.{}'.format(instance.code, file_extention)
        return "pictures/users/{}/{}".format(instance.code, name)

    @staticmethod
    def validate_small(image_field):
        """

        Validate Upload Image Size

        """
        ext = os.path.splitext(image_field.name)[1]  # [0] returns path+filename

        valid_extensions = ['.jpg', '.png', '.jpeg']

        if not ext.lower() in valid_extensions:
            raise ValidationError(
                messages.get_message('pictures.small.ext.error'))

        file_size = image_field.file.size

        limit_kb = configuration.get_integer(
            'pictures.small.maxlength.kb', default=200)

        if file_size > limit_kb * KILOBYTE:
            raise ValidationError('{} {}KB'.format(
                messages.get_message('pictures.small.maxlength.error'), limit_kb))
