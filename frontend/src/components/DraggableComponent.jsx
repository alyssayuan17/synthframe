import React from 'react';

// Icon components
const HeaderIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <line x1="3" y1="9" x2="21" y2="9" />
    </svg>
);

const HeroIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
        <line x1="8" y1="21" x2="16" y2="21" />
        <line x1="12" y1="17" x2="12" y2="21" />
    </svg>
);

const FeatureIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
);

const FooterIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <line x1="3" y1="15" x2="21" y2="15" />
    </svg>
);

const FrameIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="2" y="3" width="20" height="18" rx="2" ry="2" />
        <circle cx="12" cy="19" r="1" />
    </svg>
);

const iconMap = {
    header: <HeaderIcon />,
    hero: <HeroIcon />,
    feature: <FeatureIcon />,
    footer: <FooterIcon />,
    frame: <FrameIcon />,
};

const DraggableComponent = ({ type, label, icon, onDragStart }) => {
    const handleDragStart = (e) => {
        e.dataTransfer.setData('componentType', type);
        e.dataTransfer.effectAllowed = 'copy';
        if (onDragStart) {
            onDragStart(type);
        }
    };

    return (
        <div
            className="draggable-component"
            draggable
            onDragStart={handleDragStart}
        >
            <span className="component-icon">{iconMap[icon] || iconMap.header}</span>
            <span className="component-label">{label}</span>
        </div>
    );
};

export default DraggableComponent;
