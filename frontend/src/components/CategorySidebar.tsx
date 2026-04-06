import React, { useState, useCallback } from "react";

/**
 * Represents a single node in the category taxonomy tree.
 */
export interface CategoryNode {
  /** Unique identifier for the category. */
  id: number;
  /** Display name of the category. */
  name: string;
  /** URL-friendly slug used for routing. */
  slug: string;
  /** Nested child categories. */
  children?: CategoryNode[];
}

/**
 * Props for the CategorySidebar component.
 */
export interface CategorySidebarProps {
  /** The full category tree structure to render. */
  categories: CategoryNode[];
  /** Slug of the currently active/selected category, if any. */
  activeCategorySlug?: string;
  /** Callback invoked when a category is selected. Receives the slug. */
  onSelect: (slug: string) => void;
  /** Optional title displayed at the top of the sidebar. */
  title?: string;
  /** Optional CSS class name applied to the root element. */
  className?: string;
}

interface CategoryItemProps {
  node: CategoryNode;
  activeCategorySlug?: string;
  onSelect: (slug: string) => void;
  depth: number;
  expandedSlugs: Set<string>;
  toggleExpanded: (slug: string) => void;
}

/**
 * Recursive component that renders a single category tree node
 * with optional expand/collapse for children.
 */
function CategoryItem({
  node,
  activeCategorySlug,
  onSelect,
  depth,
  expandedSlugs,
  toggleExpanded,
}: CategoryItemProps): React.ReactElement {
  const hasChildren = node.children != null && node.children.length > 0;
  const isExpanded = expandedSlugs.has(node.slug);
  const isActive = activeCategorySlug === node.slug;

  const handleToggle = (e: React.MouseEvent | React.KeyboardEvent) => {
    e.stopPropagation();
    toggleExpanded(node.slug);
  };

  const handleSelect = (e: React.MouseEvent) => {
    e.preventDefault();
    onSelect(node.slug);
  };

  return (
    <li data-testid={`category-item-${node.slug}`}>
      <div
        className="category-sidebar__row"
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
      >
        {hasChildren ? (
          <button
            type="button"
            className="category-sidebar__toggle"
            onClick={handleToggle}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") handleToggle(e);
            }}
            aria-expanded={isExpanded}
            aria-label={`Toggle ${node.name}`}
            data-testid={`toggle-${node.slug}`}
          >
            <span
              className="category-sidebar__chevron"
              style={{
                display: "inline-block",
                transform: isExpanded ? "rotate(90deg)" : "rotate(0deg)",
                transition: "transform 0.15s ease",
              }}
            >
              ▶
            </span>
          </button>
        ) : (
          <span
            className="category-sidebar__toggle-placeholder"
            style={{ display: "inline-block", width: "20px" }}
          />
        )}

        <a
          href={`/categories/${node.slug}`}
          className={`category-sidebar__link${
            isActive ? " category-sidebar__link--active" : ""
          }`}
          onClick={handleSelect}
          aria-current={isActive ? "page" : undefined}
          data-testid={`link-${node.slug}`}
        >
          {node.name}
        </a>
      </div>

      {hasChildren && isExpanded && (
        <ul className="category-sidebar__children" role="group">
          {node.children!.map((child) => (
            <CategoryItem
              key={child.id}
              node={child}
              activeCategorySlug={activeCategorySlug}
              onSelect={onSelect}
              depth={depth + 1}
              expandedSlugs={expandedSlugs}
              toggleExpanded={toggleExpanded}
            />
          ))}
        </ul>
      )}
    </li>
  );
}

/**
 * Collects all ancestor slugs for a given target slug so the tree
 * can auto-expand to show the active category.
 */
function collectAncestorSlugs(
  nodes: CategoryNode[],
  targetSlug: string,
  path: string[] = [],
): string[] | null {
  for (const node of nodes) {
    if (node.slug === targetSlug) return path;
    if (node.children && node.children.length > 0) {
      const result = collectAncestorSlugs(
        node.children,
        targetSlug,
        [...path, node.slug],
      );
      if (result) return result;
    }
  }
  return null;
}

/**
 * CategorySidebar displays a taxonomy tree as a collapsible sidebar navigation.
 *
 * Each category renders as a link to `/categories/:slug`. Parent categories
 * with children show a toggle button to expand/collapse their subtree.
 * The active category is visually highlighted and its ancestor path is
 * automatically expanded on mount.
 */
export default function CategorySidebar({
  categories,
  activeCategorySlug,
  onSelect,
  title,
  className,
}: CategorySidebarProps): React.ReactElement {
  const [expandedSlugs, setExpandedSlugs] = useState<Set<string>>(() => {
    const initial = new Set<string>();
    if (activeCategorySlug) {
      const ancestors = collectAncestorSlugs(categories, activeCategorySlug);
      if (ancestors) {
        ancestors.forEach((s) => initial.add(s));
      }
    }
    return initial;
  });

  const toggleExpanded = useCallback((slug: string) => {
    setExpandedSlugs((prev) => {
      const next = new Set(prev);
      if (next.has(slug)) {
        next.delete(slug);
      } else {
        next.add(slug);
      }
      return next;
    });
  }, []);

  return (
    <nav
      className={`category-sidebar${className ? " " + className : ""}`}
      aria-label={title || "Category navigation"}
      data-testid="category-sidebar"
    >
      {title && (
        <h2 className="category-sidebar__title" data-testid="sidebar-title">
          {title}
        </h2>
      )}
      <ul className="category-sidebar__list" role="tree">
        {categories.map((cat) => (
          <CategoryItem
            key={cat.id}
            node={cat}
            activeCategorySlug={activeCategorySlug}
            onSelect={onSelect}
            depth={0}
            expandedSlugs={expandedSlugs}
            toggleExpanded={toggleExpanded}
          />
        ))}
      </ul>
    </nav>
  );
}
