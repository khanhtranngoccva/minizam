import io
import os.path
import hashlib
import eyed3
from psycopg import sql
from pydub import AudioSegment
from helpers import path, database


def load_audio(infile):
    sound = AudioSegment.from_file(infile)
    buffer_io = io.BytesIO()
    sound.export(buffer_io, format="wav")
    buffer = buffer_io.read()
    sha256_hash = hashlib.sha256(buffer).hexdigest()
    return buffer, sha256_hash


class Sample:
    def __init__(self,
                 sha256: str,
                 *_,
                 title: str = None,
                 artist: str = None,
                 album: str = None,
                 is_processed: bool = False,
                 _id=None
                 ):
        self.id = _id
        self.sha256 = sha256
        self.title = title
        self.artist = artist
        self.album = album
        self.is_processed = is_processed

    @staticmethod
    def setup_table():
        with database.AtomicConnection() as _conn:
            _conn.cursor.execute("""CREATE TABLE IF NOT EXISTS samples (
                    id SERIAL PRIMARY KEY,
                    sha256 BYTEA UNIQUE NOT NULL,
                    title TEXT,
                    artist TEXT,
                    album TEXT,
                    is_processed BOOLEAN DEFAULT FALSE
                )""")

    def __repr__(self):
        return f'Sample: {self.title}\nID: {self.id}\nArtist: {self.artist}\nAlbum: {self.album}\nSHA256: {self.sha256}\n'

    @property
    def path(self):
        return path.get_sample_path(f"{self.sha256}.wav")

    @staticmethod
    def load(infile, *_, require_metadata=True):
        buffer, sha256_hash = load_audio(infile)
        default_title, _ = os.path.splitext(os.path.basename(infile))
        new_filename = f"{sha256_hash}.wav"
        new_file_path = path.get_sample_path(new_filename)
        with open(new_file_path, "wb") as f:
            f.write(buffer)
        metadata = Sample.load_metadata(infile, require_metadata=require_metadata)

        title = metadata.title if metadata else default_title
        artist = metadata.artist if metadata else None
        album = metadata.album if metadata else None

        return Sample(sha256_hash,
                      title=title,
                      artist=artist,
                      album=album)

    @staticmethod
    def load_metadata(infile, *_, require_metadata=True):
        try:
            file = eyed3.load(infile)
            return file.tag
        except AttributeError as e:
            if require_metadata:
                raise e
            return None

    @staticmethod
    def get_by_ids(ids: list[int]):
        if len(ids) == 0:
            return
        query = sql.SQL("SELECT * FROM samples WHERE id IN ({ids})").format(
            ids=sql.SQL(",").join(sql.Placeholder() * len(ids))
        )
        with database.AtomicConnection() as conn:
            query_result = conn.cursor.execute(query, ids)
            for sample in Sample._yield_sample(query_result):
                yield sample

    @staticmethod
    def get_all():
        query = sql.SQL("SELECT * FROM samples")
        with database.AtomicConnection() as conn:
            query_result = conn.cursor.execute(query)
            for sample in Sample._yield_sample(query_result):
                yield sample

    @staticmethod
    def _yield_sample(query_result):
        for data in query_result:
            yield Sample(_id=data["id"], sha256=data["sha256"].hex(), title=data["title"],
                         artist=data["artist"], album=data["album"], is_processed=data["is_processed"])

    def save(self):
        with database.AtomicConnection() as conn:
            _sha256 = bytes.fromhex(self.sha256)
            query_result = conn.cursor.execute("SELECT id from samples WHERE sha256 = %s", [_sha256]).fetchone()
            if query_result is not None:
                self.id = query_result["id"]
            if self.id is None:
                query_result = conn.cursor.execute(
                    """INSERT INTO samples (sha256, title, artist, album, is_processed) 
                    VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                    [_sha256, self.title, self.artist, self.album, self.is_processed]
                )
                self.id = query_result.fetchone()["id"]
            else:
                conn.cursor.execute(
                    "UPDATE samples SET sha256=%s, title=%s, artist=%s, album=%s, is_processed=%s WHERE id=%s",
                    [_sha256, self.title, self.artist, self.album, self.is_processed, self.id]
                )
