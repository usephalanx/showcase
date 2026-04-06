/**
 * Barrel export for all API service modules and the shared client.
 *
 * Usage:
 * ```ts
 * import { boardsApi, columnsApi, cardsApi, tagsApi } from '@/api';
 * ```
 */

export { default as apiClient } from './client';
export { boardsApi } from './boards';
export { columnsApi } from './columns';
export { cardsApi } from './cards';
export { tagsApi } from './tags';
