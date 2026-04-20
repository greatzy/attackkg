import { chromium } from 'playwright';
import fs from 'fs';

async function captureScreenshots() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  try {
    // 导航到前端页面
    await page.goto('http://localhost:5174/');
    await page.waitForTimeout(2000);
    
    // 登录
    await page.fill('input[type="text"]', 'admin');
    await page.fill('input[type="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForTimeout(3000);
    
    // 截图：登录后首页
    await page.screenshot({ path: 'screenshots/homepage.png', fullPage: true });
    console.log('✓ 首页截图完成');
    
    // 导航到检测规则页面
    await page.click('text=检测规则');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'screenshots/rules.png', fullPage: true });
    console.log('✓ 检测规则页面截图完成');
    
    // 导航到威胁行为者页面
    await page.click('text=威胁行为者');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'screenshots/actors.png', fullPage: true });
    console.log('✓ 威胁行为者页面截图完成');
    
    // 导航到技术和战术页面
    await page.click('text=技术和战术');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'screenshots/attack.png', fullPage: true });
    console.log('✓ 技术和战术页面截图完成');
    
    console.log('所有截图完成！');
    
  } catch (error) {
    console.error('截图过程中出错:', error);
  } finally {
    await browser.close();
  }
}

// 创建screenshots目录
if (!fs.existsSync('screenshots')) {
  fs.mkdirSync('screenshots');
}

captureScreenshots();
