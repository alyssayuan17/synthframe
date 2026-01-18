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
    const [currentWireframeId, setCurrentWireframeId] = useState(null);

    // ===================================
    // CONNNECTION TO BACKEND (Athena AI)
    // ===================================
    React.useEffect(() => {
        const fetchLatestWireframe = async () => {
            try {
                // 1. Get list of wireframes
                const listRes = await fetch('http://localhost:8001/api/wireframes');
                const listData = await listRes.json();

                if (listData.wireframes && listData.wireframes.length > 0) {
                    // 2. Get the most recent one (last in the list likely, or just pick the last modified)
                    const latest = listData.wireframes[listData.wireframes.length - 1];

                    // Only fetch details if it's new or we haven't loaded one yet
                    // Note: In a real app, we'd check timestamps. Here we just re-fetch to catch updates (Flow 3)

                    const detailRes = await fetch(`http://localhost:8001/api/wireframes/${latest.id}`);
                    const detail = await detailRes.json();

                    if (detail && detail.components) {
                        // Update state if different (simple check)
                        setNodes(detail.components);
                        setCurrentWireframeId(latest.id);
                    }
                }
            } catch (err) {
                console.error("Error polling backend:", err);
            }
        };

        // Fetch only once on mount to restore state
        fetchLatestWireframe();

        // Polling removed to prevent conflict with local drag-and-drop state.
        // User edits (drag/resize) update local state.
        // AI updates trigger setNodes via onWireframeUpdate callback.
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

    // Sort nodes so frames render first (below other components)
    const sortedNodes = [...nodes].sort((a, b) => {
        if (a.isFrame && !b.isFrame) return -1;
        if (!a.isFrame && b.isFrame) return 1;
        return 0;
    });

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
                />
                <RightSidebar
                    currentWireframeId={currentWireframeId}
                    onWireframeUpdate={(components, wireframeId) => {
                        if (components) {
                            setNodes(components);
                            if (wireframeId) {
                                setCurrentWireframeId(wireframeId);
                            }
                        }
                    }}
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
