import { chromium } from "@playwright/test";
import assert from "node:assert/strict";
import { randomBytes } from "node:crypto";
import { mkdir } from "node:fs/promises";
const base = process.env.WEB_TEST_URL || "http://localhost:3100";
const browser = await chromium.launch({
  headless: true,
  executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE,
});
const context = await browser.newContext({
  viewport: { width: 1440, height: 1000 },
});
const page = await context.newPage();
const errors = [];
page.on("pageerror", (error) => errors.push(error.message));
try {
  await mkdir("artifacts", { recursive: true });
  await page.goto(base);
  await page.getByText("14 species documented", { exact: true }).waitFor();
  assert.equal(await page.locator(".specimen").count(), 14);
  await page.screenshot({ path: "artifacts/companion-desktop.png" });
  await page.getByLabel("Search encyclopedia").fill("Moss Snail");
  assert.equal(await page.locator(".specimen").count(), 1);
  await page.getByLabel("Search encyclopedia").fill("");
  await page.getByRole("button", { name: "Skills", exact: true }).click();
  assert.ok((await page.locator(".specimen").count()) >= 20);
  await page.getByRole("button", { name: "Items", exact: true }).click();
  assert.ok((await page.locator(".specimen").count()) > 0);
  await page.getByRole("button", { name: "Maps", exact: true }).click();
  assert.ok((await page.locator(".specimen").count()) > 0);
  await page.getByRole("button", { name: /02 Synthesis planner/ }).click();
  await page.locator(".tree .branch").first().waitFor();
  assert.ok((await page.locator(".tree .branch").count()) >= 3);
  await page.screenshot({
    path: "artifacts/companion-planner.png",
    fullPage: true,
  });
  await page.getByRole("button", { name: /03 My journal/ }).click();
  await page
    .getByRole("button", { name: "New keeper? Create an account" })
    .click();
  const username = "uiqa_" + randomBytes(5).toString("hex");
  const password = randomBytes(24).toString("base64url");
  await page.getByLabel("Keeper name", { exact: true }).fill(username);
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page
    .getByRole("button", { name: "Create account →", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Trace ancestry ↗", exact: true })
    .waitFor();
  assert.equal(await page.locator(".pet-card").count(), 1);
  const session = (await context.cookies()).find(
    (c) => c.name === "phimond_session",
  );
  assert.ok(session?.httpOnly);
  assert.equal(session.sameSite, "Strict");
  await page
    .getByRole("button", { name: "Trace ancestry ↗", exact: true })
    .click();
  await page.getByRole("heading", { name: /The lineage of/ }).waitFor();
  assert.ok((await page.locator(".tree .branch").count()) > 0);
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await page
    .getByRole("button", { name: "Already a keeper? Sign in", exact: true })
    .click();
  await page.getByLabel("Keeper name", { exact: true }).fill(username);
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page
    .getByRole("button", { name: "Open my journal →", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Trace ancestry ↗", exact: true })
    .waitFor();
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await page.getByLabel("Keeper name", { exact: true }).waitFor();
  assert.ok(
    !(await context.cookies()).some((c) => c.name === "phimond_session"),
  );
  await page.getByRole("button", { name: /01 Encyclopedia/ }).click();
  await page.getByRole("button", { name: "Creatures", exact: true }).click();
  await page.setViewportSize({ width: 390, height: 1000 });
  await page.screenshot({
    path: "artifacts/companion-mobile.png",
    fullPage: true,
  });
  assert.equal(
    await page.evaluate(
      () => document.documentElement.scrollWidth > window.innerWidth,
    ),
    false,
  );
  assert.deepEqual(errors, []);
  console.log(
    "PASS live browser: catalog tabs/search, recipe tree, registration, HttpOnly session, owned pet/lineage, logout/login/logout, mobile overflow; 3 screenshots saved.",
  );
} finally {
  await context.close();
  await browser.close();
}
