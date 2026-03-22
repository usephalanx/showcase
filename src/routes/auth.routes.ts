/**
 * Authentication route definitions.
 *
 * POST /api/auth/register
 * POST /api/auth/login
 * POST /api/auth/refresh-token
 * GET  /api/auth/me
 */
import { Router, Request, Response, NextFunction } from "express";
import * as authService from "../services/auth.service";
import { authenticate } from "../middleware/authenticate";
import { validate } from "../validation/validate";
import {
  registerSchema,
  loginSchema,
  refreshTokenSchema,
} from "../validation/auth.schema";

const router = Router();

/** POST /api/auth/register — Create a new user account. */
router.post(
  "/register",
  validate(registerSchema),
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const result = await authService.register(req.body);
      res.status(201).json({
        message: "User registered successfully",
        user: result.user,
        accessToken: result.tokens.accessToken,
        refreshToken: result.tokens.refreshToken,
      });
    } catch (error) {
      next(error);
    }
  },
);

/** POST /api/auth/login — Authenticate with email and password. */
router.post(
  "/login",
  validate(loginSchema),
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const result = await authService.login(req.body);
      res.status(200).json({
        message: "Login successful",
        user: result.user,
        accessToken: result.tokens.accessToken,
        refreshToken: result.tokens.refreshToken,
      });
    } catch (error) {
      next(error);
    }
  },
);

/** POST /api/auth/refresh-token — Exchange a refresh token for new tokens. */
router.post(
  "/refresh-token",
  validate(refreshTokenSchema),
  (req: Request, res: Response, next: NextFunction): void => {
    try {
      const { refreshToken } = req.body;
      const tokens = authService.refreshAccessToken(refreshToken);
      res.status(200).json({
        message: "Token refreshed successfully",
        accessToken: tokens.accessToken,
        refreshToken: tokens.refreshToken,
      });
    } catch (error) {
      next(error);
    }
  },
);

/** GET /api/auth/me — Return the currently authenticated user. */
router.get(
  "/me",
  authenticate,
  (req: Request, res: Response, next: NextFunction): void => {
    try {
      const user = authService.getMe(req.user!.userId);
      res.status(200).json({ user });
    } catch (error) {
      next(error);
    }
  },
);

export default router;
