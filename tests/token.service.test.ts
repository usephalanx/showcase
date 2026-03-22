/**
 * Tests for JWT token service.
 */
import {
  generateAccessToken,
  generateRefreshToken,
  verifyAccessToken,
  verifyRefreshToken,
} from "../src/services/token.service";
import { UserRole } from "../src/types";

describe("token service", () => {
  const accessPayload = {
    userId: "user-123",
    email: "test@example.com",
    role: UserRole.DENTIST,
  };

  const refreshPayload = {
    userId: "user-123",
    tokenVersion: 0,
  };

  it("should generate and verify an access token", () => {
    const token = generateAccessToken(accessPayload);
    expect(typeof token).toBe("string");

    const decoded = verifyAccessToken(token);
    expect(decoded.userId).toBe(accessPayload.userId);
    expect(decoded.email).toBe(accessPayload.email);
    expect(decoded.role).toBe(accessPayload.role);
  });

  it("should generate and verify a refresh token", () => {
    const token = generateRefreshToken(refreshPayload);
    expect(typeof token).toBe("string");

    const decoded = verifyRefreshToken(token);
    expect(decoded.userId).toBe(refreshPayload.userId);
    expect(decoded.tokenVersion).toBe(refreshPayload.tokenVersion);
  });

  it("should throw on an invalid access token", () => {
    expect(() => verifyAccessToken("bad.token")).toThrow();
  });

  it("should throw on an invalid refresh token", () => {
    expect(() => verifyRefreshToken("bad.token")).toThrow();
  });
});
