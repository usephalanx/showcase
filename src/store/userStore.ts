/**
 * In-memory user store.
 *
 * This is a simple Map-based store suitable for development and testing.
 * Replace with a real database (e.g. PostgreSQL via Prisma/Knex) for production.
 */
import { User } from "../types";

const users: Map<string, User> = new Map();

/** Retrieve a user by their unique id. */
export function findById(id: string): User | undefined {
  return users.get(id);
}

/** Retrieve a user by email (case-insensitive). */
export function findByEmail(email: string): User | undefined {
  const normalised = email.toLowerCase();
  for (const user of users.values()) {
    if (user.email === normalised) {
      return user;
    }
  }
  return undefined;
}

/** Persist a new user. */
export function create(user: User): User {
  users.set(user.id, user);
  return user;
}

/** Delete all users (useful for tests). */
export function clear(): void {
  users.clear();
}

/** Return the current count of stored users. */
export function count(): number {
  return users.size;
}
