import { chromium } from '@playwright/test';
import path from 'path';
import fs from 'fs';

const ARTIFACT_DIR = '/Users/phileanh/.gemini/antigravity-ide/brain/011c27ea-b148-400e-9b78-4882eb990740';
const OUT_LAYOUT_DIR = '/Users/phileanh/rust/phimond/.ai/design/map-layouts/desert';
const URL_BASE = 'http://127.0.0.1:5173/scene.html?map=desert_entrance_hd2d';

async function capture() {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
  });

  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

  // 1. Capture 3 camera angles (x = 0.15, 0.50, 0.85)
  const angles = [
    { name: 'desert_entrance_cam_015.png', x: 0.15 },
    { name: 'desert_entrance_cam_050.png', x: 0.50 },
    { name: 'desert_entrance_cam_085.png', x: 0.85 }
  ];

  for (const { name, x } of angles) {
    const url = `${URL_BASE}&x=${x}`;
    console.log(`Navigating to ${url}...`);
    await page.goto(url);
    await page.waitForTimeout(3000);

    const artPath = path.join(ARTIFACT_DIR, name);
    const layoutPath = path.join(OUT_LAYOUT_DIR, name);
    await page.screenshot({ path: artPath });
    fs.copyFileSync(artPath, layoutPath);
    console.log(`Captured ${name} -> ${artPath}`);
  }

  // 2. Zoom 2x on West Portal (x=0.038)
  console.log('Capturing Zoom 2x on West Portal (x=0.038)...');
  await page.goto(`${URL_BASE}&x=0.038`);
  await page.waitForTimeout(2000);
  await page.evaluate(() => {
    if (window.engine) {
      window.engine.camDist = 4.2;
    }
  });
  await page.waitForTimeout(1000);
  const portalZoomArt = path.join(ARTIFACT_DIR, 'desert_entrance_zoom_portal.png');
  const portalZoomLayout = path.join(OUT_LAYOUT_DIR, 'desert_entrance_zoom_portal.png');
  await page.screenshot({ path: portalZoomArt });
  fs.copyFileSync(portalZoomArt, portalZoomLayout);
  console.log(`Captured West Portal Zoom 2x -> ${portalZoomArt}`);

  // 3. Zoom 2x on NPC Edda (x=0.485)
  console.log('Capturing Zoom 2x on NPC Edda (x=0.485)...');
  await page.goto(`${URL_BASE}&x=0.485`);
  await page.waitForTimeout(2000);
  await page.evaluate(() => {
    if (window.engine) {
      window.engine.camDist = 4.2;
    }
  });
  await page.waitForTimeout(1000);
  const eddaZoomArt = path.join(ARTIFACT_DIR, 'desert_entrance_zoom_edda.png');
  const eddaZoomLayout = path.join(OUT_LAYOUT_DIR, 'desert_entrance_zoom_edda.png');
  await page.screenshot({ path: eddaZoomArt });
  fs.copyFileSync(eddaZoomArt, eddaZoomLayout);
  console.log(`Captured NPC Edda Zoom 2x -> ${eddaZoomArt}`);

  // 4. Zoom 2x on East Portal (x=0.965)
  console.log('Capturing Zoom 2x on East Portal (x=0.965)...');
  await page.goto(`${URL_BASE}&x=0.965`);
  await page.waitForTimeout(2000);
  await page.evaluate(() => {
    if (window.engine) {
      window.engine.camDist = 4.2;
    }
  });
  await page.waitForTimeout(1000);
  const eastPortalArt = path.join(ARTIFACT_DIR, 'desert_entrance_zoom_east_portal.png');
  const eastPortalLayout = path.join(OUT_LAYOUT_DIR, 'desert_entrance_zoom_east_portal.png');
  await page.screenshot({ path: eastPortalArt });
  fs.copyFileSync(eastPortalArt, eastPortalLayout);
  console.log(`Captured East Portal Zoom 2x -> ${eastPortalArt}`);

  // 5. Zoom 2x on Northwest Spire & Cactus (px [0-300, 100-320])
  console.log('Capturing Zoom 2x on Northwest Spire & Cactus...');
  await page.goto(`${URL_BASE}&x=0.015`);
  await page.waitForTimeout(2000);
  await page.evaluate(() => {
    const eng = window.engine;
    if (eng) {
      eng.onFrame(() => {
        eng.U.uCamX.value = -0.15;
        eng.camera.position.set(-0.25, 1.1, 1.2);
        eng.camera.lookAt(0.2, 0.75, -1.2);
        eng.camera.updateMatrixWorld();
      });
    }
  });
  await page.waitForTimeout(1000);
  const spireZoomArt = path.join(ARTIFACT_DIR, 'desert_entrance_zoom_northwest_spire.png');
  const spireZoomLayout = path.join(OUT_LAYOUT_DIR, 'desert_entrance_zoom_northwest_spire.png');
  await page.screenshot({ path: spireZoomArt });
  fs.copyFileSync(spireZoomArt, spireZoomLayout);
  console.log(`Captured Northwest Spire Zoom 2x -> ${spireZoomArt}`);

  await browser.close();
  console.log('All 7 Round 2 renders and zoom captures successfully exported to disk!');
}

capture().catch((err) => {
  console.error(err);
  process.exit(1);
});
