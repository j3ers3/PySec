#!/usr/bin/env python3 
# encoding: utf-8   
import asyncio 
from pyppeteer import launch 
async def main(): 
    browser = await launch() 
    page = await browser.newPage()   
    await page.goto('http://www.seebug.org') 
    await page.waitFor("body > div.footer-up") 
    urls = await page.evaluate('''() => {   
        var urls = new Array(); 
        var atags = document.getElementsByTagName("a"); 
        for(var i=0;i<atags.length;i++){ 
            if (atags[i].getAttribute("href")){ 
                urls[i] =   atags[i].getAttribute("href")   
            }   
        }   
        return urls;   
    }''')   

    print(urls) 
    await browser.close() 

asyncio.get_event_loop().run_until_complete(main())
