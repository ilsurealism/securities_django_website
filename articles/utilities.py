from datetime import datetime

def user_img_directory_path(instance, filename):
    date = datetime.now().date()
    return 'images/user_{0}/{1}/{2}'.format(instance.author.id, date, filename)