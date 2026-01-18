import React, { useState, useRef, useEffect } from 'react';
import UploadWidget from './widgets/UploadWidget';
import StatusWidget from './widgets/StatusWidget';

const RightSidebar = ({ currentWireframeId, onClearWireframe, onUploadSketch, hasNodes }) => {
    const [showUpload, setShowUpload] = useState(false);
    const [status, setStatus] = useState(null); // 'processing', 'success', 'error'
    const [statusData, setStatusData] = useState({});

    const handleUpload = async (base64Image) => {
        setShowUpload(false);
        setStatus('processing');
        if (onUploadSketch) {
            await onUploadSketch(base64Image);
        }
        // Status updates should ideally come from parent or shared state now
        // For now, we'll keep a local success state for the upload itself
        setStatus('success');
        setStatusData({ message: "Sketch uploaded! Athena is analyzing..." });
    };

    return (
        <div className="right-sidebar">
            <div className="sidebar-header">
                <div>
                    <h2>AI Workspace</h2>
                    <div className="status-indicator">
                        <span className="status-dot"></span>
                        <span className="status-text">Athena Online</span>
                    </div>
                </div>
                {hasNodes && (
                    <button className="clear-chip-btn" onClick={onClearWireframe} title="Start Fresh">
                        Clear Canvas
                    </button>
                )}
            </div>

            <div className="context-content">
                {/* Integration Note */}
                <div className="info-card highlight">
                    <p style={{ fontSize: '13px', margin: 0, color: '#1e40af' }}>
                        <strong>Active:</strong> {currentWireframeId || "No Project Loaded"}
                    </p>
                </div>

                {/* The "Main" Area - designed to be covered by or host the chat window */}
                <div id="athena-embedded-container" className="chat-host-area" style={{ flex: 1, minHeight: '300px', position: 'relative' }}>
                    {!showUpload && !status && !currentWireframeId && (
                        <div className="empty-chat-state">
                            <p>Ask Athena to generate a design to get started.</p>
                        </div>
                    )}

                    {/* Manual Sketch Upload always available as a quick action */}
                    <div className="actions-section" style={{ marginTop: '20px' }}>
                        <button className="upload-trigger-btn" onClick={() => setShowUpload(!showUpload)}>
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                                <polyline points="17 8 12 3 7 8" />
                                <line x1="12" y1="3" x2="12" y2="15" />
                            </svg>
                            Library / Sketch Upload
                        </button>
                    </div>

                    {showUpload && (
                        <div className="upload-container" style={{ marginTop: '12px' }}>
                            <UploadWidget onUpload={handleUpload} onClose={() => setShowUpload(false)} />
                        </div>
                    )}

                    {status && (
                        <div style={{ marginTop: '12px' }}>
                            <StatusWidget status={status} data={statusData} onOpenEditor={() => setStatus(null)} />
                        </div>
                    )}
                </div>

                {/* Helpful Tip Footer */}
                <div className="tip-box compact">
                    <p>Athena is now integrated! Say "Make a landing page" or "Upload a sketch" to begin.</p>
                </div>
            </div>
        </div>
    );
};

export default RightSidebar;
