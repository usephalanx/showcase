/**
 * Role-based access control middleware.
 *
 * Usage:
 *   router.get('/admin-only', authenticate, authorize('admin'), handler);
 *   router.get('/staff', authenticate, authorize('admin', 'dentist', 'receptionist'), handler);
 */
import { Request, Response, NextFunction } from "express";
import { UserRole } from "../types";

/**
 * Returns middleware that allows access only to users whose role is in the provided list.
 *
 * @param allowedRoles - One or more UserRole values that are permitted.
 */
export function authorize(...allowedRoles: UserRole[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.user) {
      res.status(401).json({ message: "Authentication required" });
      return;
    }

    if (!allowedRoles.includes(req.user.role)) {
      res.status(403).json({
        message: "Forbidden: insufficient permissions",
        requiredRoles: allowedRoles,
        yourRole: req.user.role,
      });
      return;
    }

    next();
  };
}
