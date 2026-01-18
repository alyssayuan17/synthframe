import React, { useState } from 'react';
import TopNavigation from '../../components/TopNavigation';
import LeftSidebar from '../../components/LeftSidebar';
import InfiniteCanvas from '../../components/InfiniteCanvas';
import { isFrameType as checkIsFrame } from '../../utils/componentTypes';
import './Sketchpad.css';

const Sketchpad = () => {
    const [nodes, setNodes] = useState([]);
    const [leftCollapsed, setLeftCollapsed] = useState(false);

    // Athena AI widget handles chat - loaded via script in index.html
    // Canvas updates will come from Athena via window events (see useEffect below)

    // Listen for wireframe updates from Athena AI
    React.useEffect(() => {
        const handleAthenaUpdate = (event) => {
            if (event.detail && event.detail.components) {
                setNodes(event.detail.components);
            }
        };

        window.addEventListener('athena-wireframe-update', handleAthenaUpdate);
        return () => window.removeEventListener('athena-wireframe-update', handleAthenaUpdate);
    }, []);

    // Expose setNodes to window for Athena to call directly if needed
    React.useEffect(() => {
        window.synthframeUpdateCanvas = (components) => {
            if (components && Array.isArray(components)) {
                setNodes(components);
            }
        };
        return () => { delete window.synthframeUpdateCanvas; };
    }, []);

    const getDefaultSize = (type) => {
        if (type === 'macbook-frame') {
            return { width: 600, height: 400 };
        } else if (type === 'iphone-frame') {
            return { width: 300, height: 600 };
        }
        return null;
    };

    const isFrameType = (type) => {
        return checkIsFrame(type);
    };

    const isInsideFrame = (nodeRect, frameRect) => {
        return (
            nodeRect.x >= frameRect.x &&
            nodeRect.x + nodeRect.width <= frameRect.x + frameRect.width &&
            nodeRect.y >= frameRect.y &&
            nodeRect.y + nodeRect.height <= frameRect.y + frameRect.height
        );
    };

    const handleAddNode = (type, position) => {
        const isFrame = isFrameType(type);
        const newNode = {
            id: Date.now(),
            type,
            position,
            isFrame,
            size: getDefaultSize(type),
            parentId: null,
            relativePosition: null,
        };

        if (!isFrame) {
            const nodeRect = {
                x: position.x,
                y: position.y,
                width: 200,
                height: 100,
            };

            const targetFrame = nodes.find(
                (n) => n.isFrame && isInsideFrame(nodeRect, { ...n.position, ...n.size })
            );

            if (targetFrame) {
                newNode.parentId = targetFrame.id;
                newNode.relativePosition = {
                    x: position.x - targetFrame.position.x,
                    y: position.y - targetFrame.position.y,
                };
            }
        }

        setNodes((prev) => [...prev, newNode]);
    };

    const handleDeleteNode = (id) => {
        setNodes((prev) => prev.filter((node) => node.id !== id));
    };

    const handleMoveNode = (id, newPosition) => {
        setNodes((prev) => {
            const movingNode = prev.find((n) => n.id === id);
            if (!movingNode) return prev;

            return prev.map((node) => {
                if (node.id === id) {
                    const updatedNode = { ...node, position: newPosition };

                    if (node.parentId) {
                        const parentFrame = prev.find((n) => n.id === node.parentId);
                        if (parentFrame) {
                            updatedNode.relativePosition = {
                                x: newPosition.x - parentFrame.position.x,
                                y: newPosition.y - parentFrame.position.y,
                            };
                        }
                    }

                    return updatedNode;
                }

                if (node.parentId === id && node.relativePosition) {
                    return {
                        ...node,
                        position: {
                            x: newPosition.x + node.relativePosition.x,
                            y: newPosition.y + node.relativePosition.y,
                        },
                    };
                }

                return node;
            });
        });
    };

    const handleResizeNode = (id, newSize) => {
        setNodes((prev) =>
            prev.map((node) =>
                node.id === id ? { ...node, size: { ...node.size, ...newSize } } : node
            )
        );
    };

    const sortedNodes = [...nodes].sort((a, b) => {
        if (a.isFrame && !b.isFrame) return -1;
        if (!a.isFrame && b.isFrame) return 1;
        return 0;
    });

    const getContentClassName = () => {
        if (leftCollapsed) return 'sketchpad-content left-collapsed';
        return 'sketchpad-content';
    };

    return (
        <div className="sketchpad">
            <TopNavigation />
            <div className={getContentClassName()}>
                <LeftSidebar />
                <InfiniteCanvas
                    nodes={sortedNodes}
                    onAddNode={handleAddNode}
                    onDeleteNode={handleDeleteNode}
                    onMoveNode={handleMoveNode}
                    onResizeNode={handleResizeNode}
                />
            </div>

            {/* Left Toggle Bar */}
            <button
                className={`side-toggle-bar left-toggle ${leftCollapsed ? 'collapsed' : ''}`}
                onClick={() => setLeftCollapsed(!leftCollapsed)}
                title={leftCollapsed ? "Show Components" : "Hide Components"}
            >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    {leftCollapsed ? (
                        <polyline points="9 18 15 12 9 6" />
                    ) : (
                        <polyline points="15 18 9 12 15 6" />
                    )}
                </svg>
            </button>
        </div>
    );
};

export default Sketchpad;
