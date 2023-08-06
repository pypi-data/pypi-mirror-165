import os
import tarfile

import zarr


class TarStore(zarr._storage.store.Store):
    def __init__(self, path):
        path = os.path.abspath(path)
        self.path = path
        self.tf = tarfile.open(path)
        self.prefix = os.path.basename(path).replace('.tar', '') + '/'

    def __contains__(self, item: str):
        item = os.path.join(self.prefix, item)
        return item in self.tf.getnames()

    def __delitem__(self, item: str):
        raise NotImplementedError('TarStore is a read-only store')
    
    def __getitem__(self, item: str):
        item = os.path.join(self.prefix, item)
        return self.tf.extractfile(item).read()

    def __iter__(self):
        return self.keys()

    def __len__(self) -> int:
        return sum(1 for _ in self.keys())

    def __setitem__(self, item: str, value):
        raise NotImplementedError('TarStore is a read-only store')
    
    def close(self):
        """Closes the underlying tar file."""
        self.tf.close()

    def getsize(self, path=None):
        file_path = os.path.join(self.prefix, path)
        tar_path = zarr.util.normalize_storage_path(file_path)
        tar_elt = self.tf.getmember(tar_path)

        if tar_elt.isfile():
            return tar_elt.size
        elif tar_elt.isdir():
            size = 0
            childs = [
                k for k in self.tf.getnames() if k.startswith(tar_path + '/')
            ]
            for child in childs:
                elt = self.tf.getmember(child)
                if elt.isfile():
                    size += elt.size
            return size
        else:
            return 0

    def keys(self):
        for m in self.tf:
            if m.isfile():
                yield m.name.replace(self.prefix, '')

    def listdir(self, path=None):
        tar_path = zarr.util.normalize_storage_path(path)
        if tar_path:
            tar_path = tar_path + '/'
        tar_path_len = len(tar_path)
        s = set([
            k[tar_path_len:].split('/', 1)[0] for k in self.keys()
            if k.startswith(tar_path)
        ])
        return list(s)


def create_tar(src_path, dest_dir=None):
    """
    Create a tar archive of source. The tar file name is source name with '.tar' extension and is stored in the same source directory.  
    """
    src_fname = os.path.basename(src_path)
    src_path = os.path.normpath(src_path)
    tar_fname = src_fname + '.tar'
    if dest_dir is None:
        dest_dir = os.path.dirname(src_path) 
    tar_fpath =  os.path.join(dest_dir, tar_fname)
    with tarfile.open(tar_fpath, "w") as tar:
        tar.add(name=src_path, arcname=src_fname)
    return tar_fpath
