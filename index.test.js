const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync(path.resolve(__dirname, './index.html'), 'utf8');

let dom;
let document;
let window;

describe('Grid Validation Testing', () => {
  beforeEach(() => {
    // Construct a new JSDOM instance per test to ensure isolated environment
    dom = new JSDOM(html, { runScripts: "dangerously" });
    document = dom.window.document;
    window = dom.window;

    // Mock global functions
    window.prompt = jest.fn();
    window.alert = jest.fn();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('Valid grid sizing (e.g. 5x5) verifying that makeRows produces the right grid size', () => {
    window.prompt.mockReturnValueOnce("5").mockReturnValueOnce("5");

    const btn = document.querySelector('button');
    btn.click();

    const gridItems = document.querySelectorAll('.grid-item');
    expect(gridItems.length).toBe(25);
    expect(window.alert).not.toHaveBeenCalled();
  });

  test('Invalid grid sizing (e.g. 100x100) verifying that alert is shown', () => {
    window.prompt.mockReturnValueOnce("100").mockReturnValueOnce("100");

    const btn = document.querySelector('button');
    btn.click();

    const gridItems = document.querySelectorAll('.grid-item');
    expect(gridItems.length).toBe(0);
    expect(window.alert).toHaveBeenCalledWith("Enter Valid entries or Maximum grid possible is 100");
  });

  test('Invalid grid sizing (e.g. 0x0) verifying that alert is shown', () => {
    window.prompt.mockReturnValueOnce("0").mockReturnValueOnce("0");

    const btn = document.querySelector('button');
    btn.click();

    const gridItems = document.querySelectorAll('.grid-item');
    expect(gridItems.length).toBe(0);
    expect(window.alert).toHaveBeenCalledWith("Enter Valid entries or Maximum grid possible is 100");
  });

  test('Invalid grid sizing (e.g. non-numeric strings) verifying that alert is shown', () => {
    window.prompt.mockReturnValueOnce("abc").mockReturnValueOnce("def");

    const btn = document.querySelector('button');
    btn.click();

    const gridItems = document.querySelectorAll('.grid-item');
    expect(gridItems.length).toBe(0);
    expect(window.alert).toHaveBeenCalledWith("Enter Valid entries or Maximum grid possible is 100");
  });
});
