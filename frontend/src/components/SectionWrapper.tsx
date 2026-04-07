import React from 'react';

export interface SectionWrapperProps {
  /** HTML id attribute used as a smooth-scroll navigation target */
  id: string;
  /** Section content */
  children: React.ReactNode;
  /** Optional additional CSS classes applied to the outer <section> element */
  className?: string;
  /** Background color preset */
  bgColor?: 'cream' | 'white' | 'slate';
}

const bgColorMap: Record<NonNullable<SectionWrapperProps['bgColor']>, string> = {
  cream: 'bg-[#FFFDF7]',
  white: 'bg-white',
  slate: 'bg-[#1E293B] text-white',
};

/**
 * SectionWrapper provides consistent vertical padding, a centered
 * max-width container, an optional background color, and an `id` for
 * smooth-scroll anchor targeting.
 *
 * Usage:
 * ```tsx
 * <SectionWrapper id="about" bgColor="cream">
 *   <h2>About</h2>
 * </SectionWrapper>
 * ```
 */
const SectionWrapper: React.FC<SectionWrapperProps> = ({
  id,
  children,
  className = '',
  bgColor = 'white',
}) => {
  const bgClass = bgColorMap[bgColor];

  return (
    <section
      id={id}
      className={`py-16 md:py-24 ${bgClass} ${className}`.trim()}
    >
      <div className="max-w-7xl mx-auto px-4">
        {children}
      </div>
    </section>
  );
};

export default SectionWrapper;
