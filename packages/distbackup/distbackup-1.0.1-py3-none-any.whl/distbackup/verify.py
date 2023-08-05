import logging

from .database import BackupDB
from .sourcefile import SourceFile

log = logging.getLogger(__name__)

class Verifier:
    def __init__(self, db:BackupDB):
        self.db:BackupDB = db

    def verify(self):
        self.db.require_disk()
        self.db.current_disk.migrate_data()

        bad_objects = []
        try:
            for hash, fpath, stat in self.db.current_disk.walk_data():
                row = self.db.query_one('SELECT last_modified, size, virtual_path, ino FROM file_tree WHERE hash = ? LIMIT 1', (hash,))
                if not row:
                    log.warning(f'{hash} deleted or not in database')
                    continue

                lastmod, size, path, ino = row
                try:
                    srcf = SourceFile(fpath, fpath.lstat())
                except OSError as e:
                    log.warning(f'cannot read {fpath} ({e})')
                    continue

                if srcf.size != size:
                    msg = f'ERROR: {self.db.current_disk.name}/{path}: size mismatch ({srcf.size} != {size})'
                    log.error(msg)
                    bad_objects.append((path, hash))
                    continue

                log.info(f'check {path} ({hash})')
                srcf.copy()
                if srcf.hash != hash:
                    msg = f'ERROR: {self.db.current_disk.name}/{path}: hash ({srcf.hash} != {hash})'
                    log.error(msg)
                    bad_objects.append((path, hash))
        except KeyboardInterrupt:
            pass

        if bad_objects:
            log.info('')
            log.info('Bad files:')
            for path, hash in bad_objects:
                log.info(f'  {hash} {path}')
        else:
            log.info('No bad files.')
