const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('request', request => {
    if (request.url().endsWith('.js')) {
      console.log('JS Loaded:', request.url());
    }
  });

  console.log("Navigating to https://gigabee.io/ ...");
  await page.goto('https://gigabee.io/', { waitUntil: 'networkidle0' });
  
  console.log("Done.");
  await browser.close();
})();
