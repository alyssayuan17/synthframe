import React, { useState } from 'react';

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

const getIconForType = (type) => {
    if (type.includes('header')) return <HeaderIcon />;
    if (type.includes('hero')) return <HeroIcon />;
    if (type.includes('feature') || type.includes('timeline')) return <FeatureIcon />;
    if (type.includes('footer') || type.includes('newsletter')) return <FooterIcon />;
    if (type.includes('frame')) return <FrameIcon />;
    return <HeaderIcon />;
};

const CanvasNode = ({ id, type, position, size, isFrame, onDelete, onMove, onResize }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [isResizing, setIsResizing] = useState(false);
    const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
    const [resizeStart, setResizeStart] = useState({ y: 0, height: 0 });

    const handleMouseDown = (e) => {
        if (e.target.closest('.delete-btn') || e.target.closest('.resize-handle')) return;
        setIsDragging(true);
        setDragOffset({
            x: e.clientX - position.x,
            y: e.clientY - position.y,
        });
    };

    const handleResizeMouseDown = (e) => {
        e.stopPropagation();
        setIsResizing(true);
        setResizeStart({
            y: e.clientY,
            height: size?.height || 400,
        });
    };

    const handleMouseMove = (e) => {
        if (isDragging && onMove) {
            onMove(id, {
                x: e.clientX - dragOffset.x,
                y: e.clientY - dragOffset.y,
            });
        } else if (isResizing && onResize) {
            const deltaY = e.clientY - resizeStart.y;
            const newHeight = Math.max(200, resizeStart.height + deltaY);
            onResize(id, { height: newHeight });
        }
    };

    const handleMouseUp = () => {
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
        ...(isFrame && size ? { width: `${size.width}px`, height: `${size.height}px` } : {}),
        transition: isDragging || isResizing ? 'none' : 'all 0.2s ease',
    };

    return (
        <div
            className={`canvas-node ${isDragging ? 'dragging' : ''} ${isFrame ? 'frame-node' : ''}`}
            style={nodeStyle}
            onMouseDown={handleMouseDown}
        >
            <div className="node-header">
                <span className="node-icon">{getIconForType(type)}</span>
                <span className="node-title">{type.replace(/-/g, ' ')}</span>
                <button className="delete-btn" onClick={() => onDelete(id)}>×</button>
            </div>

            {isFrame && (
                <div className="frame-content">
                    <div className="frame-screen"></div>
                </div>
            )}

            {!isFrame && (
                <div className="connection-points">
                    <div className="connection-point top"></div>
                    <div className="connection-point right"></div>
                    <div className="connection-point bottom"></div>
                    <div className="connection-point left"></div>
                </div>
            )}

            {isFrame && onResize && (
                <div className="resize-handle" onMouseDown={handleResizeMouseDown}>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="15 3 21 3 21 9" />
                        <polyline points="9 21 3 21 3 15" />
                        <line x1="21" y1="3" x2="14" y2="10" />
                        <line x1="3" y1="21" x2="10" y2="14" />
                    </svg>
                </div>
            )}
        </div>
    );
};

export default CanvasNode;
