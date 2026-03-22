/**
 * Centralised Express error-handling middleware.
 */
import { Request, Response, NextFunction } from "express";

/** Recognised application error with an HTTP status code. */
interface AppError extends Error {
  statusCode?: number;
}

/**
 * Global error handler — should be the last middleware registered.
 */
export function errorHandler(
  err: AppError,
  _req: Request,
  res: Response,
  _next: NextFunction,
): void {
  const statusCode = err.statusCode ?? 500;
  const message = statusCode === 500 ? "Internal server error" : err.message;

  if (statusCode === 500) {
    console.error("[ERROR]", err);
  }

  res.status(statusCode).json({ message });
}
