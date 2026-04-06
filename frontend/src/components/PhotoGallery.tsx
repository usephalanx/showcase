import React, { useState, useEffect, useCallback } from 'react';

export interface PhotoGalleryProps {
  images: string[];
  alt?: string;
}

const PhotoGallery: React.FC<PhotoGalleryProps> = ({ images, alt = 'Property photo' }) => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [lightboxIndex, setLightboxIndex] = useState(0);

  const openLightbox = useCallback(() => {
    setLightboxIndex(activeIndex);
    setLightboxOpen(true);
  }, [activeIndex]);

  const closeLightbox = useCallback(() => {
    setLightboxOpen(false);
  }, []);

  const goToPrev = useCallback(() => {
    setLightboxIndex((prev) => (prev === 0 ? images.length - 1 : prev - 1));
  }, [images.length]);

  const goToNext = useCallback(() => {
    setLightboxIndex((prev) => (prev === images.length - 1 ? 0 : prev + 1));
  }, [images.length]);

  useEffect(() => {
    if (!lightboxOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') goToPrev();
      if (e.key === 'ArrowRight') goToNext();
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [lightboxOpen, closeLightbox, goToPrev, goToNext]);

  useEffect(() => {
    if (lightboxOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => { document.body.style.overflow = ''; };
  }, [lightboxOpen]);

  if (!images || images.length === 0) {
    return (
      <div
        data-testid="photo-gallery-empty"
        style={{
          width: '100%', height: '400px', backgroundColor: '#e5e7eb',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          borderRadius: '12px', color: '#9ca3af', fontSize: '18px',
        }}
      >
        No images available
      </div>
    );
  }

  return (
    <div data-testid="photo-gallery" style={{ width: '100%' }}>
      {/* Main Image */}
      <div
        onClick={openLightbox}
        role="button"
        tabIndex={0}
        aria-label="Open fullscreen lightbox"
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') openLightbox(); }}
        style={{
          width: '100%', height: '500px', borderRadius: '12px',
          overflow: 'hidden', cursor: 'pointer', position: 'relative',
          backgroundColor: '#1f2937',
        }}
      >
        <img
          data-testid="main-image"
          src={images[activeIndex]}
          alt={`${alt} ${activeIndex + 1}`}
          style={{
            width: '100%', height: '100%', objectFit: 'cover',
            transition: 'opacity 0.4s ease-in-out',
          }}
        />
        <div
          style={{
            position: 'absolute', bottom: '12px', right: '12px',
            backgroundColor: 'rgba(0,0,0,0.6)', color: '#fff',
            padding: '4px 12px', borderRadius: '20px', fontSize: '14px',
            pointerEvents: 'none',
          }}
        >
          {activeIndex + 1} / {images.length}
        </div>
      </div>

      {/* Thumbnail Strip */}
      {images.length > 1 && (
        <div
          data-testid="thumbnail-strip"
          role="list"
          style={{
            display: 'flex', gap: '8px', marginTop: '12px',
            overflowX: 'auto', paddingBottom: '8px',
            scrollbarWidth: 'thin',
          }}
        >
          {images.map((src, index) => (
            <button
              key={`thumb-${index}`}
              role="listitem"
              data-testid={`thumbnail-${index}`}
              onClick={() => setActiveIndex(index)}
              aria-label={`View image ${index + 1}`}
              style={{
                flexShrink: 0, width: '100px', height: '72px',
                borderRadius: '8px', overflow: 'hidden', cursor: 'pointer',
                border: activeIndex === index ? '3px solid #2563eb' : '3px solid transparent',
                opacity: activeIndex === index ? 1 : 0.6,
                transition: 'opacity 0.3s ease, border-color 0.3s ease',
                padding: 0, background: 'none',
              }}
            >
              <img
                src={src}
                alt={`${alt} thumbnail ${index + 1}`}
                style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
              />
            </button>
          ))}
        </div>
      )}

      {/* Lightbox Modal */}
      {lightboxOpen && (
        <div
          data-testid="lightbox-overlay"
          role="dialog"
          aria-modal="true"
          aria-label="Image lightbox"
          onClick={closeLightbox}
          style={{
            position: 'fixed', inset: 0, zIndex: 9999,
            backgroundColor: 'rgba(0,0,0,0.85)',
            backdropFilter: 'blur(8px)', WebkitBackdropFilter: 'blur(8px)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexDirection: 'column',
          }}
        >
          {/* Close Button */}
          <button
            data-testid="lightbox-close"
            onClick={(e) => { e.stopPropagation(); closeLightbox(); }}
            aria-label="Close lightbox"
            style={{
              position: 'absolute', top: '20px', right: '20px',
              background: 'rgba(255,255,255,0.15)', border: 'none',
              color: '#fff', fontSize: '28px', width: '48px', height: '48px',
              borderRadius: '50%', cursor: 'pointer', display: 'flex',
              alignItems: 'center', justifyContent: 'center',
              transition: 'background 0.2s ease',
            }}
            onMouseEnter={(e) => { (e.target as HTMLElement).style.background = 'rgba(255,255,255,0.3)'; }}
            onMouseLeave={(e) => { (e.target as HTMLElement).style.background = 'rgba(255,255,255,0.15)'; }}
          >
            ✕
          </button>

          {/* Prev Button */}
          {images.length > 1 && (
            <button
              data-testid="lightbox-prev"
              onClick={(e) => { e.stopPropagation(); goToPrev(); }}
              aria-label="Previous image"
              style={{
                position: 'absolute', left: '20px', top: '50%',
                transform: 'translateY(-50%)',
                background: 'rgba(255,255,255,0.15)', border: 'none',
                color: '#fff', fontSize: '24px', width: '48px', height: '48px',
                borderRadius: '50%', cursor: 'pointer', display: 'flex',
                alignItems: 'center', justifyContent: 'center',
                transition: 'background 0.2s ease',
              }}
            >
              ‹
            </button>
          )}

          {/* Lightbox Image */}
          <img
            data-testid="lightbox-image"
            src={images[lightboxIndex]}
            alt={`${alt} fullscreen ${lightboxIndex + 1}`}
            onClick={(e) => e.stopPropagation()}
            style={{
              maxWidth: '90vw', maxHeight: '85vh', objectFit: 'contain',
              borderRadius: '8px',
              transition: 'opacity 0.3s ease-in-out',
            }}
          />

          {/* Next Button */}
          {images.length > 1 && (
            <button
              data-testid="lightbox-next"
              onClick={(e) => { e.stopPropagation(); goToNext(); }}
              aria-label="Next image"
              style={{
                position: 'absolute', right: '20px', top: '50%',
                transform: 'translateY(-50%)',
                background: 'rgba(255,255,255,0.15)', border: 'none',
                color: '#fff', fontSize: '24px', width: '48px', height: '48px',
                borderRadius: '50%', cursor: 'pointer', display: 'flex',
                alignItems: 'center', justifyContent: 'center',
                transition: 'background 0.2s ease',
              }}
            >
              ›
            </button>
          )}

          {/* Counter */}
          <div
            style={{
              color: '#fff', marginTop: '16px', fontSize: '16px',
              background: 'rgba(0,0,0,0.5)', padding: '6px 16px',
              borderRadius: '20px',
            }}
          >
            {lightboxIndex + 1} / {images.length}
          </div>
        </div>
      )}
    </div>
  );
};

export default PhotoGallery;
