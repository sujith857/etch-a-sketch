from playwright.sync_api import sync_playwright
import time

def run_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("file:///app/index.html")

        # Warmup
        page.evaluate("""
            () => {
                makeRows(10, 10);
            }
        """)

        # Test 100x100
        result = page.evaluate("""
            () => {
                const start = performance.now();
                makeRows(100, 100);
                const end = performance.now();
                return end - start;
            }
        """)
        print(f"Time taken for makeRows(100, 100): {result:.2f} ms")

        # Test larger to see if it makes more difference
        result_large = page.evaluate("""
            () => {
                const start = performance.now();
                makeRows(300, 300);
                const end = performance.now();
                return end - start;
            }
        """)
        print(f"Time taken for makeRows(300, 300): {result_large:.2f} ms")
        browser.close()

if __name__ == "__main__":
    run_benchmark()
