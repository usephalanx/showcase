/// <reference types="vite/client" />

/**
 * Type declarations for CSS module imports.
 * Allows TypeScript to understand .module.css imports.
 */
declare module "*.module.css" {
  const classes: { readonly [key: string]: string };
  export default classes;
}
