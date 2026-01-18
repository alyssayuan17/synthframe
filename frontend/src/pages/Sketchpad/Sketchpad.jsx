import React, { useState } from 'react';
import TopNavigation from '../../components/TopNavigation';
import LeftSidebar from '../../components/LeftSidebar';
import InfiniteCanvas from '../../components/InfiniteCanvas';
import RightSidebar from '../../components/RightSidebar';
import './Sketchpad.css';

const Sketchpad = () => {
    const [nodes, setNodes] = useState([]);
    const [leftCollapsed, setLeftCollapsed] = useState(false);
    const [rightCollapsed, setRightCollapsed] = useState(false);
    const [selectedNodeId, setSelectedNodeId] = useState(null);

    const getDefaultSize = (type) => {
        if (type === 'macbook-frame') {
            return { width: 600, height: 400 };
        } else if (type === 'iphone-frame') {
            return { width: 300, height: 600 };
        }
        return null;
    };

    const isFrameType = (type) => {
        return type.includes('frame');
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
            // Check if we are dropped inside any frame
            const nodeRect = {
                x: position.x,
                y: position.y,
                width: 200, // Approximate width
                height: 100, // Approximate height
            };

            // We need to access current nodes state. Since setNodes uses callback,
            // we can't access 'prev' here easily without a second setNodes or just using 'nodes' state which might be stale?
            // Actually 'nodes' from the render scope is fine for the INITIAL add.
            const targetFrame = nodes.find(
                (n) => n.isFrame && isInsideFrame(nodeRect, { ...n.position, ...n.size })
            );

            if (targetFrame) {
                newNode.parentId = targetFrame.id;
                // Store relative position to the frame
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
        if (selectedNodeId === id) {
            setSelectedNodeId(null);
        }
    };



    const handleMoveNode = (id, newPosition) => {
        setNodes((prev) => {
            const movingNode = prev.find((n) => n.id === id);
            if (!movingNode) return prev;

            // Calculate delta for moving children
            const delta = {
                x: newPosition.x - movingNode.position.x,
                y: newPosition.y - movingNode.position.y,
            };

            return prev.map((node) => {
                // Case 1: Moving the node itself (frame or child)
                if (node.id === id) {
                    const updatedNode = { ...node, position: newPosition };

                    // If this is a child being moved, update its relative position to its parent
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

                // Case 2: If we're moving a frame, move all its children with it
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

    const handleNodeDragStop = (id) => {
        setNodes((prev) => {
            const movedNode = prev.find((n) => n.id === id);
            if (!movedNode) return prev;

            // Case 1: Moved a Frame -> Capture components inside it
            if (movedNode.isFrame) {
                const frameRect = {
                    x: movedNode.position.x,
                    y: movedNode.position.y,
                    width: movedNode.size?.width || 200,
                    height: movedNode.size?.height || 100,
                };

                return prev.map(n => {
                    if (n.id === id || n.isFrame) return n; // Skip self/frames

                    const nodeRect = {
                        x: n.position.x,
                        y: n.position.y,
                        width: n.size?.width || 200,
                        height: n.size?.height || 100
                    };

                    if (isInsideFrame(nodeRect, frameRect)) {
                        return {
                            ...n,
                            parentId: id,
                            relativePosition: {
                                x: n.position.x - frameRect.x,
                                y: n.position.y - frameRect.y
                            }
                        };
                    }
                    // Note: We don't detach existing children here because dragging the frame moves them, 
                    // so they stay inside. Only detach if the CHILD is moved out (Case 2).
                    return n;
                });
            }

            // Case 2: Moved a Component -> Check if dropped on a Frame
            const nodeRect = {
                x: movedNode.position.x,
                y: movedNode.position.y,
                width: movedNode.size?.width || 200,
                height: movedNode.size?.height || 100,
            };

            const targetFrame = prev.find(
                (n) => n.isFrame && n.id !== id && isInsideFrame(nodeRect, { ...n.position, ...n.size })
            );

            if (targetFrame) {
                const relativePosition = {
                    x: movedNode.position.x - targetFrame.position.x,
                    y: movedNode.position.y - targetFrame.position.y,
                };

                return prev.map((n) =>
                    n.id === id
                        ? { ...n, parentId: targetFrame.id, relativePosition }
                        : n
                );
            } else {
                if (movedNode.parentId) {
                    return prev.map((n) =>
                        n.id === id ? { ...n, parentId: null, relativePosition: null } : n
                    );
                }
            }
            return prev;
        });
    };

    // Sort nodes so frames render first (below other components)
    const sortedNodes = [...nodes].sort((a, b) => {
        if (a.isFrame && !b.isFrame) return -1;
        if (!a.isFrame && b.isFrame) return 1;
        return 0;
    });

    // Handle keyboard events for deleting selected node
    React.useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.key === 'Delete' || e.key === 'Backspace') && selectedNodeId) {
                // Prevent default backspace navigation
                e.preventDefault();
                handleDeleteNode(selectedNodeId);
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [selectedNodeId]);

    const [connections, setConnections] = useState([]);

    const handleAddConnection = (sourceId, targetId) => {
        if (connections.some(c => c.sourceId === sourceId && c.targetId === targetId)) return;
        setConnections(prev => [...prev, {
            id: Date.now(),
            sourceId,
            targetId
        }]);
    };

    const getContentClassName = () => {
        if (leftCollapsed && rightCollapsed) return 'sketchpad-content both-collapsed';
        if (leftCollapsed) return 'sketchpad-content left-collapsed';
        if (rightCollapsed) return 'sketchpad-content right-collapsed';
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
                    connections={connections}
                    onAddConnection={handleAddConnection}
                    onNodeDragStop={handleNodeDragStop}
                    selectedNodeId={selectedNodeId}
                    onSelectNode={setSelectedNodeId}
                />
                <RightSidebar />
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

            {/* Right Toggle Bar */}
            <button
                className={`side-toggle-bar right-toggle ${rightCollapsed ? 'collapsed' : ''}`}
                onClick={() => setRightCollapsed(!rightCollapsed)}
                title={rightCollapsed ? "Show AI Assistant" : "Hide AI Assistant"}
            >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    {rightCollapsed ? (
                        <polyline points="15 18 9 12 15 6" />
                    ) : (
                        <polyline points="9 18 15 12 9 6" />
                    )}
                </svg>
            </button>
        </div>
    );
};

export default Sketchpad;