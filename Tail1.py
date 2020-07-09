#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   Blake VandeMerwe, LiveViewTech
# <<

import os
import io
import asyncio
from functools import partial
from typing import AsyncIterator
import time

LINE_BUFFER = 1

import logging
import time

logger_format = '%(asctime)s:%(threadName)s:%(message)s'
logging.basicConfig(format=logger_format, level=logging.INFO, datefmt="%H:%M:%S")

async def tail( filename, last_lines = 10, non_exist_max_secs = 10.0, fp_poll_secs = 0.125):
    """Continuously tail a file pointer yielding one line at a time."""

    async def wait_exists():
        """Wait for a file to exist, the return statement reflects
        whether or not the file existed when the timeout limits were reached."""
        bail_at= time.monotonic() + non_exist_max_secs
        while not os.path.exists(filename):
            if time.monotonic() >= bail_at:
                logging.error('File Does not Exist :'+filename)
                return False
            await asyncio.sleep(fp_poll_secs)
        return True

    async def check_rotate(_fp):
        """Determine if the file rotated in place; same name different inode."""
        nonlocal fino
        print(fino,filename)
        print(locals(),globals())
        time.sleep(10)
        if os.stat(filename).st_ino != fino:
            new_fp = open(filename, 'r')
            _fp.close()
            new_fp.seek(0, os.SEEK_SET)
            fino = os.fstat(new_fp.fileno()).st_ino
            return new_fp
        return _fp

    # ~~
    if not await wait_exists():
        return

    buff = io.StringIO()
    stat = os.stat(filename)

    fino= stat.st_ino
    size = stat.st_size
    blocksize = os.statvfs(filename).f_bsize

    fp = open(filename, 'r', LINE_BUFFER)

    if last_lines > 0:
        if stat.st_size <= blocksize:
            # if the file is smaller than 8kb, read all the lines
            for line in fp.readlines()[-last_lines::]:
                yield line.rstrip()
        else:
            # if the file is larger than 8kb, seek 8kb from the end
            #  and return all the lines except the (potential) half-line
            # first element and the null-terminated extra line at the end.
            fp.seek(os.stat(fp.fileno()).st_size - blocksize)
            for line in fp.readlines()[1:-1][-last_lines::]:
                yield line.rstrip()

    # seek to the end of the file for tailing
    #  given the above operations we should already be there.
    fp.seek(0, os.SEEK_END)

    try:
        while True:
            # wait for the file to exist -- generously
            if not os.path.exists(filename):
                if not await wait_exists():
                    return

            fp = await check_rotate(fp)

            n_stat = os.fstat(fp.fileno())
            n_size = n_stat.st_size

            # if the file is the same size, churn
            #  .. this could be error-prone on small files that
            # rotate VERY fast, but that's an edge case for
            #  tailing a persistent log file.
            if n_size == size:
                await asyncio.sleep(fp_poll_secs)
                continue

            # if the file shrank, seek to the beginning
            if n_size < size:
                fp.seek(0, os.SEEK_SET)

            size = n_size
            for chunk in iter(partial(fp.read, blocksize), ''):
                buff.write(chunk)

            buff.seek(0, os.SEEK_SET)

            for line in buff.readlines():
                yield line.rstrip()

            # resize our string buffer
            buff.truncate(0)

    except IOError:
        buff.close()
        fp.close()


async def main1(file):
    print(file)
    async for line in tail(file):
        print(file,"==> ",line)



async def main(files):
    logging.info("Main started")
    logging.info("Creating multiple tasks with asyncio.gather")
    await asyncio.gather(*[main1(i) for i in files]) # awaits completion of all tasks
    logging.info("Main Ended")

asyncio.run(main(['/var/log/syslog','/var/log/auth.log','/tmp/1.txt']))