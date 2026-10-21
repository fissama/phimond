import { chromium } from '@playwright/test';
import path from 'path';

const ARTIFACT_DIR = '/Users/phileanh/.gemini/antigravity-ide/brain/011c27ea-b148-400e-9b78-4882eb990740';
const URL_BASE = 'http://127.0.0.1:5173/scene.html?map=desert_hd2d';

async function capture() {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
  });

  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

  const angles = [
    { name: 'desert_cam_015.png', x: 0.15 },
    { name: 'desert_cam_050.png', x: 0.50 },
    { name: 'desert_cam_085.png', x: 0.85 }
  ];

  for (const { name, x } of angles) {
    const url = `${URL_BASE}&x=${x}`;
    console.log(`Navigating to ${url}...`);
    await page.goto(url);
    await page.waitForTimeout(4000);
    const outPath = path.join(ARTIFACT_DIR, name);
    await page.screenshot({ path: outPath });
    console.log(`Captured ${name} -> ${outPath}`);
  }

  await browser.close();
  console.log('All 3 camera angles captured!');
}

capture().catch(console.error);
