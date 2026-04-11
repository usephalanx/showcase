/// <reference types="vite/client" />

/**
 * Type declarations for CSS module imports.
 *
 * Allows TypeScript to understand `import styles from '*.module.css'`
 * and treat the default export as a record of string class names.
 */
declare module '*.module.css' {
  const classes: { readonly [key: string]: string };
  export default classes;
}
