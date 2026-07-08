const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
  page.on('requestfailed', request => {
    console.log('REQUEST FAILED:', request.url(), request.failure().errorText);
  });
  page.on('response', response => {
    if (response.status() === 404) {
      console.log('404:', response.url());
    }
  });

  console.log("Navigating to https://gigabee.io/ ...");
  await page.goto('https://gigabee.io/', { waitUntil: 'networkidle0' });
  
  console.log("Done.");
  await browser.close();
})();
