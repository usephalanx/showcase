import { useCallback } from 'react';
import { scrollToElement } from '@/utils/scrollTo';

/**
 * Custom hook that returns a click handler for smooth-scrolling to a section.
 *
 * @param offset - Vertical offset in pixels to account for fixed headers.
 * @returns A function that accepts a section ID and scrolls to it.
 *
 * @example
 * ```tsx
 * const scrollTo = useSmoothScroll(80);
 * <button onClick={() => scrollTo('contact')}>Contact</button>
 * ```
 */
export function useSmoothScroll(offset: number = 80): (sectionId: string) => void {
  const scrollTo = useCallback(
    (sectionId: string) => {
      scrollToElement(sectionId, offset);
    },
    [offset],
  );

  return scrollTo;
}
