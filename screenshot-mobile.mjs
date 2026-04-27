import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const url = process.argv[2] || 'http://localhost:3001';
const label = process.argv[3] || 'mobile';
const action = process.argv[4] || 'none';

const screenshotDir = path.join(__dirname, 'temporary screenshots');
if (!fs.existsSync(screenshotDir)) fs.mkdirSync(screenshotDir, { recursive: true });
const existing = fs.readdirSync(screenshotDir).filter(f => f.startsWith('screenshot-'));
let maxNum = 0;
for (const f of existing) {
  const m = f.match(/^screenshot-(\d+)/);
  if (m) maxNum = Math.max(maxNum, parseInt(m[1]));
}
const filename = `screenshot-${maxNum + 1}-${label}.png`;

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 400));

  if (action === 'open-menu') {
    await page.click('#hamburger');
    await new Promise(r => setTimeout(r, 350));
  }

  await page.screenshot({ path: path.join(screenshotDir, filename), fullPage: false });
  console.log(`Saved: ${filename}`);
  await browser.close();
})();
