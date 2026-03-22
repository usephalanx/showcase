/**
 * In-memory refresh-token store.
 *
 * Tracks issued refresh tokens so they can be validated and revoked.
 * Replace with a persistent store (e.g. Redis, database) in production.
 */
import { RefreshTokenRecord } from "../types";

const tokens: Map<string, RefreshTokenRecord> = new Map();

/** Save a refresh-token record. */
export function save(record: RefreshTokenRecord): void {
  tokens.set(record.token, record);
}

/** Find a refresh-token record by the token string. */
export function findByToken(token: string): RefreshTokenRecord | undefined {
  return tokens.get(token);
}

/** Remove a refresh-token record (revoke). */
export function remove(token: string): boolean {
  return tokens.delete(token);
}

/** Remove all tokens for a specific user. */
export function removeAllForUser(userId: string): void {
  for (const [key, record] of tokens.entries()) {
    if (record.userId === userId) {
      tokens.delete(key);
    }
  }
}

/** Clear all stored tokens (useful for tests). */
export function clear(): void {
  tokens.clear();
}
