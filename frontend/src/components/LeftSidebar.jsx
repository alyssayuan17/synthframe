import React, { useState } from 'react';
import DraggableComponent from './DraggableComponent';

const LeftSidebar = () => {
    const [activeTab, setActiveTab] = useState('navigation');

    const componentCategories = {
        frames: [
            { type: 'macbook-frame', label: 'MacBook Frame', icon: 'frame' },
            { type: 'iphone-frame', label: 'iPhone Frame', icon: 'frame' },
        ],
        navigation: [
            { type: 'navbar', label: 'Navbar', icon: 'header' },
            { type: 'navbar-dropdown', label: 'Navbar with Dropdown', icon: 'header' },
            { type: 'breadcrumbs', label: 'Breadcrumbs', icon: 'header' },
            { type: 'tabs', label: 'Tabs', icon: 'header' },
        ],
        buttons: [
            { type: 'button-primary', label: 'Primary Button', icon: 'header' },
            { type: 'button-secondary', label: 'Secondary Button', icon: 'header' },
            { type: 'button-accent', label: 'Accent Button', icon: 'header' },
            { type: 'button-group', label: 'Button Group', icon: 'header' },
            { type: 'button-outline', label: 'Outline Button', icon: 'header' },
        ],
        cards: [
            { type: 'card-basic', label: 'Basic Card', icon: 'feature' },
            { type: 'card-image', label: 'Card with Image', icon: 'feature' },
            { type: 'card-compact', label: 'Compact Card', icon: 'feature' },
        ],
        forms: [
            { type: 'input-text', label: 'Text Input', icon: 'feature' },
            { type: 'input-label', label: 'Input with Label', icon: 'feature' },
            { type: 'textarea', label: 'Textarea', icon: 'feature' },
            { type: 'select', label: 'Select', icon: 'feature' },
            { type: 'checkbox', label: 'Checkbox', icon: 'feature' },
            { type: 'radio', label: 'Radio Group', icon: 'feature' },
            { type: 'range', label: 'Range Slider', icon: 'feature' },
            { type: 'toggle', label: 'Toggle Switch', icon: 'feature' },
        ],
        display: [
            { type: 'alert-info', label: 'Alert Info', icon: 'feature' },
            { type: 'alert-success', label: 'Alert Success', icon: 'feature' },
            { type: 'badge', label: 'Badge', icon: 'feature' },
            { type: 'badge-group', label: 'Badge Group', icon: 'feature' },
            { type: 'progress', label: 'Progress Bar', icon: 'feature' },
            { type: 'radial-progress', label: 'Radial Progress', icon: 'feature' },
            { type: 'stats', label: 'Stats', icon: 'feature' },
            { type: 'calendar', label: 'Calendar', icon: 'feature' },
        ],
        hero: [
            { type: 'hero-basic', label: 'Basic Hero', icon: 'hero' },
            { type: 'hero-image', label: 'Hero with Image', icon: 'hero' },
            { type: 'pricing', label: 'Pricing Section', icon: 'hero' },
        ],
        modal: [
            { type: 'modal', label: 'Modal', icon: 'feature' },
            { type: 'drawer', label: 'Drawer', icon: 'feature' },
            { type: 'dropdown', label: 'Dropdown', icon: 'header' },
            { type: 'dropdown-hover', label: 'Dropdown (Hover)', icon: 'header' },
        ],
        footers: [
            { type: 'footer-basic', label: 'Basic Footer', icon: 'footer' },
            { type: 'footer-centered', label: 'Centered Footer', icon: 'footer' },
        ],
    };

    const TabIcon = ({ type }) => {
        const icons = {
            frames: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="2" y="3" width="20" height="18" rx="2" ry="2" />
                    <circle cx="12" cy="19" r="1" />
                </svg>
            ),
            navigation: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                    <line x1="3" y1="9" x2="21" y2="9" />
                </svg>
            ),
            buttons: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="8" width="18" height="8" rx="2" ry="2" />
                </svg>
            ),
            cards: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                    <line x1="3" y1="10" x2="21" y2="10" />
                </svg>
            ),
            forms: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
            ),
            display: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                </svg>
            ),
            hero: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                    <line x1="8" y1="21" x2="16" y2="21" />
                    <line x1="12" y1="17" x2="12" y2="21" />
                </svg>
            ),
            modal: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
            ),
            footers: (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                    <line x1="3" y1="15" x2="21" y2="15" />
                </svg>
            ),
        };
        return icons[type] || null;
    };

    const tabs = [
        { id: 'frames', label: 'Frames' },
        { id: 'navigation', label: 'Navigation' },
        { id: 'buttons', label: 'Buttons' },
        { id: 'cards', label: 'Cards' },
        { id: 'forms', label: 'Forms' },
        { id: 'display', label: 'Display' },
        { id: 'hero', label: 'Hero' },
        { id: 'modal', label: 'Modal' },
        { id: 'footers', label: 'Footers' },
    ];

    return (
        <div className="left-sidebar">
            <div className="sidebar-nav">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        className={`tab-icon-btn ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        <TabIcon type={tab.id} />
                        <span className="tab-tooltip">{tab.label}</span>
                    </button>
                ))}
            </div>

            <div className="sidebar-content-area">
                <div className="sidebar-header">
                    <h2>Components</h2>
                </div>

                <div className="component-list">
                    {componentCategories[activeTab].map((component) => (
                        <DraggableComponent
                            key={component.type}
                            type={component.type}
                            label={component.label}
                            icon={component.icon}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default LeftSidebar;
