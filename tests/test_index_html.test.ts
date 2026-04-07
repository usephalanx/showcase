/**
 * Tests for index.html structure and SEO attributes.
 * Validates that the HTML entry point contains required meta tags,
 * Google Fonts links, and the root mount point.
 */
import { describe, it, expect, beforeAll } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';

let htmlContent: string;

beforeAll(() => {
  htmlContent = readFileSync(resolve(__dirname, '..', 'index.html'), 'utf-8');
});

describe('index.html', () => {
  it('should have the correct title', () => {
    expect(htmlContent).toContain('<title>Maddie | Luxury Real Estate</title>');
  });

  it('should have a meta description', () => {
    expect(htmlContent).toContain('name="description"');
    expect(htmlContent).toContain('Luxury real estate');
  });

  it('should have a viewport meta tag', () => {
    expect(htmlContent).toContain('name="viewport"');
    expect(htmlContent).toContain('width=device-width');
  });

  it('should preconnect to Google Fonts', () => {
    expect(htmlContent).toContain('href="https://fonts.googleapis.com"');
    expect(htmlContent).toContain('href="https://fonts.gstatic.com"');
  });

  it('should load Playfair Display font', () => {
    expect(htmlContent).toContain('Playfair+Display');
  });

  it('should load Inter font', () => {
    expect(htmlContent).toContain('Inter');
  });

  it('should have smooth scroll on html element', () => {
    expect(htmlContent).toContain('scroll-behavior: smooth');
  });

  it('should have a root div mount point', () => {
    expect(htmlContent).toContain('<div id="root"></div>');
  });

  it('should reference main.tsx as module script', () => {
    expect(htmlContent).toContain('src="/src/main.tsx"');
    expect(htmlContent).toContain('type="module"');
  });

  it('should have lang="en" attribute', () => {
    expect(htmlContent).toContain('lang="en"');
  });
});
