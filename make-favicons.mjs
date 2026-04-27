import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import http from 'http';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const sizes = [
  { name: 'favicon-16.png', size: 16 },
  { name: 'favicon-32.png', size: 32 },
  { name: 'favicon-192.png', size: 192 },
  { name: 'favicon-512.png', size: 512 },
  { name: 'apple-touch-icon.png', size: 180 },
];

const PORT = 3939;
const server = http.createServer((req, res) => {
  const filePath = path.join(__dirname, decodeURIComponent(req.url === '/' ? '/index.html' : req.url));
  fs.readFile(filePath, (err, content) => {
    if (err) { res.writeHead(404); res.end(); return; }
    const ext = path.extname(filePath).toLowerCase();
    const types = { '.html': 'text/html', '.jpg': 'image/jpeg', '.png': 'image/png' };
    res.writeHead(200, { 'Content-Type': types[ext] || 'application/octet-stream' });
    res.end(content);
  });
});

await new Promise(r => server.listen(PORT, r));

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();

  for (const { name, size } of sizes) {
    await page.setViewport({ width: size, height: size, deviceScaleFactor: 1 });
    const html = `<!doctype html><html><head><style>
      html,body{margin:0;padding:0;background:#ffffff;}
      body{width:${size}px;height:${size}px;display:flex;align-items:center;justify-content:center;overflow:hidden;}
      .wrap{width:${size}px;height:${size}px;position:relative;overflow:hidden;}
      img{position:absolute;top:50%;left:0;height:100%;width:auto;transform:translateY(-50%);object-fit:cover;}
    </style></head><body><div class="wrap"><img id="logo" src="http://localhost:${PORT}/Assets/logo.jpg"/></div></body></html>`;
    await page.setContent(html, { waitUntil: 'load', timeout: 10000 });
    await page.evaluate(() => new Promise(resolve => {
      const img = document.getElementById('logo');
      if (img.complete && img.naturalWidth) return resolve();
      img.onload = () => resolve();
      img.onerror = () => resolve();
    }));
    // Crop the leftmost portion of the logo to isolate the M-mark.
    await page.evaluate((targetSize) => {
      const img = document.getElementById('logo');
      const nh = img.naturalHeight;
      const nw = img.naturalWidth;
      // Source logo is 403x125 lockup. Tight crop of the M-mark = leftmost ~95px square.
      const cropSize = nh * 0.61;
      const scale = targetSize / cropSize;
      const cropWidth = cropSize;
      const imgH = nh * scale;
      const imgW = nw * scale;
      img.style.height = imgH + 'px';
      img.style.width = imgW + 'px';
      img.style.left = '0';
      img.style.top = ((targetSize - imgH) / 2) + 'px';
      img.style.transform = 'none';
    }, size);
    await new Promise(r => setTimeout(r, 80));
    await page.screenshot({
      path: path.join(__dirname, name),
      omitBackground: false,
      clip: { x: 0, y: 0, width: size, height: size },
    });
    console.log(`Rendered ${name} (${size}x${size})`);
  }

  await browser.close();
  server.close();
})();
