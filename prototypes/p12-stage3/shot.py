import sys,json,asyncio
from playwright.async_api import async_playwright
url=sys.argv[1]; out=sys.argv[2]; wait=float(sys.argv[3]) if len(sys.argv)>3 else 5
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl'])
        pg=await b.new_page(viewport={'width':1280,'height':720})
        logs=[]
        pg.on('console',lambda m:logs.append(m.type+': '+m.text[:300]))
        pg.on('pageerror',lambda e:logs.append('PAGEERR: '+str(e)[:400]))
        await pg.goto(url); await pg.wait_for_timeout(int(wait*1000))
        await pg.screenshot(path=out)
        print('\n'.join(logs[-25:]))
        try:
            print(await pg.evaluate("document.getElementById('phud')?.className"))
        except Exception as e: print('hud err',e)
        await b.close()
asyncio.run(main())
