/**
 * Shared domain types used across the application.
 */

/** Available user roles in the system. */
export enum UserRole {
  ADMIN = "admin",
  DENTIST = "dentist",
  RECEPTIONIST = "receptionist",
  PATIENT = "patient",
}

/** Persisted user record. */
export interface User {
  id: string;
  email: string;
  passwordHash: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  createdAt: Date;
  updatedAt: Date;
}

/** Public-facing user representation (no password hash). */
export interface UserPublic {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  createdAt: Date;
  updatedAt: Date;
}

/** JWT access-token payload shape. */
export interface JwtPayload {
  userId: string;
  email: string;
  role: UserRole;
}

/** JWT refresh-token payload shape. */
export interface JwtRefreshPayload {
  userId: string;
  tokenVersion: number;
}

/** Stored refresh-token metadata. */
export interface RefreshTokenRecord {
  token: string;
  userId: string;
  expiresAt: Date;
}
