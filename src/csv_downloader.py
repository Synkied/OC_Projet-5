# coding: utf8

import requests

from tqdm import tqdm  # shows a progress bar

from constants import *


class TqdmDL(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""

    def download_from_url(self, url, directory, fname):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        # Streaming, so we can iterate over the response.

        dwnld = requests.get(url, stream=True)

        # size of chunk downloaded
        chunk_size = 32 * 1024
        # Total size in bytes.
        total_size = int(dwnld.headers.get('content-length', 0))

        # write to utf-16, for foreign chars
        with open(directory + fname, 'wb') as f:
            pbar = tqdm(dwnld.iter_content(
                chunk_size=chunk_size,
                decode_unicode=True),
                desc="Téléchargement en cours...",
                total=total_size,
                unit='B',
                unit_scale=True
            )
            for data in pbar:
                if data:
                    pbar.update(chunk_size)
                    f.write(data)


if __name__ == "__main__":
    t = TqdmDL()

    t.download_from_url(CSV_URL, "../", CSV_FNAME)
