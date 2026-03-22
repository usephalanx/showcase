/**
 * Tests for POST /api/auth/register
 */
import { request, makeRegisterPayload } from "./helpers";
import * as userStore from "../src/store/userStore";
import * as refreshTokenStore from "../src/store/refreshTokenStore";

beforeEach(() => {
  userStore.clear();
  refreshTokenStore.clear();
});

describe("POST /api/auth/register", () => {
  it("should register a new user and return tokens", async () => {
    const payload = makeRegisterPayload();
    const res = await request.post("/api/auth/register").send(payload);

    expect(res.status).toBe(201);
    expect(res.body.message).toBe("User registered successfully");
    expect(res.body.user).toBeDefined();
    expect(res.body.user.email).toBe(payload.email.toLowerCase());
    expect(res.body.user.firstName).toBe(payload.firstName);
    expect(res.body.user.role).toBe("patient");
    expect(res.body.accessToken).toBeDefined();
    expect(res.body.refreshToken).toBeDefined();
    // Must NOT expose password hash
    expect(res.body.user.passwordHash).toBeUndefined();
  });

  it("should return 409 when registering with a duplicate email", async () => {
    const payload = makeRegisterPayload({ email: "dup@example.com" });
    await request.post("/api/auth/register").send(payload);
    const res = await request.post("/api/auth/register").send(payload);

    expect(res.status).toBe(409);
    expect(res.body.message).toMatch(/already exists/i);
  });

  it("should return 400 for missing required fields", async () => {
    const res = await request.post("/api/auth/register").send({});
    expect(res.status).toBe(400);
    expect(res.body.errors).toBeDefined();
    expect(res.body.errors.length).toBeGreaterThan(0);
  });

  it("should return 400 for invalid email", async () => {
    const payload = makeRegisterPayload({ email: "not-an-email" });
    const res = await request.post("/api/auth/register").send(payload);
    expect(res.status).toBe(400);
  });

  it("should return 400 for password shorter than 8 characters", async () => {
    const payload = makeRegisterPayload({ password: "short" });
    const res = await request.post("/api/auth/register").send(payload);
    expect(res.status).toBe(400);
  });

  it("should accept a custom role", async () => {
    const payload = makeRegisterPayload({ role: "dentist" });
    const res = await request.post("/api/auth/register").send(payload);
    expect(res.status).toBe(201);
    expect(res.body.user.role).toBe("dentist");
  });

  it("should return 400 for an invalid role", async () => {
    const payload = makeRegisterPayload({ role: "superadmin" });
    const res = await request.post("/api/auth/register").send(payload);
    expect(res.status).toBe(400);
  });
});
