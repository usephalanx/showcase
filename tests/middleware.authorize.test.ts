/**
 * Tests for the authorize (RBAC) middleware.
 */
import { request, makeRegisterPayload } from "./helpers";
import * as userStore from "../src/store/userStore";
import * as refreshTokenStore from "../src/store/refreshTokenStore";
import app from "../src/app";
import { authenticate } from "../src/middleware/authenticate";
import { authorize } from "../src/middleware/authorize";
import { UserRole } from "../src/types";
import { Router } from "express";

// Register a test-only protected route
const testRouter = Router();
testRouter.get(
  "/admin-only",
  authenticate,
  authorize(UserRole.ADMIN),
  (_req, res) => {
    res.json({ ok: true });
  },
);
testRouter.get(
  "/staff",
  authenticate,
  authorize(UserRole.ADMIN, UserRole.DENTIST, UserRole.RECEPTIONIST),
  (_req, res) => {
    res.json({ ok: true });
  },
);
app.use("/test-rbac", testRouter);

beforeEach(() => {
  userStore.clear();
  refreshTokenStore.clear();
});

describe("authorize middleware", () => {
  it("should allow an admin to access admin-only routes", async () => {
    const payload = makeRegisterPayload({ role: "admin", email: "admin@test.com" });
    const reg = await request.post("/api/auth/register").send(payload);

    const res = await request
      .get("/test-rbac/admin-only")
      .set("Authorization", `Bearer ${reg.body.accessToken}`);

    expect(res.status).toBe(200);
    expect(res.body.ok).toBe(true);
  });

  it("should forbid a patient from accessing admin-only routes", async () => {
    const payload = makeRegisterPayload({ role: "patient", email: "pat@test.com" });
    const reg = await request.post("/api/auth/register").send(payload);

    const res = await request
      .get("/test-rbac/admin-only")
      .set("Authorization", `Bearer ${reg.body.accessToken}`);

    expect(res.status).toBe(403);
    expect(res.body.message).toMatch(/forbidden/i);
  });

  it("should allow a dentist to access staff routes", async () => {
    const payload = makeRegisterPayload({ role: "dentist", email: "dentist@test.com" });
    const reg = await request.post("/api/auth/register").send(payload);

    const res = await request
      .get("/test-rbac/staff")
      .set("Authorization", `Bearer ${reg.body.accessToken}`);

    expect(res.status).toBe(200);
  });

  it("should forbid a patient from accessing staff routes", async () => {
    const payload = makeRegisterPayload({ role: "patient", email: "pat2@test.com" });
    const reg = await request.post("/api/auth/register").send(payload);

    const res = await request
      .get("/test-rbac/staff")
      .set("Authorization", `Bearer ${reg.body.accessToken}`);

    expect(res.status).toBe(403);
  });
});
