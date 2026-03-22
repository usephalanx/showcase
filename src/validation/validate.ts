/**
 * Express middleware factory that validates request bodies against Zod schemas.
 */
import { Request, Response, NextFunction } from "express";
import { ZodSchema, ZodError } from "zod";

/**
 * Returns an Express middleware that validates `req.body` with the provided Zod schema.
 * On success the parsed (and potentially defaulted/transformed) body replaces `req.body`.
 * On failure a 400 JSON response with structured errors is returned.
 */
export function validate<T>(schema: ZodSchema<T>) {
  return (req: Request, res: Response, next: NextFunction): void => {
    try {
      const parsed = schema.parse(req.body);
      req.body = parsed;
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        const errors = error.errors.map((e) => ({
          field: e.path.join("."),
          message: e.message,
        }));
        res.status(400).json({ message: "Validation failed", errors });
        return;
      }
      next(error);
    }
  };
}
