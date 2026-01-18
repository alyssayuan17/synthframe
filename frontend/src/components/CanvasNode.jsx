import { getIconCategory, getDisplayLabel } from '../utils/componentTypes';
import React, { useState, useRef } from 'react';
import { getComponentByType } from './ComponentRegistry';

// Icon components for canvas nodes
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

const SidebarIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <line x1="9" y1="3" x2="9" y2="21" />
    </svg>
);

const FormIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <line x1="7" y1="8" x2="17" y2="8" />
        <line x1="7" y1="12" x2="17" y2="12" />
        <line x1="7" y1="16" x2="12" y2="16" />
    </svg>
);

const TableIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <line x1="3" y1="9" x2="21" y2="9" />
        <line x1="3" y1="15" x2="21" y2="15" />
        <line x1="12" y1="3" x2="12" y2="21" />
    </svg>
);

const ChartIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <line x1="18" y1="20" x2="18" y2="10" />
        <line x1="12" y1="20" x2="12" y2="4" />
        <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
);

const ImageIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <circle cx="8.5" cy="8.5" r="1.5" />
        <polyline points="21 15 16 10 5 21" />
    </svg>
);

const ButtonIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="8" width="18" height="8" rx="2" ry="2" />
    </svg>
);

const TextIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <polyline points="4 7 4 4 20 4 20 7" />
        <line x1="9" y1="20" x2="15" y2="20" />
        <line x1="12" y1="4" x2="12" y2="20" />
    </svg>
);

const CalendarIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
        <line x1="16" y1="2" x2="16" y2="6" />
        <line x1="8" y1="2" x2="8" y2="6" />
        <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
);

// Map icon categories to components
const ICON_MAP = {
    header: <HeaderIcon />,
    hero: <HeroIcon />,
    feature: <FeatureIcon />,
    footer: <FooterIcon />,
    frame: <FrameIcon />,
    sidebar: <SidebarIcon />,
    form: <FormIcon />,
    input: <FormIcon />,
    table: <TableIcon />,
    chart: <ChartIcon />,
    image: <ImageIcon />,
    button: <ButtonIcon />,
    text: <TextIcon />,
    calendar: <CalendarIcon />,
    default: <HeaderIcon />,
};

const getIconForType = (type) => {
    const category = getIconCategory(type);
    return ICON_MAP[category] || ICON_MAP.default;
};

const CanvasNode = ({ id, type, position, size, props, isFrame, onDelete, onMove, onResize, onConnectStart, onConnectEnd, onDragEnd, isSelected, onSelect }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [isResizing, setIsResizing] = useState(false);
    const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
    const [resizeStart, setResizeStart] = useState({ x: 0, y: 0, width: 0, height: 0, direction: 'se' });
    const nodeRef = useRef(null);

    const handleMouseDown = (e) => {
        if (e.target.closest('.delete-btn') || e.target.closest('.resize-handle') || e.target.closest('.connection-point')) return;
        if (['INPUT', 'SELECT', 'TEXTAREA', 'BUTTON', 'LABEL', 'OPTION'].includes(e.target.tagName)) return;

        // Select this node when clicked
        if (onSelect) {
            onSelect(id);
        }

        setIsDragging(true);
        setDragOffset({
            x: e.clientX - position.x,
            y: e.clientY - position.y,
        });
    };

    const handleResizeMouseDown = (e, direction) => {
        e.stopPropagation();
        setIsResizing(true);
        const currentWidth = size?.width || (nodeRef.current ? nodeRef.current.offsetWidth : 200);
        const currentHeight = size?.height || (nodeRef.current ? nodeRef.current.offsetHeight : 100);

        setResizeStart({
            x: e.clientX,
            y: e.clientY,
            width: currentWidth,
            height: currentHeight,
            direction
        });
    };

    const handleConnectionStart = (e) => {
        e.stopPropagation();
        if (onConnectStart) {
            onConnectStart(id, { x: e.clientX, y: e.clientY });
        }
    };

    // We handle connection end by mouseUp on a target node/point
    const handleMouseUpOnNode = () => {
        if (onConnectEnd) {
            onConnectEnd(id);
        }
    };

    const handleMouseMove = (e) => {
        if (isDragging && onMove) {
            onMove(id, {
                x: e.clientX - dragOffset.x,
                y: e.clientY - dragOffset.y,
            });
        } else if (isResizing && onResize) {
            const deltaX = e.clientX - resizeStart.x;
            const deltaY = e.clientY - resizeStart.y;

            let newWidth = resizeStart.width;
            let newHeight = resizeStart.height;

            if (resizeStart.direction.includes('e')) {
                newWidth = Math.max(40, resizeStart.width + deltaX);
            }
            if (resizeStart.direction.includes('s')) {
                newHeight = Math.max(40, resizeStart.height + deltaY);
            }

            // Resize both width and height for everything
            onResize(id, {
                width: newWidth,
                height: newHeight
            });
        }
    };

    const handleMouseUp = () => {
        if (isDragging && onDragEnd) {
            onDragEnd(id);
        }
        setIsDragging(false);
        setIsResizing(false);
    };

    React.useEffect(() => {
        if (isDragging || isResizing) {
            window.addEventListener('mousemove', handleMouseMove);
            window.addEventListener('mouseup', handleMouseUp);
            return () => {
                window.removeEventListener('mousemove', handleMouseMove);
                window.removeEventListener('mouseup', handleMouseUp);
            };
        }
    }, [isDragging, isResizing, dragOffset, resizeStart]);

    const nodeStyle = {
        left: `${position.x}px`,
        top: `${position.y}px`,
        ...(size ? { width: `${size.width}px`, height: `${size.height}px` } : {}),
        transition: isDragging || isResizing ? 'none' : 'all 0.2s ease',
    };


    return (
        <div
            ref={nodeRef}
            className={`canvas-node-wrapper ${isDragging ? 'dragging' : ''} ${isFrame ? 'frame-node' : ''} ${isSelected ? 'selected' : ''}`}
            style={nodeStyle}
            onMouseUp={handleMouseUpOnNode}
        >
            <div className="node-header">
                <span className="node-icon">{getIconForType(type)}</span>
                <span className="node-title">{getDisplayLabel(type)}</span>
                <button className="delete-btn" onClick={() => onDelete(id)}>×</button>
            </div>
            {/* Floating title label */}
            <div className="node-label">
                <span className="node-label-text">{type.replace(/-/g, ' ')}</span>
                <button className="node-delete-btn" onClick={() => onDelete(id)}>×</button>
            </div>

            {/* Render actual interactive component */}
            {!isFrame && (() => {
                const Component = getComponentByType(type);
                return Component ? (
                    <div className="node-component p-2" onMouseDown={handleMouseDown} style={{ width: '100%', height: '100%', boxSizing: 'border-box' }}>
                        <Component {...(props || {})} />
                    </div>
                ) : null;
            })()}

            {isFrame && (
                <div className="frame-content" onMouseDown={handleMouseDown}>
                    <div className="frame-screen"></div>
                </div>
            )}

            {/* Connection Points - Visible for ALL components including frames */}
            <div className="connection-points">
                <div className="connection-point top" onMouseDown={handleConnectionStart}></div>
                <div className="connection-point right" onMouseDown={handleConnectionStart}></div>
                <div className="connection-point bottom" onMouseDown={handleConnectionStart}></div>
                <div className="connection-point left" onMouseDown={handleConnectionStart}></div>
            </div>

            {/* Resize Handles */}
            {onResize && (
                <>
                    <div className="resize-handle resize-handle-n" onMouseDown={(e) => handleResizeMouseDown(e, 'n')} />
                    <div className="resize-handle resize-handle-ne" onMouseDown={(e) => handleResizeMouseDown(e, 'ne')} />
                    <div className="resize-handle resize-handle-e" onMouseDown={(e) => handleResizeMouseDown(e, 'e')}>
                        <svg width="8" height="14" viewBox="0 0 8 14" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M5 2L7 7L5 12" />
                            <path d="M3 2L1 7L3 12" />
                        </svg>
                    </div>
                    <div className="resize-handle resize-handle-se" onMouseDown={(e) => handleResizeMouseDown(e, 'se')}>
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M15 3h6v6M14 10l7-7M9 21H3v-6M10 14l-7 7" />
                        </svg>
                    </div>
                    <div className="resize-handle resize-handle-s" onMouseDown={(e) => handleResizeMouseDown(e, 's')}>
                        <svg width="14" height="8" viewBox="0 0 14 8" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M2 5L7 7L12 5" />
                            <path d="M2 3L7 1L12 3" />
                        </svg>
                    </div>
                    <div className="resize-handle resize-handle-sw" onMouseDown={(e) => handleResizeMouseDown(e, 'sw')} />
                    <div className="resize-handle resize-handle-w" onMouseDown={(e) => handleResizeMouseDown(e, 'w')} />
                    <div className="resize-handle resize-handle-nw" onMouseDown={(e) => handleResizeMouseDown(e, 'nw')} />
                </>
            )}
        </div>
    );
};

export default CanvasNode;
