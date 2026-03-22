/**
 * Core authentication business logic.
 */
import { v4 as uuidv4 } from "uuid";
import { User, UserPublic, UserRole, RefreshTokenRecord } from "../types";
import * as userStore from "../store/userStore";
import * as refreshTokenStore from "../store/refreshTokenStore";
import { hashPassword, comparePassword } from "./password.service";
import {
  generateAccessToken,
  generateRefreshToken,
  verifyRefreshToken,
} from "./token.service";

/** Convert a full User to its public projection (no password hash). */
export function toPublic(user: User): UserPublic {
  return {
    id: user.id,
    email: user.email,
    firstName: user.firstName,
    lastName: user.lastName,
    role: user.role,
    createdAt: user.createdAt,
    updatedAt: user.updatedAt,
  };
}

/** Tokens returned after successful authentication. */
export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export interface RegisterParams {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role?: UserRole;
}

/**
 * Register a new user.
 *
 * @throws Error if a user with the given email already exists.
 */
export async function register(
  params: RegisterParams,
): Promise<{ user: UserPublic; tokens: AuthTokens }> {
  const existing = userStore.findByEmail(params.email);
  if (existing) {
    throw new ConflictError("A user with this email already exists");
  }

  const now = new Date();
  const user: User = {
    id: uuidv4(),
    email: params.email.toLowerCase(),
    passwordHash: await hashPassword(params.password),
    firstName: params.firstName,
    lastName: params.lastName,
    role: params.role ?? UserRole.PATIENT,
    createdAt: now,
    updatedAt: now,
  };

  userStore.create(user);

  const tokens = issueTokens(user);

  return { user: toPublic(user), tokens };
}

export interface LoginParams {
  email: string;
  password: string;
}

/**
 * Authenticate a user with email and password.
 *
 * @throws UnauthorizedError on invalid credentials.
 */
export async function login(
  params: LoginParams,
): Promise<{ user: UserPublic; tokens: AuthTokens }> {
  const user = userStore.findByEmail(params.email);
  if (!user) {
    throw new UnauthorizedError("Invalid email or password");
  }

  const passwordMatches = await comparePassword(params.password, user.passwordHash);
  if (!passwordMatches) {
    throw new UnauthorizedError("Invalid email or password");
  }

  const tokens = issueTokens(user);

  return { user: toPublic(user), tokens };
}

/**
 * Refresh an access token using a valid refresh token.
 *
 * @throws UnauthorizedError if the refresh token is invalid or revoked.
 */
export function refreshAccessToken(
  refreshToken: string,
): { accessToken: string; refreshToken: string } {
  let payload;
  try {
    payload = verifyRefreshToken(refreshToken);
  } catch {
    throw new UnauthorizedError("Invalid or expired refresh token");
  }

  const stored = refreshTokenStore.findByToken(refreshToken);
  if (!stored) {
    throw new UnauthorizedError("Refresh token has been revoked");
  }

  // Remove the old refresh token (rotation)
  refreshTokenStore.remove(refreshToken);

  const user = userStore.findById(payload.userId);
  if (!user) {
    throw new UnauthorizedError("User no longer exists");
  }

  const tokens = issueTokens(user);
  return tokens;
}

/**
 * Get the current user by id.
 *
 * @throws NotFoundError if the user does not exist.
 */
export function getMe(userId: string): UserPublic {
  const user = userStore.findById(userId);
  if (!user) {
    throw new NotFoundError("User not found");
  }
  return toPublic(user);
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Issue both an access and refresh token for the given user. */
function issueTokens(user: User): AuthTokens {
  const accessToken = generateAccessToken({
    userId: user.id,
    email: user.email,
    role: user.role,
  });

  const refreshToken = generateRefreshToken({
    userId: user.id,
    tokenVersion: 0,
  });

  // Persist refresh-token record
  const expiresAt = new Date();
  expiresAt.setDate(expiresAt.getDate() + 7);
  const record: RefreshTokenRecord = {
    token: refreshToken,
    userId: user.id,
    expiresAt,
  };
  refreshTokenStore.save(record);

  return { accessToken, refreshToken };
}

// ---------------------------------------------------------------------------
// Custom error classes
// ---------------------------------------------------------------------------

export class ConflictError extends Error {
  /** HTTP 409 conflict error. */
  public readonly statusCode = 409;
  constructor(message: string) {
    super(message);
    this.name = "ConflictError";
  }
}

export class UnauthorizedError extends Error {
  /** HTTP 401 unauthorized error. */
  public readonly statusCode = 401;
  constructor(message: string) {
    super(message);
    this.name = "UnauthorizedError";
  }
}

export class NotFoundError extends Error {
  /** HTTP 404 not found error. */
  public readonly statusCode = 404;
  constructor(message: string) {
    super(message);
    this.name = "NotFoundError";
  }
}

export class ForbiddenError extends Error {
  /** HTTP 403 forbidden error. */
  public readonly statusCode = 403;
  constructor(message: string) {
    super(message);
    this.name = "ForbiddenError";
  }
}
