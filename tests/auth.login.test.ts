/**
 * Tests for POST /api/auth/login
 */
import { request, makeRegisterPayload } from "./helpers";
import * as userStore from "../src/store/userStore";
import * as refreshTokenStore from "../src/store/refreshTokenStore";

beforeEach(() => {
  userStore.clear();
  refreshTokenStore.clear();
});

describe("POST /api/auth/login", () => {
  it("should login an existing user and return tokens", async () => {
    const payload = makeRegisterPayload({ email: "login@example.com" });
    await request.post("/api/auth/register").send(payload);

    const res = await request.post("/api/auth/login").send({
      email: payload.email,
      password: payload.password,
    });

    expect(res.status).toBe(200);
    expect(res.body.message).toBe("Login successful");
    expect(res.body.accessToken).toBeDefined();
    expect(res.body.refreshToken).toBeDefined();
    expect(res.body.user.email).toBe(payload.email.toLowerCase());
  });

  it("should return 401 for wrong password", async () => {
    const payload = makeRegisterPayload({ email: "wrong@example.com" });
    await request.post("/api/auth/register").send(payload);

    const res = await request.post("/api/auth/login").send({
      email: payload.email,
      password: "WrongPassword!",
    });

    expect(res.status).toBe(401);
    expect(res.body.message).toMatch(/invalid/i);
  });

  it("should return 401 for non-existent email", async () => {
    const res = await request.post("/api/auth/login").send({
      email: "nobody@example.com",
      password: "SomePassword1",
    });
    expect(res.status).toBe(401);
  });

  it("should return 400 for missing fields", async () => {
    const res = await request.post("/api/auth/login").send({});
    expect(res.status).toBe(400);
  });
});
