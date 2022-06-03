from pathlib import Path
from time import time


def users_avatars_path(instance, filename):
    # file will be uploaded to
    # MEDIA_ROOT / user_<username> / avatars / <filename>
    num = int(time() * 1000)
    suff = Path(filename).suffix
    return 'user_{0}/avatars/{1}'.format(instance.username, f'pic_{num}{suff}')
