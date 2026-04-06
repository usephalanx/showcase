/**
 * Tests for the App component and route definitions.
 *
 * Uses MemoryRouter to simulate navigation and verify that the
 * correct page components render for each route.
 */

import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import App from "../src/App";

/**
 * Helper to render App at a specific route path.
 */
function renderAtPath(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  );
}

describe("App routing", () => {
  it('should render the HomePage at "/"', () => {
    renderAtPath("/");
    expect(
      screen.getByText("Find Your Dream Home"),
    ).toBeDefined();
  });

  it('should render the HomePage with "Featured Properties" section', () => {
    renderAtPath("/");
    expect(
      screen.getByText("Featured Properties"),
    ).toBeDefined();
  });

  it('should render PropertyDetailPage at "/property/:id"', () => {
    renderAtPath("/property/prop-1");
    expect(
      screen.getByText("Modern Downtown Loft"),
    ).toBeDefined();
  });

  it("should render Property Not Found for an invalid property ID", () => {
    renderAtPath("/property/non-existent");
    expect(
      screen.getByText("Property Not Found"),
    ).toBeDefined();
  });

  it('should render the ContactPage at "/contact"', () => {
    renderAtPath("/contact");
    expect(screen.getByText("Contact Us")).toBeDefined();
  });

  it("should render the contact form fields", () => {
    renderAtPath("/contact");
    expect(screen.getByLabelText("Full Name")).toBeDefined();
    expect(screen.getByLabelText("Email Address")).toBeDefined();
    expect(screen.getByLabelText("Message")).toBeDefined();
  });
});
