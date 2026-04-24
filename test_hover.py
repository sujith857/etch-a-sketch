import os
from playwright.sync_api import sync_playwright

def test_hover_effect():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Get the absolute path to the local index.html file
        current_dir = os.getcwd()
        file_path = f"file://{current_dir}/index.html"

        page.goto(file_path)

        # Handle prompts for grid size
        prompts = ["10", "10"]
        def handle_dialog(dialog):
            if prompts:
                value = prompts.pop(0)
                dialog.accept(value)
            else:
                dialog.accept()

        page.on("dialog", handle_dialog)

        # Click the button to create the grid
        page.click("button:has-text('Choose New grid')")

        # Wait for the grid to be generated
        page.wait_for_selector(".grid-item")

        # Select the first grid item
        first_cell = page.locator(".grid-item").first

        # Verify initial class state (should only be 'grid-item', but checking that it is NOT 'hovered')
        assert "hovered" not in first_cell.get_attribute("class"), "Initial state should not have 'hovered' class."
        assert "grid-item" in first_cell.get_attribute("class"), "Initial state should have 'grid-item' class."

        # Trigger hover
        first_cell.hover()

        # Verify class state after hovering
        assert "hovered" in first_cell.get_attribute("class"), "Hovering should add 'hovered' class."
        assert "grid-item" in first_cell.get_attribute("class"), "Hovering should not remove 'grid-item' class."

        # Trigger mouseleave by moving the mouse away (hovering something else or a specific coordinate outside)
        page.mouse.move(0, 0)

        # Verify class state after mouseleave
        assert "hovered" not in first_cell.get_attribute("class"), "Mouse leave should remove 'hovered' class."
        assert "grid-item" in first_cell.get_attribute("class"), "Mouse leave should not remove 'grid-item' class."

        print("Test passed: Hover effect correctly adds/removes 'hovered' class without overwriting 'grid-item'.")

        browser.close()

if __name__ == "__main__":
    test_hover_effect()
