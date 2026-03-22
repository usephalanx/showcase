/**
 * JWT token generation and verification helpers.
 */
import jwt from "jsonwebtoken";
import { config } from "../config";
import { JwtPayload, JwtRefreshPayload, UserRole } from "../types";

/**
 * Generate a short-lived access token.
 */
export function generateAccessToken(payload: JwtPayload): string {
  return jwt.sign(payload, config.jwtSecret, {
    expiresIn: config.jwtExpiresIn,
  });
}

/**
 * Generate a long-lived refresh token.
 */
export function generateRefreshToken(payload: JwtRefreshPayload): string {
  return jwt.sign(payload, config.jwtRefreshSecret, {
    expiresIn: config.jwtRefreshExpiresIn,
  });
}

/**
 * Verify and decode an access token.
 *
 * @throws {jwt.JsonWebTokenError} if the token is invalid or expired.
 */
export function verifyAccessToken(token: string): JwtPayload {
  const decoded = jwt.verify(token, config.jwtSecret) as JwtPayload & {
    iat: number;
    exp: number;
  };
  return {
    userId: decoded.userId,
    email: decoded.email,
    role: decoded.role as UserRole,
  };
}

/**
 * Verify and decode a refresh token.
 *
 * @throws {jwt.JsonWebTokenError} if the token is invalid or expired.
 */
export function verifyRefreshToken(token: string): JwtRefreshPayload {
  const decoded = jwt.verify(token, config.jwtRefreshSecret) as JwtRefreshPayload & {
    iat: number;
    exp: number;
  };
  return {
    userId: decoded.userId,
    tokenVersion: decoded.tokenVersion,
  };
}
