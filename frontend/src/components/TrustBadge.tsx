import React from "react";

export interface TrustBadgeProps {
  /** Icon or emoji string displayed at the top of the badge */
  icon: string;
  /** Bold stat number, e.g. '200+', '5★' */
  stat: string;
  /** Descriptive label beneath the stat, e.g. 'Homes Sold' */
  label: string;
  /** Optional additional CSS classes for the outer container */
  className?: string;
}

const TrustBadge: React.FC<TrustBadgeProps> = ({
  icon,
  stat,
  label,
  className = "",
}) => {
  return (
    <div
      className={`flex flex-col items-center text-center gap-2 ${className}`.trim()}
      data-testid="trust-badge"
    >
      <span
        className="text-4xl leading-none"
        role="img"
        aria-label={label}
        data-testid="trust-badge-icon"
      >
        {icon}
      </span>
      <span
        className="text-2xl md:text-3xl font-bold font-playfair"
        style={{ color: "#C8A951" }}
        data-testid="trust-badge-stat"
      >
        {stat}
      </span>
      <span
        className="text-sm md:text-base font-medium text-slate-600 tracking-wide uppercase"
        data-testid="trust-badge-label"
      >
        {label}
      </span>
    </div>
  );
};

export default TrustBadge;
