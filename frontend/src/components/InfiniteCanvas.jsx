import React, { useState, useRef } from 'react';
import CanvasNode from './CanvasNode';

const InfiniteCanvas = ({ nodes, onAddNode, onDeleteNode, onMoveNode, onResizeNode }) => {
    const [pan, setPan] = useState({ x: 0, y: 0 });
    const [zoom, setZoom] = useState(1);
    const [isPanning, setIsPanning] = useState(false);
    const [panStart, setPanStart] = useState({ x: 0, y: 0 });
    const [isDraggingComponent, setIsDraggingComponent] = useState(false);
    const canvasRef = useRef(null);

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
        if (isDraggingComponent || e.target.closest('.canvas-node')) {
            return;
        }

        if (e.target === canvasRef.current || e.target.closest('.canvas-content')) {
            setIsPanning(true);
            setPanStart({
                x: e.clientX - pan.x,
                y: e.clientY - pan.y,
            });
        }
    };

    const handleMouseMove = (e) => {
        if (isPanning) {
            setPan({
                x: e.clientX - panStart.x,
                y: e.clientY - panStart.y,
            });
        }
    };

    const handleMouseUp = () => {
        setIsPanning(false);
    };

    // Fix passive event listener error for wheel event
    React.useEffect(() => {
        const element = canvasRef.current;
        if (!element) return;

        const handleWheelEvent = (e) => {
            e.preventDefault();
            const delta = e.deltaY > 0 ? -0.1 : 0.1;
            setZoom((prevZoom) => Math.min(Math.max(prevZoom + delta, 0.5), 2));
        };

        element.addEventListener('wheel', handleWheelEvent, { passive: false });
        return () => element.removeEventListener('wheel', handleWheelEvent);
    }, []);

    const handleZoomIn = () => {
        setZoom((prevZoom) => Math.min(prevZoom + 0.1, 2));
    };

    const handleZoomOut = () => {
        setZoom((prevZoom) => Math.max(prevZoom - 0.1, 0.5));
    };

    React.useEffect(() => {
        if (isPanning) {
            window.addEventListener('mousemove', handleMouseMove);
            window.addEventListener('mouseup', handleMouseUp);
            return () => {
                window.removeEventListener('mousemove', handleMouseMove);
                window.removeEventListener('mouseup', handleMouseUp);
            };
        }
    }, [isPanning, panStart]);

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
