/**
 * Tests for GET /api/auth/me
 */
import { request, makeRegisterPayload } from "./helpers";
import * as userStore from "../src/store/userStore";
import * as refreshTokenStore from "../src/store/refreshTokenStore";

beforeEach(() => {
  userStore.clear();
  refreshTokenStore.clear();
});

describe("GET /api/auth/me", () => {
  it("should return the current user when authenticated", async () => {
    const payload = makeRegisterPayload();
    const registerRes = await request.post("/api/auth/register").send(payload);
    const { accessToken } = registerRes.body;

    const res = await request
      .get("/api/auth/me")
      .set("Authorization", `Bearer ${accessToken}`);

    expect(res.status).toBe(200);
    expect(res.body.user).toBeDefined();
    expect(res.body.user.email).toBe(payload.email.toLowerCase());
    expect(res.body.user.passwordHash).toBeUndefined();
  });

  it("should return 401 without an Authorization header", async () => {
    const res = await request.get("/api/auth/me");
    expect(res.status).toBe(401);
  });

  it("should return 401 with an invalid token", async () => {
    const res = await request
      .get("/api/auth/me")
      .set("Authorization", "Bearer invalid.token.here");
    expect(res.status).toBe(401);
  });
});
