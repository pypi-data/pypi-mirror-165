# from hamunafs.utils.redisutil import XRedisAsync

# import asyncio

# redis = XRedisAsync('cache.ai.hamuna.club', '1987yang', 6379)

# asyncio.run(redis.zadd('1', '2', 3))
import asyncio
from hamunafs.backends.bk_wy import WYSF
from hamunafs.backends.bk_minio import MinioBackend

async def main():
    # wysf_client = WYSF({
    #     'key': '46b5e0508a9641a485c6d3f62078e7ab',
    #     'secret': 'fd187963fb8943febc2624e1241081ed',
    #     'domain': 'hamuna-images.nos-eastchina1.126.net',
    #     'default_bucket': 'hamuna-images'
    # })

    # ret, e = await wysf_client.put_async('/home/superpigy/文档/hamuna-backend/html/index.html', 'tmp', 'hi.html')
    # print(ret)

    # bucket, bucket_name = e.split('/')
    # ret = await wysf_client.get_async('test.html', bucket, bucket_name)

    minio_client = MinioBackend({
        'key': 'hmcz',
        'secret': 'hmcz1234',
        'domain': 'stream.ai.hamuna.club:9001',
        'default_bucket': 'tmps'
    })
    for i in range(100):
        ret, e = minio_client.put('/home/superpigy/文档/hamuna-backend/html/index.html', 'tmp', 'hi.html')
        print(ret)

    # bucket, bucket_name = e.split('/')
    # ret = minio_client.get('test.html', bucket, bucket_name)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
