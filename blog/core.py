def upload_path(instance, filename):
    return "{category}/{filename}".format(category=instance.category.name, filename=filename)

