import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import SectionWrapper from './SectionWrapper';

describe('SectionWrapper', () => {
  it('renders without crashing', () => {
    const { container } = render(
      <SectionWrapper id="test-section">
        <p>Hello</p>
      </SectionWrapper>
    );
    expect(container.querySelector('section')).toBeTruthy();
  });

  it('renders children correctly', () => {
    render(
      <SectionWrapper id="hero">
        <h1>Welcome</h1>
      </SectionWrapper>
    );
    expect(screen.getByText('Welcome')).toBeTruthy();
  });

  it('sets the id attribute for scroll targeting', () => {
    const { container } = render(
      <SectionWrapper id="about">
        <p>About content</p>
      </SectionWrapper>
    );
    const section = container.querySelector('section');
    expect(section?.getAttribute('id')).toBe('about');
  });

  it('applies consistent padding classes', () => {
    const { container } = render(
      <SectionWrapper id="padded">
        <p>Padded</p>
      </SectionWrapper>
    );
    const section = container.querySelector('section');
    expect(section?.className).toContain('py-16');
    expect(section?.className).toContain('md:py-24');
  });

  it('renders the inner container with max-width and horizontal padding', () => {
    const { container } = render(
      <SectionWrapper id="container">
        <p>Contained</p>
      </SectionWrapper>
    );
    const innerDiv = container.querySelector('section > div');
    expect(innerDiv?.className).toContain('max-w-7xl');
    expect(innerDiv?.className).toContain('mx-auto');
    expect(innerDiv?.className).toContain('px-4');
  });

  it('defaults to white background when no bgColor is provided', () => {
    const { container } = render(
      <SectionWrapper id="default-bg">
        <p>Default</p>
      </SectionWrapper>
    );
    const section = container.querySelector('section');
    expect(section?.className).toContain('bg-white');
  });

  it('applies cream background class', () => {
    const { container } = render(
      <SectionWrapper id="cream-section" bgColor="cream">
        <p>Cream</p>
      </SectionWrapper>
    );
    const section = container.querySelector('section');
    expect(section?.className).toContain('bg-[#FFFDF7]');
  });

  it('applies slate background class with white text', () => {
    const { container } = render(
      <SectionWrapper id="slate-section" bgColor="slate">
        <p>Slate</p>
      </SectionWrapper>
    );
    const section = container.querySelector('section');
    expect(section?.className).toContain('bg-[#1E293B]');
    expect(section?.className).toContain('text-white');
  });

  it('applies white background class explicitly', () => {
    const { container } = render(
      <SectionWrapper id="white-section" bgColor="white">
        <p>White</p>
      </SectionWrapper>
    );
    const section = container.querySelector('section');
    expect(section?.className).toContain('bg-white');
  });

  it('merges additional className prop', () => {
    const { container } = render(
      <SectionWrapper id="custom" className="border-t border-gray-200">
        <p>Custom</p>
      </SectionWrapper>
    );
    const section = container.querySelector('section');
    expect(section?.className).toContain('border-t');
    expect(section?.className).toContain('border-gray-200');
  });

  it('does not produce double spaces when className is omitted', () => {
    const { container } = render(
      <SectionWrapper id="no-extra-spaces">
        <p>Clean</p>
      </SectionWrapper>
    );
    const section = container.querySelector('section');
    const classStr = section?.className ?? '';
    expect(classStr).not.toMatch(/  /);
  });

  it('renders multiple children', () => {
    render(
      <SectionWrapper id="multi">
        <h2>Title</h2>
        <p>Paragraph one</p>
        <p>Paragraph two</p>
      </SectionWrapper>
    );
    expect(screen.getByText('Title')).toBeTruthy();
    expect(screen.getByText('Paragraph one')).toBeTruthy();
    expect(screen.getByText('Paragraph two')).toBeTruthy();
  });
});
