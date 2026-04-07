import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import TrustBadge from "./TrustBadge";

describe("TrustBadge", () => {
  it("renders without crashing", () => {
    const { container } = render(
      <TrustBadge icon="🏠" stat="200+" label="Homes Sold" />
    );
    expect(container).toBeTruthy();
  });

  it("displays the icon prop", () => {
    render(<TrustBadge icon="🏠" stat="200+" label="Homes Sold" />);
    const iconEl = screen.getByTestId("trust-badge-icon");
    expect(iconEl.textContent).toBe("🏠");
  });

  it("displays the stat prop with gold color", () => {
    render(<TrustBadge icon="🏠" stat="200+" label="Homes Sold" />);
    const statEl = screen.getByTestId("trust-badge-stat");
    expect(statEl.textContent).toBe("200+");
    expect(statEl.style.color).toBe("rgb(200, 169, 81)");
  });

  it("displays the label prop", () => {
    render(<TrustBadge icon="🏠" stat="200+" label="Homes Sold" />);
    const labelEl = screen.getByTestId("trust-badge-label");
    expect(labelEl.textContent).toBe("Homes Sold");
  });

  it("renders with different props for Licensed Agent", () => {
    render(<TrustBadge icon="📋" stat="✓" label="Licensed Agent" />);
    expect(screen.getByTestId("trust-badge-icon").textContent).toBe("📋");
    expect(screen.getByTestId("trust-badge-stat").textContent).toBe("✓");
    expect(screen.getByTestId("trust-badge-label").textContent).toBe("Licensed Agent");
  });

  it("renders with different props for 5★ Rated", () => {
    render(<TrustBadge icon="⭐" stat="5★" label="Rated" />);
    expect(screen.getByTestId("trust-badge-icon").textContent).toBe("⭐");
    expect(screen.getByTestId("trust-badge-stat").textContent).toBe("5★");
    expect(screen.getByTestId("trust-badge-label").textContent).toBe("Rated");
  });

  it("applies additional className when provided", () => {
    render(
      <TrustBadge
        icon="🏠"
        stat="200+"
        label="Homes Sold"
        className="p-4 bg-white"
      />
    );
    const badge = screen.getByTestId("trust-badge");
    expect(badge.className).toContain("p-4");
    expect(badge.className).toContain("bg-white");
  });

  it("has the correct aria-label on the icon for accessibility", () => {
    render(<TrustBadge icon="🏠" stat="200+" label="Homes Sold" />);
    const iconEl = screen.getByTestId("trust-badge-icon");
    expect(iconEl.getAttribute("aria-label")).toBe("Homes Sold");
  });

  it("has role=img on the icon element", () => {
    render(<TrustBadge icon="🏠" stat="200+" label="Homes Sold" />);
    const iconEl = screen.getByTestId("trust-badge-icon");
    expect(iconEl.getAttribute("role")).toBe("img");
  });

  it("does not have trailing spaces in className when no extra class provided", () => {
    render(<TrustBadge icon="🏠" stat="200+" label="Homes Sold" />);
    const badge = screen.getByTestId("trust-badge");
    expect(badge.className).not.toMatch(/\s$/);
  });
});
