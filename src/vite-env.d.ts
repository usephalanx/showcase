/// <reference types="vite/client" />

/**
 * Type declarations for CSS modules.
 *
 * Allows TypeScript to understand default imports from .module.css files.
 */
declare module '*.module.css' {
  const classes: { readonly [key: string]: string };
  export default classes;
}
