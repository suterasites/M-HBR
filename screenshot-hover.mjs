import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const url = process.argv[2] || 'http://localhost:3001';
const linkText = process.argv[3] || 'Services';
const label = process.argv[4] || `hover-${linkText.toLowerCase()}`;

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
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 400));

  const handle = await page.evaluateHandle((text) => {
    const links = Array.from(document.querySelectorAll('nav .nav-link'));
    return links.find(l => l.textContent.trim() === text);
  }, linkText);

  if (handle) {
    const el = handle.asElement();
    if (el) {
      await el.hover();
      await new Promise(r => setTimeout(r, 350));
    }
  }

  await page.screenshot({ path: path.join(screenshotDir, filename), fullPage: false, captureBeyondViewport: false });
  console.log(`Saved: ${filename}`);
  await browser.close();
})();
