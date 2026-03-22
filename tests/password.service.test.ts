/**
 * Tests for password hashing service.
 */
import { hashPassword, comparePassword } from "../src/services/password.service";

describe("password service", () => {
  it("should hash a password and verify it", async () => {
    const plain = "MySecretP@ss1";
    const hash = await hashPassword(plain);

    expect(hash).not.toBe(plain);
    expect(hash.startsWith("$2")).toBe(true); // bcrypt prefix

    const match = await comparePassword(plain, hash);
    expect(match).toBe(true);
  });

  it("should reject a wrong password", async () => {
    const hash = await hashPassword("CorrectPassword1");
    const match = await comparePassword("WrongPassword1", hash);
    expect(match).toBe(false);
  });
});
