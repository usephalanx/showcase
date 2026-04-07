/**
 * Tests for src/index.css content.
 * Validates that the global stylesheet contains required Tailwind directives,
 * base styles, component classes, and custom utilities.
 */
import { describe, it, expect, beforeAll } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';

let cssContent: string;

beforeAll(() => {
  cssContent = readFileSync(
    resolve(__dirname, '..', 'src', 'index.css'),
    'utf-8',
  );
});

describe('src/index.css', () => {
  it('should include @tailwind base directive', () => {
    expect(cssContent).toContain('@tailwind base;');
  });

  it('should include @tailwind components directive', () => {
    expect(cssContent).toContain('@tailwind components;');
  });

  it('should include @tailwind utilities directive', () => {
    expect(cssContent).toContain('@tailwind utilities;');
  });

  it('should set smooth scroll on html', () => {
    expect(cssContent).toContain('scroll-behavior: smooth');
  });

  it('should set body font to Inter via font-inter', () => {
    expect(cssContent).toContain('font-inter');
  });

  it('should set heading font to Playfair Display via font-playfair', () => {
    expect(cssContent).toContain('font-playfair');
  });

  it('should define section-container component class', () => {
    expect(cssContent).toContain('.section-container');
  });

  it('should define section-padding component class', () => {
    expect(cssContent).toContain('.section-padding');
  });

  it('should define btn-primary component class', () => {
    expect(cssContent).toContain('.btn-primary');
  });

  it('should define btn-secondary component class', () => {
    expect(cssContent).toContain('.btn-secondary');
  });

  it('should define gold-gradient component class', () => {
    expect(cssContent).toContain('.gold-gradient');
  });

  it('should define gold-gradient-text component class', () => {
    expect(cssContent).toContain('.gold-gradient-text');
  });

  it('should define hover-lift animation class', () => {
    expect(cssContent).toContain('.hover-lift');
  });

  it('should define hover-scale animation class', () => {
    expect(cssContent).toContain('.hover-scale');
  });

  it('should define hover-glow animation class', () => {
    expect(cssContent).toContain('.hover-glow');
  });

  it('should include webkit font smoothing', () => {
    expect(cssContent).toContain('-webkit-font-smoothing: antialiased');
  });

  it('should set cream background on body', () => {
    expect(cssContent).toContain('bg-cream');
  });
});
