/**
 * Shared test helpers.
 */
import supertest from "supertest";
import app from "../src/app";

/** Pre-configured supertest agent bound to the Express app. */
export const request = supertest(app);

/** Standard registration payload factory. */
export function makeRegisterPayload(overrides: Record<string, unknown> = {}) {
  return {
    email: `test-${Date.now()}@example.com`,
    password: "SecurePass123!",
    firstName: "Jane",
    lastName: "Doe",
    ...overrides,
  };
}
