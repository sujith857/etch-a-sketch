import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    # Use current working directory to point to index.html
    html_path = f"file://{os.path.abspath('index.html')}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # We need to test the prompts.
        # The code prompts for rows, then cols.
        # We'll set up a queue of prompt answers.

        prompt_answers = []
        alerts_seen = []

        async def handle_dialog(dialog):
            if dialog.type == 'prompt':
                if prompt_answers:
                    answer = prompt_answers.pop(0)
                    await dialog.accept(answer)
                else:
                    await dialog.accept("10") # fallback
            elif dialog.type == 'alert':
                alerts_seen.append(dialog.message)
                await dialog.accept()
            else:
                await dialog.dismiss()

        page.on('dialog', handle_dialog)

        # Helper to click the button and wait a tiny bit
        async def click_button():
            await page.click('button')
            await page.wait_for_timeout(100)

        await page.goto(html_path)

        print("Testing valid inputs...")
        prompt_answers = ["10", "10"]
        alerts_seen.clear()
        await click_button()
        assert len(alerts_seen) == 0, f"Expected no alerts, got {alerts_seen}"
        # Verify grid exists (10x10 = 100 items)
        items = await page.locator('.grid-item').count()
        assert items == 100, f"Expected 100 grid items, got {items}"

        print("Testing invalid input (strings)...")
        prompt_answers = ["abc", "def"]
        alerts_seen.clear()
        await click_button()
        assert len(alerts_seen) == 1, "Expected an alert for invalid string input"
        assert "Valid entries" in alerts_seen[0] or "Maximum grid" in alerts_seen[0]

        print("Testing invalid input (out of bounds > 100)...")
        prompt_answers = ["101", "101"]
        alerts_seen.clear()
        await click_button()
        assert len(alerts_seen) == 1, "Expected an alert for out of bounds input"

        print("Testing invalid input (out of bounds <= 0)...")
        prompt_answers = ["0", "10"]
        alerts_seen.clear()
        await click_button()
        assert len(alerts_seen) == 1, "Expected an alert for <= 0 input"

        print("Testing upper bounds (100, 100)...")
        prompt_answers = ["100", "100"]
        alerts_seen.clear()
        await click_button()
        assert len(alerts_seen) == 0, f"Expected no alerts, got {alerts_seen}"
        items = await page.locator('.grid-item').count()
        assert items == 10000, f"Expected 10000 grid items, got {items}"

        await browser.close()
        print("All tests passed!")

if __name__ == '__main__':
    asyncio.run(main())
