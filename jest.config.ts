import type { Config } from 'jest';

/**
 * Jest configuration for the Madhuri Real Estate project.
 * Uses ts-jest for TypeScript support and jsdom for DOM testing.
 */
const config: Config = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.tsx?$': 'ts-jest',
  },
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/src/__mocks__/fileMock.ts',
  },
  testMatch: ['<rootDir>/src/__tests__/**/*.test.tsx'],
  setupFilesAfterSetup: [],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
};

export default config;
