import React, { useState, useRef } from 'react';
import CanvasNode from './CanvasNode';

const InfiniteCanvas = ({ nodes, onAddNode, onDeleteNode, onMoveNode, onResizeNode, connections = [], onAddConnection, onNodeDragStop, selectedNodeId, onSelectNode }) => {
    const [pan, setPan] = useState({ x: 0, y: 0 });
    const [zoom, setZoom] = useState(1);
    const [isPanning, setIsPanning] = useState(false);
    const [panStart, setPanStart] = useState({ x: 0, y: 0 });
    const [isDraggingComponent, setIsDraggingComponent] = useState(false);
    const canvasRef = useRef(null);
    const [drawingConnection, setDrawingConnection] = useState(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        setIsDraggingComponent(true);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDraggingComponent(false);
        const componentType = e.dataTransfer.getData('componentType');
        if (componentType) {
            const rect = canvasRef.current.getBoundingClientRect();
            const x = (e.clientX - rect.left - pan.x) / zoom;
            const y = (e.clientY - rect.top - pan.y) / zoom;
            onAddNode(componentType, { x, y });
        }
    };

    const handleDragLeave = (e) => {
        if (e.target === canvasRef.current) {
            setIsDraggingComponent(false);
        }
    };

    const handleMouseDown = (e) => {
        // Don't start panning if we're dragging a component or clicking on a node
        if (isDraggingComponent || e.target.closest('.canvas-node') || e.target.closest('.canvas-node-wrapper')) {
            return;
        }

        if (e.target === canvasRef.current || e.target.closest('.canvas-content')) {
            // Deselect any selected node when clicking on canvas background
            if (onSelectNode) {
                onSelectNode(null);
            }
            setIsPanning(true);
            setPanStart({
                x: e.clientX - pan.x,
                y: e.clientY - pan.y,
            });
        }
    };



    const handleWheel = (e) => {
        e.preventDefault();
        const delta = e.deltaY > 0 ? -0.1 : 0.1;
        setZoom((prevZoom) => Math.min(Math.max(prevZoom + delta, 0.5), 2));
    };

    // Add wheel event listener with passive: false to allow preventDefault()
    React.useEffect(() => {
        const canvas = canvasRef.current;
        if (canvas) {
            canvas.addEventListener('wheel', handleWheel, { passive: false });
            return () => {
                canvas.removeEventListener('wheel', handleWheel);
            };
        }
    }, [zoom]);

    const handleZoomIn = () => {
        setZoom((prevZoom) => Math.min(prevZoom + 0.1, 2));
    };

    const handleZoomOut = () => {
        setZoom((prevZoom) => Math.max(prevZoom - 0.1, 0.5));
    };

    const getLocalCoordinates = (clientX, clientY) => {
        if (!canvasRef.current) return { x: 0, y: 0 };
        const rect = canvasRef.current.getBoundingClientRect();
        return {
            x: (clientX - rect.left - pan.x) / zoom,
            y: (clientY - rect.top - pan.y) / zoom,
        };
    };

    const handleMouseMove = (e) => {
        if (isPanning) {
            setPan({
                x: e.clientX - panStart.x,
                y: e.clientY - panStart.y,
            });
        }
        if (drawingConnection) {
            const localPos = getLocalCoordinates(e.clientX, e.clientY);
            setDrawingConnection(prev => ({
                ...prev,
                currentX: localPos.x,
                currentY: localPos.y
            }));
        }
    };

    const handleMouseUp = () => {
        setIsPanning(false);
        if (drawingConnection) {
            setDrawingConnection(null);
        }
    };

    React.useEffect(() => {
        if (isPanning || drawingConnection) {
            window.addEventListener('mousemove', handleMouseMove);
            window.addEventListener('mouseup', handleMouseUp);
            return () => {
                window.removeEventListener('mousemove', handleMouseMove);
                window.removeEventListener('mouseup', handleMouseUp);
            };
        }
    }, [isPanning, panStart, drawingConnection]);

    const handleConnectStart = (nodeId, clientPos) => {
        const localPos = getLocalCoordinates(clientPos.x, clientPos.y);
        setDrawingConnection({
            sourceId: nodeId,
            currentX: localPos.x,
            currentY: localPos.y,
        });
    };

    const handleConnectEnd = (targetNodeId) => {
        if (drawingConnection && drawingConnection.sourceId !== targetNodeId) {
            onAddConnection(drawingConnection.sourceId, targetNodeId);
        }
        setDrawingConnection(null);
    };




    // Calculate center point for a node
    const getNodeCenter = (node) => {
        const width = node.size?.width || 200;
        const height = node.size?.height || 100; // Approximate height for non-frames
        return {
            x: node.position.x + width / 2,
            y: node.position.y + height / 2,
        };
    };

    const getCurvedPath = (x1, y1, x2, y2) => {
        const dx = x2 - x1;
        const dy = y2 - y1;
        const distance = Math.sqrt(dx * dx + dy * dy);

        // Control point offset (creates the curve)
        const offset = distance * 0.3;

        // Calculate control points for a smooth curve
        const cx1 = x1 + offset;
        const cy1 = y1;
        const cx2 = x2 - offset;
        const cy2 = y2;

        return `M ${x1} ${y1} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${x2} ${y2}`;
    };

    const renderConnections = () => {
        return (
            <svg
                className="connections-layer"
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    pointerEvents: 'none',
                    overflow: 'visible',
                    zIndex: 0
                }}
            >
                {/* Existing Connections */}
                {connections.map((conn) => {
                    const sourceNode = nodes.find(n => n.id === conn.sourceId);
                    const targetNode = nodes.find(n => n.id === conn.targetId);
                    if (!sourceNode || !targetNode) return null;

                    const start = getNodeCenter(sourceNode);
                    const end = getNodeCenter(targetNode);
                    const pathData = getCurvedPath(start.x, start.y, end.x, end.y);

                    return (
                        <path
                            key={conn.id}
                            d={pathData}
                            stroke="black"
                            strokeWidth="2"
                            fill="none"
                        />
                    );
                })}

                {/* Drawing Connection Line */}
                {drawingConnection && (() => {
                    const sourceNode = nodes.find(n => n.id === drawingConnection.sourceId);
                    if (!sourceNode) return null;
                    const start = getNodeCenter(sourceNode);
                    const pathData = getCurvedPath(
                        start.x,
                        start.y,
                        drawingConnection.currentX,
                        drawingConnection.currentY
                    );

                    return (
                        <path
                            d={pathData}
                            stroke="black"
                            strokeWidth="2"
                            strokeDasharray="5,5"
                            fill="none"
                        />
                    );
                })()}
            </svg>
        );
    };

    return (
        <div className="infinite-canvas-container">
            <div
                ref={canvasRef}
                className="infinite-canvas"
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onDragLeave={handleDragLeave}
                onMouseDown={handleMouseDown}
                style={{
                    backgroundImage: 'radial-gradient(circle, #cbd5e1 1px, transparent 1px)',
                    backgroundSize: `${20 * zoom}px ${20 * zoom}px`,
                    backgroundPosition: `${pan.x}px ${pan.y}px`,
                }}
            >
                <div
                    className="canvas-content"
                    style={{
                        transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
                        width: '100%',
                        height: '100%',
                        transformOrigin: '0 0',
                    }}
                >
                    {renderConnections()}

                    {nodes.length === 0 && (
                        <div className="ghost-text">Drag and Drop Components Here</div>
                    )}
                    {nodes.map((node) => (
                        <CanvasNode
                            key={node.id}
                            id={node.id}
                            type={node.type}
                            position={node.position}
                            size={node.size}
                            isFrame={node.isFrame}
                            onDelete={onDeleteNode}
                            onMove={onMoveNode}
                            onResize={onResizeNode}
                            onConnectStart={handleConnectStart}
                            onConnectEnd={handleConnectEnd}
                            onDragEnd={onNodeDragStop}
                            isSelected={selectedNodeId === node.id}
                            onSelect={onSelectNode}
                        />
                    ))}
                </div>
            </div>

            <div className="zoom-controls">
                <button className="zoom-btn" onClick={handleZoomOut} title="Zoom Out">−</button>
                <span className="zoom-level">{Math.round(zoom * 100)}%</span>
                <button className="zoom-btn" onClick={handleZoomIn} title="Zoom In">+</button>
            </div>
        </div>
    );
};

export default InfiniteCanvas;
