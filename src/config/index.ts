/**
 * Application configuration loaded from environment variables.
 * Never hardcode secrets — always use env vars.
 */
export interface AppConfig {
  /** Port the HTTP server listens on. */
  port: number;
  /** Secret used to sign JWT access tokens. */
  jwtSecret: string;
  /** Secret used to sign JWT refresh tokens. */
  jwtRefreshSecret: string;
  /** Access token lifetime (e.g. "15m"). */
  jwtExpiresIn: string;
  /** Refresh token lifetime (e.g. "7d"). */
  jwtRefreshExpiresIn: string;
  /** Bcrypt salt rounds. */
  bcryptSaltRounds: number;
  /** Current runtime environment. */
  nodeEnv: string;
}

export const config: AppConfig = {
  port: parseInt(process.env.PORT ?? "3000", 10),
  jwtSecret: process.env.JWT_SECRET ?? "dev-access-secret-change-me",
  jwtRefreshSecret: process.env.JWT_REFRESH_SECRET ?? "dev-refresh-secret-change-me",
  jwtExpiresIn: process.env.JWT_EXPIRES_IN ?? "15m",
  jwtRefreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN ?? "7d",
  bcryptSaltRounds: parseInt(process.env.BCRYPT_SALT_ROUNDS ?? "12", 10),
  nodeEnv: process.env.NODE_ENV ?? "development",
};
