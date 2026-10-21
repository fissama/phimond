import { chromium } from '@playwright/test';
import path from 'path';
import fs from 'fs';

const ARTIFACT_DIR = '/Users/phileanh/.gemini/antigravity-ide/brain/011c27ea-b148-400e-9b78-4882eb990740';
const URL_BASE = 'http://127.0.0.1:5173/scene.html?map=windrock_hd2d';

async function capture() {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
  });

  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

  const angles = [
    { name: 'windrock_cam_015.png', x: 0.15 },
    { name: 'windrock_cam_050.png', x: 0.50 },
    { name: 'windrock_cam_085.png', x: 0.85 }
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

  // Capture 2x zoomed crop of the suspension bridge across chasm & ground transition at x=0.50
  console.log('Capturing 2x zoom crop at x=0.50...');
  const zoomUrl = `${URL_BASE}&x=0.50`;
  await page.goto(zoomUrl);
  await page.waitForTimeout(3000);
  
  // Crop around the bridge, chasms, and floor decals (center region 640x360 scaled to 1280x720)
  const clip = { x: 320, y: 220, width: 640, height: 360 };
  const zoomPath = path.join(ARTIFACT_DIR, 'windrock_transition_zoom_2x.png');
  await page.screenshot({ path: zoomPath, clip });
  console.log(`Captured windrock_transition_zoom_2x.png -> ${zoomPath}`);

  await browser.close();
  console.log('All 4 visual validation screenshots captured successfully!');
}

capture().catch(console.error);
