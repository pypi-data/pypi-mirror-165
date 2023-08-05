import asyncio
from .utils.misc import choose
import json
import time
from .pururin import get_pur
from .nhentai import get_nh
from .hentaifox import get_hfox
from .asmhentai import get_asm

async def get_bulk(book: str = choose().bulk):
    f = open(book)

    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError:
        print("Invalid bulk file, does not follow the nested JSON format.\nBulk downloads guide: https://github.com/sinkaroid/tomoe#bulk-download")
        return

    initial = time.time()
    print(f'Requesting {len(data["book"])} doujinshi..')
    
    for i in data['book']:
        for key, value in i.items():
            ## print(key, value)
            if key.startswith("p"):
                await asyncio.gather(get_pur(value))
            elif key.startswith("n"):
                await asyncio.gather(get_nh(value))
            elif key.startswith("h"):
                await asyncio.gather(get_hfox(value))
            elif key.startswith("a"):
                await asyncio.gather(get_asm(value))

            else:
                print("An unexpected property that does not support bulk requests:", key, value)
                pass
            
    print(f"Bulk download completed, took: {(time.time() - initial) / 60:.2f}" + " minutes")
    f.close()