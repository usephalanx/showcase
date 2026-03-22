/**
 * Tests for Zod validation schemas.
 */
import {
  registerSchema,
  loginSchema,
  refreshTokenSchema,
} from "../src/validation/auth.schema";

describe("registerSchema", () => {
  it("should accept valid input", () => {
    const result = registerSchema.safeParse({
      email: "user@example.com",
      password: "StrongP@ss1",
      firstName: "John",
      lastName: "Doe",
    });
    expect(result.success).toBe(true);
  });

  it("should default role to patient", () => {
    const result = registerSchema.parse({
      email: "user@example.com",
      password: "StrongP@ss1",
      firstName: "John",
      lastName: "Doe",
    });
    expect(result.role).toBe("patient");
  });

  it("should reject short passwords", () => {
    const result = registerSchema.safeParse({
      email: "user@example.com",
      password: "short",
      firstName: "John",
      lastName: "Doe",
    });
    expect(result.success).toBe(false);
  });

  it("should reject invalid roles", () => {
    const result = registerSchema.safeParse({
      email: "user@example.com",
      password: "StrongP@ss1",
      firstName: "John",
      lastName: "Doe",
      role: "superuser",
    });
    expect(result.success).toBe(false);
  });
});

describe("loginSchema", () => {
  it("should accept valid input", () => {
    const result = loginSchema.safeParse({
      email: "user@example.com",
      password: "password",
    });
    expect(result.success).toBe(true);
  });

  it("should reject missing email", () => {
    const result = loginSchema.safeParse({ password: "password" });
    expect(result.success).toBe(false);
  });
});

describe("refreshTokenSchema", () => {
  it("should accept valid input", () => {
    const result = refreshTokenSchema.safeParse({
      refreshToken: "some.jwt.token",
    });
    expect(result.success).toBe(true);
  });

  it("should reject empty refreshToken", () => {
    const result = refreshTokenSchema.safeParse({ refreshToken: "" });
    expect(result.success).toBe(false);
  });
});
