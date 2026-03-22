/**
 * Zod schemas for request validation on auth endpoints.
 */
import { z } from "zod";
import { UserRole } from "../types";

/** Schema for POST /api/auth/register */
export const registerSchema = z.object({
  email: z
    .string({ required_error: "Email is required" })
    .email("Invalid email address")
    .max(255, "Email must be at most 255 characters"),
  password: z
    .string({ required_error: "Password is required" })
    .min(8, "Password must be at least 8 characters")
    .max(128, "Password must be at most 128 characters"),
  firstName: z
    .string({ required_error: "First name is required" })
    .min(1, "First name is required")
    .max(100, "First name must be at most 100 characters"),
  lastName: z
    .string({ required_error: "Last name is required" })
    .min(1, "Last name is required")
    .max(100, "Last name must be at most 100 characters"),
  role: z
    .nativeEnum(UserRole, {
      errorMap: () => ({
        message: `Role must be one of: ${Object.values(UserRole).join(", ")}`,
      }),
    })
    .optional()
    .default(UserRole.PATIENT),
});

/** Schema for POST /api/auth/login */
export const loginSchema = z.object({
  email: z
    .string({ required_error: "Email is required" })
    .email("Invalid email address"),
  password: z
    .string({ required_error: "Password is required" })
    .min(1, "Password is required"),
});

/** Schema for POST /api/auth/refresh-token */
export const refreshTokenSchema = z.object({
  refreshToken: z
    .string({ required_error: "Refresh token is required" })
    .min(1, "Refresh token is required"),
});

export type RegisterInput = z.infer<typeof registerSchema>;
export type LoginInput = z.infer<typeof loginSchema>;
export type RefreshTokenInput = z.infer<typeof refreshTokenSchema>;
