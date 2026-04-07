/**
 * Smoothly scroll to an element identified by its DOM id.
 *
 * @param elementId - The id attribute of the target element (without '#').
 * @param offset - Optional vertical offset in pixels (e.g. for fixed headers).
 */
export function scrollToElement(elementId: string, offset: number = 0): void {
  const element = document.getElementById(elementId);
  if (!element) {
    return;
  }

  const elementPosition = element.getBoundingClientRect().top + window.scrollY;
  const offsetPosition = elementPosition - offset;

  window.scrollTo({
    top: offsetPosition,
    behavior: 'smooth',
  });
}
