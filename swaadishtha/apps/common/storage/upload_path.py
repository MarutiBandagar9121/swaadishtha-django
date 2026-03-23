import uuid
import os


def generate_upload_path(folder: str, instance_id: str, filename: str) -> str:
    """
    Generic function to generate upload path.

    :param folder: base folder name (e.g. 'products', 'categories')
    :param instance_id: unique identifier of instance
    :param filename: original filename
    :return: formatted upload path
    """
    ext = os.path.splitext(filename)[1]  # keeps .jpg, .png etc.
    return f"{folder}/{instance_id}/{uuid.uuid4()}{ext}"


class UploadPath:
    """
    Callable class for Django upload_to.
    Usage:
        upload_to=UploadPath("products", "product_id")
    """

    def __init__(self, folder: str, id_field: str):
        self.folder = folder
        self.id_field = id_field

    def __call__(self, instance, filename):
        instance_id = getattr(instance, self.id_field)
        return generate_upload_path(self.folder, instance_id, filename)