from django.db import models


def uploaded_file_path(instance, filename):
    """
    The default file storage convention for uploaded files.
    :param instance: An instance of the File object for the file that was uploaded.
    :param filename: The original filename of the file tat was uploaded.
    :return: A string representing the path at which the file should be stored (under MEDIA_ROOT)
    """
    return "{0}_{1}".format(instance.when_uploaded.strftime("%Y%m%d_%H%M%S"), filename)


class File(models.Model):
    hash = models.CharField(max_length=64, primary_key=True, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=255)
    when_uploaded = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=uploaded_file_path, unique=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super().save(**kwargs)


class Class(models.Model):
    hash = models.CharField(max_length=64, primary_key=True, editable=False)
    file_hash = models.ForeignKey("File", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Method(models.Model):
    hash = models.CharField(max_length=64, primary_key=True, editable=False)
    class_hash = models.ForeignKey("Class", on_delete=models.CASCADE, default="")
    file_hash = models.ForeignKey("File", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    return_type = models.CharField(max_length=255, default="void")

    def __str__(self):
        return self.name


class MethodParameter(models.Model):
    method_hash = models.ForeignKey("Method", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name


class ClassRelationship(models.Model):
    parent_hash = models.ForeignKey("Class", on_delete=models.CASCADE, related_name="+")
    child_hash = models.ForeignKey("Class", on_delete=models.CASCADE, related_name="+")
    relationship_type = models.CharField(max_length=255, default="association")

    def __str__(self):
        return self.name
