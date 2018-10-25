import argparse
import aiohttp
import asyncio
import async_timeout
import gzip
import re

from collections import defaultdict

base_url = "http://dumps.wikimedia.your.org/other/pageviews/{year}/{year}-{month:02d}/pageviews-{year}{month:02d}{day:02d}-{hour:02d}0000.gz"
async def downloadFile(semaphore, session, url):
    try:
        # with async_timeout.timeout(10):
        async with semaphore,  session.get(url) as remotefile:
            if remotefile.status == 200:
                data = await remotefile.read()
                outfile = re.sub("/", "_", url[7:])
                with open(outfile, 'wb') as fp:
                    print('Saving')
                    fp.write(data)
                    return outfile
            else:
                print('Something went wrong')
                print(remotefile)
                return
    except Exception as e:
        print(e)
        return

async def processOne(semaphore, session, url, counter):
    filename = await downloadFile(semaphore, session, url)
    if not filename:
        return

    cnt = 0
    with gzip.open(filename, 'r') as fp:
        for line in fp:
            line = line.decode("utf-8")
            if not line.startswith("it"):
                continue

            # keep only wikipedia pages
            if re.match(r"it\.\+", line):
                continue

            cnt += 1
            print("\rProcessed pages: {0}".format(cnt), flush=True, end=" ")
            parts = line.split()
            counter[parts[1]] += int(parts[2])

async def aux(urls, counter):
    sem = asyncio.Semaphore(10)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(processOne(sem, session, url, counter))
            tasks.append(task)
        await asyncio.gather(*tasks)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2016)
    parser.add_argument("--month", type=int, default=4)
    parser.add_argument("--temp_folder", type=str)
    args = parser.parse_args()

    urls = []
    counter = defaultdict(int)
    for day in range(1, 32):
        for hour in range(24):
            urls.append(base_url.format(
                year=args.year, month=args.month, day=day, hour=hour))

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(aux(urls, counter))
    loop.run_until_complete(aux(urls, counter))
    print(sorted(list(counter.items()), key=lambda x: x[1], reverse=True)[:5])
    with open('counter.pickle', 'wb') as fp:
        pickle.dump(counter, fp)



if __name__ == "__main__":
    main()
