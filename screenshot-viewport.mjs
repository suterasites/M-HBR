import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const url = process.argv[2] || 'http://localhost:3001';
const label = process.argv[3] || 'viewport';
const scrollY = parseInt(process.argv[4] || '0', 10);

const screenshotDir = path.join(__dirname, 'temporary screenshots');
if (!fs.existsSync(screenshotDir)) fs.mkdirSync(screenshotDir, { recursive: true });
const existing = fs.readdirSync(screenshotDir).filter(f => f.startsWith('screenshot-'));
let maxNum = 0;
for (const f of existing) {
  const m = f.match(/^screenshot-(\d+)/);
  if (m) maxNum = Math.max(maxNum, parseInt(m[1]));
}
const num = maxNum + 1;
const filename = `screenshot-${num}-${label}.png`;

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 600));
  if (scrollY === -1) {
    await page.evaluate(() => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      window.scrollTo(0, max);
    });
    await new Promise(r => setTimeout(r, 600));
  } else if (scrollY > 0) {
    await page.evaluate((y) => { document.documentElement.scrollTop = y; document.body.scrollTop = y; }, scrollY);
    await new Promise(r => setTimeout(r, 600));
  }
  await page.screenshot({ path: path.join(screenshotDir, filename), fullPage: false, captureBeyondViewport: false });
  console.log(`Saved: ${filename}`);
  await browser.close();
})();
