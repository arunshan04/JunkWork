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
    async def wait_exists():
        bail_at= time.monotonic() + non_exist_max_secs
        while not os.path.exists(filename):
            if time.monotonic() >= bail_at:
                logging.error('File Does not Exist :'+filename)
                return False
            await asyncio.sleep(fp_poll_secs)
        return True

    async def check_rotate(_fp):
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
    fp.seek(0, os.SEEK_END)

    try:
        while True:
            if not os.path.exists(filename):
                if not await wait_exists():
                    return
            fp = await check_rotate(fp)
            n_stat = os.fstat(fp.fileno())
            n_size = n_stat.st_size
            if n_size == size:
                await asyncio.sleep(fp_poll_secs)
                continue
            if n_size < size:
                fp.seek(0, os.SEEK_SET)
            size = n_size
            for chunk in iter(partial(fp.read, blocksize), ''):
                buff.write(chunk)
            buff.seek(0, os.SEEK_SET)
            for line in buff.readlines():
                yield line.rstrip()
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