const { defaults } = require("jest-config")

module.exports = {
  ...defaults,
  moduleFileExtensions: ["js"],
  testPathIgnorePatterns: ["<rootDir>/scripts/", "<rootDir>/node_modules/"],
  collectCoverage: true,
  coveragePathIgnorePatterns: ["/scripts/", "/node_modules/"],
  coverageReporters: ["json", "lcov", "text", "text-summary"],
  collectCoverageFrom: ["src/**/*.{js,jsx,ts,tsx}"],
  // The setupFiles array lets you list files that will be read before all tests are run
  setupFiles: [`<rootDir>/tests/support/env-variables.js`],
}
