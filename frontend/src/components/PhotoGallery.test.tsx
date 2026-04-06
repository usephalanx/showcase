import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import PhotoGallery from './PhotoGallery';

const MOCK_IMAGES = [
  'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
  'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',
  'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
  'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
];

describe('PhotoGallery', () => {
  beforeEach(() => {
    document.body.style.overflow = '';
  });

  it('renders without crashing with images', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    expect(screen.getByTestId('photo-gallery')).toBeDefined();
  });

  it('renders empty state when no images are provided', () => {
    render(<PhotoGallery images={[]} />);
    expect(screen.getByTestId('photo-gallery-empty')).toBeDefined();
    expect(screen.getByText('No images available')).toBeDefined();
  });

  it('displays the first image as the main image by default', () => {
    render(<PhotoGallery images={MOCK_IMAGES} alt="Test property" />);
    const mainImg = screen.getByTestId('main-image') as HTMLImageElement;
    expect(mainImg.src).toBe(MOCK_IMAGES[0]);
    expect(mainImg.alt).toBe('Test property 1');
  });

  it('renders thumbnail strip with correct number of thumbnails', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    const strip = screen.getByTestId('thumbnail-strip');
    expect(strip).toBeDefined();
    MOCK_IMAGES.forEach((_, index) => {
      expect(screen.getByTestId(`thumbnail-${index}`)).toBeDefined();
    });
  });

  it('does not render thumbnail strip for single image', () => {
    render(<PhotoGallery images={[MOCK_IMAGES[0]]} />);
    expect(screen.queryByTestId('thumbnail-strip')).toBeNull();
  });

  it('changes main image when a thumbnail is clicked', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    const thumbnail2 = screen.getByTestId('thumbnail-2');
    fireEvent.click(thumbnail2);
    const mainImg = screen.getByTestId('main-image') as HTMLImageElement;
    expect(mainImg.src).toBe(MOCK_IMAGES[2]);
  });

  it('opens lightbox when main image is clicked', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    expect(screen.queryByTestId('lightbox-overlay')).toBeNull();
    const mainImageContainer = screen.getByRole('button', { name: /open fullscreen lightbox/i });
    fireEvent.click(mainImageContainer);
    expect(screen.getByTestId('lightbox-overlay')).toBeDefined();
    expect(screen.getByTestId('lightbox-image')).toBeDefined();
  });

  it('lightbox displays the currently active image', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    fireEvent.click(screen.getByTestId('thumbnail-1'));
    fireEvent.click(screen.getByRole('button', { name: /open fullscreen lightbox/i }));
    const lightboxImg = screen.getByTestId('lightbox-image') as HTMLImageElement;
    expect(lightboxImg.src).toBe(MOCK_IMAGES[1]);
  });

  it('navigates to next image in lightbox', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    fireEvent.click(screen.getByRole('button', { name: /open fullscreen lightbox/i }));
    const nextBtn = screen.getByTestId('lightbox-next');
    fireEvent.click(nextBtn);
    const lightboxImg = screen.getByTestId('lightbox-image') as HTMLImageElement;
    expect(lightboxImg.src).toBe(MOCK_IMAGES[1]);
  });

  it('navigates to previous image in lightbox', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    fireEvent.click(screen.getByRole('button', { name: /open fullscreen lightbox/i }));
    const prevBtn = screen.getByTestId('lightbox-prev');
    fireEvent.click(prevBtn);
    const lightboxImg = screen.getByTestId('lightbox-image') as HTMLImageElement;
    expect(lightboxImg.src).toBe(MOCK_IMAGES[MOCK_IMAGES.length - 1]);
  });

  it('wraps around to first image when clicking next on last image', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    fireEvent.click(screen.getByTestId('thumbnail-3'));
    fireEvent.click(screen.getByRole('button', { name: /open fullscreen lightbox/i }));
    const nextBtn = screen.getByTestId('lightbox-next');
    fireEvent.click(nextBtn);
    const lightboxImg = screen.getByTestId('lightbox-image') as HTMLImageElement;
    expect(lightboxImg.src).toBe(MOCK_IMAGES[0]);
  });

  it('closes lightbox when close button is clicked', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    fireEvent.click(screen.getByRole('button', { name: /open fullscreen lightbox/i }));
    expect(screen.getByTestId('lightbox-overlay')).toBeDefined();
    fireEvent.click(screen.getByTestId('lightbox-close'));
    expect(screen.queryByTestId('lightbox-overlay')).toBeNull();
  });

  it('closes lightbox when overlay background is clicked', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    fireEvent.click(screen.getByRole('button', { name: /open fullscreen lightbox/i }));
    fireEvent.click(screen.getByTestId('lightbox-overlay'));
    expect(screen.queryByTestId('lightbox-overlay')).toBeNull();
  });

  it('closes lightbox on Escape key press', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    fireEvent.click(screen.getByRole('button', { name: /open fullscreen lightbox/i }));
    expect(screen.getByTestId('lightbox-overlay')).toBeDefined();
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(screen.queryByTestId('lightbox-overlay')).toBeNull();
  });

  it('navigates with arrow keys in lightbox', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    fireEvent.click(screen.getByRole('button', { name: /open fullscreen lightbox/i }));
    fireEvent.keyDown(document, { key: 'ArrowRight' });
    const lightboxImg = screen.getByTestId('lightbox-image') as HTMLImageElement;
    expect(lightboxImg.src).toBe(MOCK_IMAGES[1]);
    fireEvent.keyDown(document, { key: 'ArrowLeft' });
    expect((screen.getByTestId('lightbox-image') as HTMLImageElement).src).toBe(MOCK_IMAGES[0]);
  });

  it('uses default alt text when alt prop is not provided', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    const mainImg = screen.getByTestId('main-image') as HTMLImageElement;
    expect(mainImg.alt).toBe('Property photo 1');
  });

  it('displays image counter text', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    expect(screen.getByText(`1 / ${MOCK_IMAGES.length}`)).toBeDefined();
  });

  it('has proper dialog role on lightbox', () => {
    render(<PhotoGallery images={MOCK_IMAGES} />);
    fireEvent.click(screen.getByRole('button', { name: /open fullscreen lightbox/i }));
    expect(screen.getByRole('dialog')).toBeDefined();
  });
});
