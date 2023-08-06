"""Test for slow upload of models to byoml."""
from io import RawIOBase
from typing import Any, Tuple
from datetime import datetime
import time
import random
import logging
import os

import pytest
import pandas as pd

from waylay import (
    WaylayClient,
    RestResponseError
)

from fixtures import sklearn_model_and_test_data

LOG = logging.getLogger(__name__)


class SlowBytesIO(RawIOBase):
    """A buffer that intentionaly slows down blocking reads from it."""

    def __init__(self, byte_data, chunck_size=1024, sleep=0):
        """Create a SlowBytesIO buffer."""
        self.data = byte_data
        self.len = len(byte_data)
        self.pos = 0
        self.sleep = sleep
        self.start = None
        self.chunck_size = chunck_size

    # implement seekable interface to let http client extract length
    def seek(self, offset, whence=os.SEEK_SET):
        """Set read position in stream."""
        if whence == os.SEEK_SET:
            self.pos = offset
        elif whence == os.SEEK_CUR:
            self.pos += offset
        elif whence == os.SEEK_END:
            self.pos = self.len + offset
        return self.pos

    def tell(self):
        """Get read position in stream."""
        return self.pos

    def __next__(self):
        """Get next chunck."""
        chunck = self.read(self.chunck_size)
        if not chunck:
            raise StopIteration
        return chunck

    def readinto(self, b):
        """Read from data into given buffer."""
        if not self.start:
            self.start = datetime.now()

        req_len = len(b)
        LOG.info(f'[{datetime.now()-self.start}] request to read {req_len} bytes at {self.pos}')
        if req_len > self.chunck_size:
            req_len = self.chunck_size
            LOG.info(f'[{datetime.now()-self.start}] truncated to read max {req_len} bytes')

        new_pos = self.pos + req_len
        if new_pos >= self.len:
            new_pos = self.len
            req_len = self.len - self.pos

        if self.sleep:
            LOG.info(f'[{datetime.now()-self.start}] sleeping for {self.sleep} seconds')
            time.sleep(self.sleep)

        b[:req_len] = self.data[self.pos:new_pos]
        self.pos = new_pos
        return req_len


def test_slow_buffer_read():
    """Test SlowBytesIO.read ."""
    with SlowBytesIO(b'hello world\n', 5, 0.1) as buf:
        assert b'hello world\n' == buf.read()


def test_slow_buffer_iter():
    """Test SlowBytesIO.__next__ ."""
    msg = b'hello world\n'
    with SlowBytesIO(msg, 3, 0.1) as buf:
        pos = 0
        for b in buf:
            nxt_pos = pos+len(b)
            assert msg[pos:nxt_pos] == b
            pos = nxt_pos


TOTAL_TIME = 60
CHUNK_COUNT = 15
SLEEP_TIME = TOTAL_TIME / CHUNK_COUNT


@pytest.mark.skip(reason="this takes way to long for a regular integration test")
def test_byoml_slow_upload(sklearn_model_and_test_data: Tuple[Any, pd.DataFrame], waylay_test_client: WaylayClient):
    """Create, upload, and get a model with a slowed down upload buffer."""
    trained_model, _ = sklearn_model_and_test_data

    model_name = f"slow-upload-{int(random.random()*1000)}"

    # unrolling of waylay_test_client.byoml.model.upload()
    model_res = waylay_test_client.byoml.model
    with model_res._send_model_arguments(
        model_name, trained_model,
        framework="sklearn",
        metadata=dict(description=f"integration test {__name__}.test_byoml_slow_upload")
    ) as create_args:

        # replace the zip bytes with a slow reader around it
        #    "file": ('model.zip', model_zip_buffer.getvalue())
        files_file_arg = create_args['files']['file']
        model_zip_bytes = files_file_arg[1]
        chunk_size = int(len(model_zip_bytes) / CHUNK_COUNT)
        slow_buffer = SlowBytesIO(model_zip_bytes, chunk_size, SLEEP_TIME)

        create_args['files']['file'] = ('model.zip', slow_buffer)

        header_value = model_res.headers.pop('Content-Type', None)
        try:
            model_res._create(**create_args)
        finally:
            model_res.headers['Content-Type'] = header_value

        # validate that model is present
        model_repr = model_res.get(model_name)
        assert 'name' in model_repr
        assert f'integration test {__name__}' in model_repr['description']

        # remove model
        model_res.remove(model_name)
