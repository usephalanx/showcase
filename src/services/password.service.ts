/**
 * Password hashing and comparison helpers wrapping bcrypt.
 */
import bcrypt from "bcrypt";
import { config } from "../config";

/**
 * Hash a plain-text password using bcrypt.
 *
 * @param plainText - The raw password to hash.
 * @returns The bcrypt hash string.
 */
export async function hashPassword(plainText: string): Promise<string> {
  return bcrypt.hash(plainText, config.bcryptSaltRounds);
}

/**
 * Compare a plain-text password against a bcrypt hash.
 *
 * @param plainText - The raw password provided by the user.
 * @param hash - The stored bcrypt hash.
 * @returns `true` if the password matches.
 */
export async function comparePassword(
  plainText: string,
  hash: string,
): Promise<boolean> {
  return bcrypt.compare(plainText, hash);
}
