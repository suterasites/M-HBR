import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const svg = fs.readFileSync(path.join(__dirname, 'favicon.svg'), 'utf8');

const sizes = [
  { name: 'favicon-16.png', size: 16 },
  { name: 'favicon-32.png', size: 32 },
  { name: 'favicon-192.png', size: 192 },
  { name: 'favicon-512.png', size: 512 },
  { name: 'apple-touch-icon.png', size: 180 },
];

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();

  for (const { name, size } of sizes) {
    await page.setViewport({ width: size, height: size, deviceScaleFactor: 1 });
    const html = `<!doctype html><html><head><style>
      html,body{margin:0;padding:0;background:transparent;}
      body{width:${size}px;height:${size}px;display:block;}
      svg{width:${size}px;height:${size}px;display:block;}
    </style></head><body>${svg}</body></html>`;
    await page.setContent(html, { waitUntil: 'load', timeout: 10000 });
    await new Promise(r => setTimeout(r, 100));
    await page.screenshot({
      path: path.join(__dirname, name),
      omitBackground: true,
      clip: { x: 0, y: 0, width: size, height: size },
    });
    console.log(`Rendered ${name} (${size}x${size})`);
  }

  await browser.close();
})();
