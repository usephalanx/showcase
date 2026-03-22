/**
 * Tests for POST /api/auth/refresh-token
 */
import { request, makeRegisterPayload } from "./helpers";
import * as userStore from "../src/store/userStore";
import * as refreshTokenStore from "../src/store/refreshTokenStore";

beforeEach(() => {
  userStore.clear();
  refreshTokenStore.clear();
});

describe("POST /api/auth/refresh-token", () => {
  it("should issue new tokens with a valid refresh token", async () => {
    const payload = makeRegisterPayload();
    const registerRes = await request.post("/api/auth/register").send(payload);
    const { refreshToken } = registerRes.body;

    const res = await request
      .post("/api/auth/refresh-token")
      .send({ refreshToken });

    expect(res.status).toBe(200);
    expect(res.body.accessToken).toBeDefined();
    expect(res.body.refreshToken).toBeDefined();
    // The old refresh token should now be rotated (different)
    expect(res.body.refreshToken).not.toBe(refreshToken);
  });

  it("should reject a reused (rotated) refresh token", async () => {
    const payload = makeRegisterPayload();
    const registerRes = await request.post("/api/auth/register").send(payload);
    const { refreshToken } = registerRes.body;

    // First refresh — should succeed
    await request.post("/api/auth/refresh-token").send({ refreshToken });

    // Second use of the same token — should fail
    const res = await request
      .post("/api/auth/refresh-token")
      .send({ refreshToken });

    expect(res.status).toBe(401);
  });

  it("should return 401 for a garbage token", async () => {
    const res = await request
      .post("/api/auth/refresh-token")
      .send({ refreshToken: "garbage.token.value" });

    expect(res.status).toBe(401);
  });

  it("should return 400 when refreshToken is missing", async () => {
    const res = await request.post("/api/auth/refresh-token").send({});
    expect(res.status).toBe(400);
  });
});
