/**
 * Component Type Mapping Utility
 *
 * This utility normalizes component types between:
 * - Frontend (kebab-case): navigation-bar, hero-banner, etc.
 * - Backend (UPPERCASE): NAVBAR, HERO, etc.
 *
 * The backend uses UPPERCASE for Gemini/CV pipeline consistency.
 * The frontend drag-and-drop uses kebab-case for readability.
 */

// Mapping from frontend kebab-case to backend UPPERCASE
export const FRONTEND_TO_BACKEND = {
    // Headers
    'navigation-bar': 'NAVBAR',
    'sticky-header': 'NAVBAR',
    'mega-menu': 'NAVBAR',
    'simple-header': 'NAVBAR',
    // Hero
    'hero-banner': 'HERO',
    'hero': 'HERO',
    'video-hero': 'HERO',
    'split-hero': 'HERO',
    'gradient-hero': 'HERO',
    // Features / Sections
    'feature-grid': 'SECTION',
    'section': 'SECTION',
    'content-section': 'SECTION',
    'icon-features': 'SECTION',
    'card-features': 'CARD',
    'card': 'CARD',
    'timeline': 'SECTION',
    // Interactive
    'form': 'FORM',
    'button': 'BUTTON',
    'input': 'INPUT',
    'text': 'TEXT',
    'heading': 'HEADING',
    // Media / Data
    'image': 'IMAGE',
    'table': 'TABLE',
    'calendar': 'CALENDAR',
    'chart': 'CHART',
    // Navigation / Layout
    'sidebar': 'SIDEBAR',
    'footer': 'FOOTER',
    'simple-footer': 'FOOTER',
    'multi-column': 'FOOTER',
    'social-footer': 'FOOTER',
    'newsletter': 'FOOTER',
    'bottom-nav': 'BOTTOM_NAV',
    // Frames
    'macbook-frame': 'FRAME',
    'iphone-frame': 'FRAME',
    'frame': 'FRAME',
};

// Mapping from backend UPPERCASE to display category
export const BACKEND_TO_CATEGORY = {
    'NAVBAR': 'header',
    'SIDEBAR': 'sidebar',
    'FOOTER': 'footer',
    'HEADING': 'text',
    'TEXT': 'text',
    'CARD': 'feature',
    'BUTTON': 'button',
    'FORM': 'form',
    'INPUT': 'input',
    'TABLE': 'table',
    'CHART': 'chart',
    'IMAGE': 'image',
    'HERO': 'hero',
    'SECTION': 'feature',
    'CALENDAR': 'calendar',
    'BOTTOM_NAV': 'footer',
    'FRAME': 'frame',
};

/**
 * Convert frontend kebab-case type to backend UPPERCASE type
 * @param {string} frontendType - e.g., 'navigation-bar'
 * @returns {string} - e.g., 'NAVBAR'
 */
export function toBackendType(frontendType) {
    return FRONTEND_TO_BACKEND[frontendType] || frontendType.toUpperCase().replace(/-/g, '_');
}

/**
 * Get icon category for a component type (works with both conventions)
 * @param {string} type - Either kebab-case or UPPERCASE
 * @returns {string} - Icon category: 'header', 'hero', 'feature', 'footer', 'frame'
 */
export function getIconCategory(type) {
    // First check if it's UPPERCASE (from backend)
    if (BACKEND_TO_CATEGORY[type]) {
        return BACKEND_TO_CATEGORY[type];
    }

    // Then check if it's kebab-case (from frontend drag-drop)
    const upperType = FRONTEND_TO_BACKEND[type];
    if (upperType && BACKEND_TO_CATEGORY[upperType]) {
        return BACKEND_TO_CATEGORY[upperType];
    }

    // Fallback: infer from type name
    const lowerType = type.toLowerCase();
    if (lowerType.includes('header') || lowerType.includes('nav') || lowerType.includes('menu')) {
        return 'header';
    }
    if (lowerType.includes('hero') || lowerType.includes('banner')) {
        return 'hero';
    }
    if (lowerType.includes('feature') || lowerType.includes('card') || lowerType.includes('section') || lowerType.includes('timeline')) {
        return 'feature';
    }
    if (lowerType.includes('footer') || lowerType.includes('newsletter') || lowerType.includes('bottom')) {
        return 'footer';
    }
    if (lowerType.includes('frame')) {
        return 'frame';
    }

    return 'default';
}

/**
 * Check if a type represents a frame component
 * @param {string} type - Either kebab-case or UPPERCASE
 * @returns {boolean}
 */
export function isFrameType(type) {
    const lowerType = type.toLowerCase();
    return lowerType.includes('frame') || type === 'FRAME';
}

/**
 * Get display label for a component type
 * @param {string} type - Either kebab-case or UPPERCASE
 * @returns {string} - Human-readable label
 */
export function getDisplayLabel(type) {
    // If it's kebab-case, convert to title case
    if (type.includes('-')) {
        return type
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
    // If it's UPPERCASE, convert to title case
    return type.charAt(0).toUpperCase() + type.slice(1).toLowerCase();
}

// All valid backend component types
export const BACKEND_COMPONENT_TYPES = [
    'NAVBAR',
    'HERO',
    'SECTION',
    'CARD',
    'FORM',
    'BUTTON',
    'TEXT',
    'IMAGE',
    'SIDEBAR',
    'FOOTER',
    'TABLE',
    'CALENDAR',
    'CHART',
    'INPUT',
    'HEADING',
    'BOTTOM_NAV',
    'FRAME',
];

export default {
    FRONTEND_TO_BACKEND,
    BACKEND_TO_CATEGORY,
    BACKEND_COMPONENT_TYPES,
    toBackendType,
    getIconCategory,
    isFrameType,
    getDisplayLabel,
};
