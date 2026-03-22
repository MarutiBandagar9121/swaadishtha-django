import uuid
import os

def get_product_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]  # includes dot
    return f'products/{instance.product_id}/{uuid.uuid4()}{ext}'

def get_product_variant_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]  # includes dot
    return f'product_variant/{instance.variant_id}/{uuid.uuid4()}{ext}'