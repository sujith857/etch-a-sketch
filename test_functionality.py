from playwright.sync_api import sync_playwright

def test_app():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("file:///app/index.html")

        # Test valid input
        def handle_prompt(dialog):
            if "rows" in dialog.message.lower():
                dialog.accept("10")
            elif "cols" in dialog.message.lower():
                dialog.accept("10")

        page.on("dialog", handle_prompt)
        page.click("button")

        # Check grid items
        items = page.locator(".grid-item")
        count = items.count()
        print(f"Grid items created: {count}")
        assert count == 100, f"Expected 100 grid items, got {count}"

        # Check hover
        first_item = items.nth(0)
        first_item.hover()
        classes = first_item.get_attribute("class")
        print(f"Classes on hover: {classes}")
        assert "hovered" in classes, f"Expected 'hovered' in classes, got {classes}"

        # Move mouse away
        page.mouse.move(0, 0)
        classes = first_item.get_attribute("class")
        print(f"Classes after mouseleave: {classes}")
        assert "hovered" not in classes, f"Expected 'hovered' to be removed, got {classes}"

        # Test invalid input
        def handle_prompt_invalid(dialog):
            if "rows" in dialog.message.lower():
                dialog.accept("abc")
            elif "cols" in dialog.message.lower():
                dialog.accept("def")
            else:
                dialog.accept()

        page.remove_listener("dialog", handle_prompt)

        alert_shown = False
        def handle_alert(dialog):
            nonlocal alert_shown
            if "valid entries" in dialog.message.lower():
                alert_shown = True
            dialog.accept()

        page.on("dialog", handle_prompt_invalid)
        # We need a separate listener for alert maybe?
        # Actually playwright dialog event fires for prompt, alert, confirm

        # Let's reset the dialog handler to handle both prompt and alert
        page.remove_listener("dialog", handle_prompt_invalid)

        def handle_all_dialogs(dialog):
            nonlocal alert_shown
            if dialog.type == "alert":
                alert_shown = True
                dialog.accept()
            elif dialog.type == "prompt":
                dialog.accept("abc")
            else:
                dialog.accept()

        page.on("dialog", handle_all_dialogs)
        page.click("button")

        assert alert_shown, "Expected alert to be shown for invalid input"
        print("All tests passed!")
        browser.close()

if __name__ == "__main__":
    test_app()
