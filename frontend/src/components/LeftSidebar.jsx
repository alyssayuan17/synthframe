import React, { useState } from 'react';
import DraggableComponent from './DraggableComponent';

const LeftSidebar = () => {
    const [activeTab, setActiveTab] = useState('headers');

    const componentCategories = {
        frames: [
            { type: 'macbook-frame', label: 'MacBook Frame', icon: 'frame' },
            { type: 'iphone-frame', label: 'iPhone Frame', icon: 'frame' },
        ],
        headers: [
            { type: 'navigation-bar', label: 'Navigation Bar', icon: 'header' },
            { type: 'sticky-header', label: 'Sticky Header', icon: 'header' },
            { type: 'mega-menu', label: 'Mega Menu', icon: 'header' },
            { type: 'simple-header', label: 'Simple Header', icon: 'header' },
        ],
        hero: [
            { type: 'hero-banner', label: 'Hero Banner', icon: 'hero' },
            { type: 'video-hero', label: 'Video Hero', icon: 'hero' },
            { type: 'split-hero', label: 'Split Hero', icon: 'hero' },
            { type: 'gradient-hero', label: 'Gradient Hero', icon: 'hero' },
        ],
        features: [
            { type: 'feature-grid', label: 'Feature Grid', icon: 'feature' },
            { type: 'icon-features', label: 'Icon Features', icon: 'feature' },
            { type: 'card-features', label: 'Card Features', icon: 'feature' },
            { type: 'timeline', label: 'Timeline', icon: 'feature' },
        ],
        footers: [
            { type: 'simple-footer', label: 'Simple Footer', icon: 'footer' },
            { type: 'multi-column', label: 'Multi-Column', icon: 'footer' },
            { type: 'social-footer', label: 'Social Footer', icon: 'footer' },
            { type: 'newsletter', label: 'Newsletter', icon: 'footer' },
        ],
    };

    const TabIcon = ({ type }) => {
        const icons = {
            frames: (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="2" y="3" width="20" height="18" rx="2" ry="2" />
                    <circle cx="12" cy="19" r="1" />
                </svg>
            ),
            headers: (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                    <line x1="3" y1="9" x2="21" y2="9" />
                </svg>
            ),
            hero: (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                    <line x1="8" y1="21" x2="16" y2="21" />
                    <line x1="12" y1="17" x2="12" y2="21" />
                </svg>
            ),
            features: (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                </svg>
            ),
            footers: (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                    <line x1="3" y1="15" x2="21" y2="15" />
                </svg>
            ),
        };
        return icons[type] || null;
    };

    const tabs = [
        { id: 'frames', label: 'Frames' },
        { id: 'headers', label: 'Headers' },
        { id: 'hero', label: 'Hero Sections' },
        { id: 'features', label: 'Features' },
        { id: 'footers', label: 'Footers' },
    ];

    return (
        <div className="left-sidebar">
            <div className="sidebar-header">
                <h2>Components</h2>
            </div>

            <div className="tabs">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        className={`tab ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        <TabIcon type={tab.id} />
                        <span>{tab.label}</span>
                    </button>
                ))}
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
    );
};

export default LeftSidebar;
