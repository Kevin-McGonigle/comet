from django.db import models
import hashlib
import json

def uploaded_file_path(instance, filename):
    """
    The default file storage convention for uploaded files.
    :param instance: An instance of the File object for the file that was uploaded.
    :param filename: The original filename of the file tat was uploaded.
    :return: A string representing the path at which the file should be stored (under MEDIA_ROOT)
    """
    return "{0}_{1}".format(instance.when_uploaded.strftime("%Y%m%d_%H%M%S"), filename)

def generate_hash(filename):
    """
    :param instance: An instance of the File object for the file that was uploaded.
    :param filename: The original filename of the file that was uploaded.
    :return: A string representing the hash of the file.
    """
    return hashlib.sha224(filename.encode('utf-8')).hexdigest()

class File(models.Model):
    hash = models.CharField(max_length=64, primary_key=True, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    size = models.IntegerField(blank=True, null=True)
    file_type = models.CharField(max_length=255)
    when_uploaded = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=uploaded_file_path, unique=True)

    def save(self, *args, **kwargs):
        self.hash = generate_hash(self.name)
        super(File, self).save(*args, **kwargs)

    def __str__(self):
        return json.dumps({
            "hash": self.hash,
            "name": self.name,
        })

class FileHash(models.Model):
    hash = models.CharField(max_length=64, primary_key=True, editable=False)

    def __str__(self):
        return self.hash