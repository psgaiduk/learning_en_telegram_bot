from os import makedirs, path, listdir, remove
import subprocess
from django.utils import timezone

from settings import settings


def create_dump_func():

    db = settings.postgres

    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    filename = f"db_dump_{timestamp}.sql"
    dump_dir = "static/dump/"
    filepath = path.join(dump_dir, filename)
    makedirs(dump_dir, exist_ok=True)

    command = f"PGPASSWORD={db.password} pg_dump -h {db.host} -U {db.user} -d {db.db_name} | gzip > {filepath}"
    subprocess.run(command, shell=True, check=True)

    dump_files = sorted(
        [path.join(dump_dir, f) for f in listdir(dump_dir) if f.endswith(".sql")],
        key=path.getmtime
    )

    deleted_info = ""
    if len(dump_files) > 14:
        for file_to_delete in dump_files[:-14]:
            deleted_info = f"{deleted_info} - Delete: {file_to_delete}"
            remove(file_to_delete)

    return f"Created file {filename}{deleted_info}"
