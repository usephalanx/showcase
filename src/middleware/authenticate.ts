/**
 * Express middleware that verifies the JWT access token from the Authorization header.
 * On success, attaches the decoded payload to `req.user`.
 */
import { Request, Response, NextFunction } from "express";
import { verifyAccessToken } from "../services/token.service";
import { JwtPayload } from "../types";

// Extend Express Request to carry authenticated user info.
declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload;
    }
  }
}

/**
 * Middleware that requires a valid Bearer token in the Authorization header.
 */
export function authenticate(
  req: Request,
  res: Response,
  next: NextFunction,
): void {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    res.status(401).json({ message: "Missing or malformed authorization header" });
    return;
  }

  const token = authHeader.slice(7); // strip "Bearer "

  try {
    const payload = verifyAccessToken(token);
    req.user = payload;
    next();
  } catch {
    res.status(401).json({ message: "Invalid or expired access token" });
  }
}
