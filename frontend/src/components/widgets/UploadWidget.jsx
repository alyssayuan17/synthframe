/**
 * Upload Widget for Athena AI Chat
 * =================================
 *
 * This widget appears in the Athena chat to allow users to upload
 * hand-drawn sketches for analysis via CV pipeline.
 *
 * Features:
 * - Drag-and-drop file upload
 * - Click to browse files
 * - Camera capture (mobile: opens camera app, desktop: uses webcam)
 * - Image preview before sending
 *
 * Usage in Athena:
 * - Widget appears when user clicks the attachment icon
 * - User can upload existing image OR take a new photo
 * - Image is converted to base64 and sent to /api/analyze
 */

import React, { useState, useCallback, useRef } from 'react';

export default function UploadWidget({ onUpload, onClose }) {
    const [isDragging, setIsDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [preview, setPreview] = useState(null);
    const [showCamera, setShowCamera] = useState(false);
    const [cameraError, setCameraError] = useState(null);

    const videoRef = useRef(null);
    const streamRef = useRef(null);
    const canvasRef = useRef(null);

    const handleFile = useCallback(async (file) => {
        if (!file || !file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }

        setUploading(true);

        // Convert to base64
        const reader = new FileReader();
        reader.onload = async (e) => {
            const base64 = e.target.result;
            setPreview(base64);

            // Send to Athena (which calls MCP server)
            if (onUpload) {
                await onUpload(base64);
            }

            setUploading(false);
        };

        reader.readAsDataURL(file);
    }, [onUpload]);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files[0];
        handleFile(file);
    }, [handleFile]);

    const handleFileInput = useCallback((e) => {
        const file = e.target.files[0];
        handleFile(file);
    }, [handleFile]);

    // Start camera for desktop webcam capture
    const startCamera = async () => {
        setCameraError(null);
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' } // Prefer back camera on mobile
            });
            streamRef.current = stream;
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
            setShowCamera(true);
        } catch (err) {
            console.error('Camera access error:', err);
            setCameraError('Could not access camera. Please check permissions.');
        }
    };

    // Stop camera stream
    const stopCamera = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
            streamRef.current = null;
        }
        setShowCamera(false);
    };

    // Capture photo from video stream
    const capturePhoto = () => {
        if (!videoRef.current || !canvasRef.current) return;

        const video = videoRef.current;
        const canvas = canvasRef.current;

        // Set canvas size to video size
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Draw video frame to canvas
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        // Convert to base64
        const base64 = canvas.toDataURL('image/png');
        setPreview(base64);

        // Stop camera
        stopCamera();

        // Send to backend
        setUploading(true);
        if (onUpload) {
            onUpload(base64).then(() => setUploading(false));
        }
    };

    // Clean up camera on unmount
    React.useEffect(() => {
        return () => {
            if (streamRef.current) {
                streamRef.current.getTracks().forEach(track => track.stop());
            }
        };
    }, []);

    return (
        <div className="upload-widget" style={styles.container}>
            <div className="upload-header" style={styles.header}>
                <h3 style={styles.title}>
                    {showCamera ? 'Take a Photo' : 'Upload Your Sketch'}
                </h3>
                {onClose && (
                    <button onClick={() => { stopCamera(); onClose(); }} style={styles.closeButton}>
                        ×
                    </button>
                )}
            </div>

            {/* Camera View */}
            {showCamera ? (
                <div style={styles.cameraContainer}>
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        style={styles.video}
                    />
                    <div style={styles.cameraControls}>
                        <button onClick={stopCamera} style={styles.cancelButton}>
                            Cancel
                        </button>
                        <button onClick={capturePhoto} style={styles.captureButton}>
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <circle cx="12" cy="12" r="10" />
                            </svg>
                        </button>
                    </div>
                    <canvas ref={canvasRef} style={{ display: 'none' }} />
                </div>
            ) : (
                <>
                    {/* Upload Zone */}
                    <div
                        className={`upload-zone ${isDragging ? 'dragging' : ''}`}
                        style={{
                            ...styles.uploadZone,
                            ...(isDragging ? styles.uploadZoneDragging : {})
                        }}
                        onDragOver={(e) => {
                            e.preventDefault();
                            setIsDragging(true);
                        }}
                        onDragLeave={() => setIsDragging(false)}
                        onDrop={handleDrop}
                    >
                        {preview ? (
                            <div style={styles.previewContainer}>
                                <img src={preview} alt="Sketch preview" style={styles.preview} />
                                <button
                                    onClick={() => {
                                        setPreview(null);
                                        const fileInput = document.getElementById('file-input');
                                        if (fileInput) fileInput.value = '';
                                    }}
                                    style={styles.clearButton}
                                >
                                    Upload Different Sketch
                                </button>
                            </div>
                        ) : (
                            <>
                                <svg style={styles.uploadIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                                </svg>
                                <p style={styles.uploadText}>
                                    {uploading ? 'Processing...' : 'Drop your sketch here'}
                                </p>
                                <p style={styles.uploadSubtext}>or choose an option below</p>

                                <div style={styles.buttonRow}>
                                    {/* Browse Files Button */}
                                    <label style={styles.browseButton}>
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ marginRight: '6px' }}>
                                            <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
                                            <polyline points="13 2 13 9 20 9" />
                                        </svg>
                                        Browse Files
                                        <input
                                            id="file-input"
                                            type="file"
                                            accept="image/*"
                                            onChange={handleFileInput}
                                            style={styles.fileInput}
                                            disabled={uploading}
                                        />
                                    </label>

                                    {/* Take Photo Button - Mobile (uses capture attribute) */}
                                    <label style={styles.cameraButton}>
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ marginRight: '6px' }}>
                                            <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
                                            <circle cx="12" cy="13" r="4" />
                                        </svg>
                                        Take Photo
                                        <input
                                            type="file"
                                            accept="image/*"
                                            capture="environment"
                                            onChange={handleFileInput}
                                            style={styles.fileInput}
                                            disabled={uploading}
                                        />
                                    </label>
                                </div>

                                {/* Desktop Webcam Option */}
                                <button onClick={startCamera} style={styles.webcamLink}>
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ marginRight: '4px' }}>
                                        <polygon points="23 7 16 12 23 17 23 7" />
                                        <rect x="1" y="5" width="15" height="14" rx="2" ry="2" />
                                    </svg>
                                    Use Webcam
                                </button>

                                {cameraError && (
                                    <p style={styles.errorText}>{cameraError}</p>
                                )}
                            </>
                        )}
                    </div>

                    {/* Tips */}
                    {!preview && (
                        <div style={styles.tips}>
                            <p style={styles.tipTitle}>Tips for best results:</p>
                            <ul style={styles.tipList}>
                                <li>Draw clear boxes for UI components</li>
                                <li>Use dark pen on white paper</li>
                                <li>Ensure good lighting (no shadows)</li>
                                <li>Keep camera steady and focused</li>
                            </ul>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}

// Inline styles (for easy embedding in Athena)
const styles = {
    container: {
        width: '100%',
        maxWidth: '500px',
        padding: '20px',
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        boxShadow: '0 2px 12px rgba(0,0,0,0.1)',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    },
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '16px',
    },
    title: {
        margin: 0,
        fontSize: '18px',
        fontWeight: 600,
        color: '#1a1a1a',
    },
    closeButton: {
        background: 'none',
        border: 'none',
        fontSize: '24px',
        cursor: 'pointer',
        color: '#666',
        padding: 0,
        width: '28px',
        height: '28px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    uploadZone: {
        border: '2px dashed #d1d5db',
        borderRadius: '8px',
        padding: '40px 20px',
        textAlign: 'center',
        backgroundColor: '#f9fafb',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    uploadZoneDragging: {
        borderColor: '#3b82f6',
        backgroundColor: '#eff6ff',
    },
    uploadIcon: {
        width: '48px',
        height: '48px',
        margin: '0 auto 12px',
        color: '#9ca3af',
    },
    uploadText: {
        margin: '0 0 8px',
        fontSize: '16px',
        color: '#4b5563',
        fontWeight: 500,
    },
    uploadSubtext: {
        margin: '0 0 16px',
        fontSize: '14px',
        color: '#9ca3af',
    },
    buttonRow: {
        display: 'flex',
        gap: '12px',
        justifyContent: 'center',
        flexWrap: 'wrap',
    },
    browseButton: {
        display: 'inline-flex',
        alignItems: 'center',
        padding: '10px 20px',
        backgroundColor: '#3b82f6',
        color: '#ffffff',
        borderRadius: '6px',
        fontWeight: 500,
        cursor: 'pointer',
        transition: 'background-color 0.2s ease',
        fontSize: '14px',
    },
    cameraButton: {
        display: 'inline-flex',
        alignItems: 'center',
        padding: '10px 20px',
        backgroundColor: '#10b981',
        color: '#ffffff',
        borderRadius: '6px',
        fontWeight: 500,
        cursor: 'pointer',
        transition: 'background-color 0.2s ease',
        fontSize: '14px',
    },
    webcamLink: {
        display: 'inline-flex',
        alignItems: 'center',
        marginTop: '16px',
        padding: '8px 16px',
        backgroundColor: 'transparent',
        border: '1px solid #d1d5db',
        borderRadius: '6px',
        color: '#6b7280',
        fontSize: '13px',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    fileInput: {
        display: 'none',
    },
    previewContainer: {
        textAlign: 'center',
    },
    preview: {
        maxWidth: '100%',
        maxHeight: '300px',
        borderRadius: '8px',
        marginBottom: '16px',
    },
    clearButton: {
        padding: '8px 16px',
        backgroundColor: '#f3f4f6',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
        fontSize: '14px',
        color: '#374151',
        fontWeight: 500,
    },
    tips: {
        marginTop: '20px',
        padding: '16px',
        backgroundColor: '#f0f9ff',
        borderRadius: '8px',
        border: '1px solid #bfdbfe',
    },
    tipTitle: {
        margin: '0 0 8px',
        fontSize: '14px',
        fontWeight: 600,
        color: '#1e40af',
    },
    tipList: {
        margin: 0,
        paddingLeft: '20px',
        fontSize: '13px',
        color: '#1e40af',
        lineHeight: 1.6,
    },
    // Camera styles
    cameraContainer: {
        borderRadius: '8px',
        overflow: 'hidden',
        backgroundColor: '#000',
    },
    video: {
        width: '100%',
        display: 'block',
        borderRadius: '8px 8px 0 0',
    },
    cameraControls: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '20px',
        padding: '16px',
        backgroundColor: '#1a1a1a',
    },
    captureButton: {
        width: '64px',
        height: '64px',
        borderRadius: '50%',
        border: '4px solid #fff',
        backgroundColor: '#ef4444',
        color: '#fff',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transition: 'transform 0.1s ease',
    },
    cancelButton: {
        padding: '10px 20px',
        backgroundColor: 'transparent',
        border: '1px solid #fff',
        borderRadius: '6px',
        color: '#fff',
        fontSize: '14px',
        cursor: 'pointer',
    },
    errorText: {
        marginTop: '12px',
        fontSize: '13px',
        color: '#ef4444',
    },
};
