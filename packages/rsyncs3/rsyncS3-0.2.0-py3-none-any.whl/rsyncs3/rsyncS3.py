import copy
import hashlib
import multiprocessing
import os
import shutil
import tempfile

import boto3 as boto


# ============================================
#                    RsyncS3
# ============================================
class RsyncS3:
    """
    Provides a local cache of an S3 bucket on disk,
    with the ability to sync up to the latest version of all files.
    Based on this issue : https://github.com/boto/boto/issues/3343
    """

    _DEFAULT_PATH = os.path.join(tempfile.gettempdir(), __name__)

    # -----
    # constructor
    # -----
    def __init__(self, bucketName: str, prefix: str = "", path: str = None) -> None:
        """
        Init method.

        Parameters
        ----------
        bucketName : str
            The name of the S3 bucket from which data is to be fetched.

        prefix : str
            The prefix up to which you want to sync.

        path : optional, str
            A path to store the local files.
        """
        self.bucketName = bucketName
        self.prefix = prefix

        if not path:
            path = os.path.join(self._DEFAULT_PATH, self.bucketName)

        self.path = path
        os.makedirs(path, exist_ok=True)

        s3Resource = boto.resource("s3")
        self.bucket = s3Resource.Bucket(self.bucketName)

    # -----
    # __enter__
    # -----
    def __enter__(self):
        """
        Provides a context manager that will open but not sync, then
        delete the cache on exit.
        """
        return self

    # -----
    # __exit__
    # -----
    def __exit__(self, excType, excValue, traceback):
        """
        Provides a context manager which will open but not sync, then
        delete the cache on exit.
        """
        self.close()

    # -----
    # __getstate__
    # -----
    def __getstate__(self):
        """
        Pickle and un-pickle the self object between multiprocessing
        pools.
        """
        out = copy.copy(self.__dict__)
        out["bucket"] = None
        return out

    # -----
    # __setstate__
    # -----
    def __setstate__(self, stateDict):
        """
        Pickle and un-pickle the self object between multiprocessing
        pools.
        """
        s3Resource = boto.resource("s3")
        stateDict["bucket"] = s3Resource.Bucket(stateDict["bucketName"])
        self.__dict__ = stateDict

    # -----
    # get_path
    # -----
    def get_path(self, key):
        """
        Returns the local file storage path for a given file key.
        """
        return os.path.join(self.path, self.prefix, key)

    # -----
    # calculate_s3_etag
    # -----
    def calculate_s3_etag(self, file, key, tag):
        """
        Calculates the S3 custom e-tag (a specially formatted MD5 hash).
        """
        md5s = []

        chunk_count = 0
        while True:
            data = file.read(self._get_chunk_size(key, tag, chunk_count))
            chunk_count += 1
            if data:
                md5s.append(hashlib.md5(data))
            else:
                break

        if len(md5s) == 1:
            return f'"{md5s[0].hexdigest()}"'

        digests = b"".join(m.digest() for m in md5s)
        digests_md5 = hashlib.md5(digests)
        return f'"{digests_md5.hexdigest()}-{len(md5s)}"'

    # -----
    # _get_obj
    # -----
    def _get_obj(self, key, tag):
        """
        Downloads an object at key to file path. Checks to see if an
        existing file matches the current hash.
        """
        path = os.path.join(self.path, key)
        print(f"Getting {path}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        is_file = path[-1] != "/"
        if is_file:
            should_download = True
            try:
                with open(path, "rb") as file:
                    computed_tag = self.calculate_s3_etag(file, key, tag)
                    if tag == computed_tag:
                        print("Cache Hit")
                        should_download = False
                    else:
                        print(f"Cache Miss {tag} :: {computed_tag}")
            except FileNotFoundError:
                pass

            if should_download:
                self.bucket.download_file(key, path)

    # -----
    # _get_chunk_size
    # -----
    def _get_chunk_size(self, key, tag, chunk=0):
        try:
            parts = tag.split("-")[1]
        except IndexError:
            parts = 0
        if parts:
            client = boto.client(service_name="s3", use_ssl=True)

            response = client.head_object(
                Bucket=self.bucketName, Key=key, PartNumber=chunk
            )
            return int(response["ContentLength"])

        return 8 * 1024 * 1024

    # -----
    # sync
    # -----
    def sync(self):
        """
        Syncs the local and remote S3 copies.
        """
        with multiprocessing.Pool(1) as pool:
            keys = [
                (obj.key, obj.e_tag)
                for obj in self.bucket.objects.filter(Prefix=self.prefix)
            ]
            pool.starmap(self._get_obj, keys)

    # -----
    # close
    # -----
    def close(self):
        """
        Deletes all local files.
        """
        shutil.rmtree(self.path)
