/**
 * Status Widget for Athena AI Chat
 * =================================
 *
 * Shows processing status and results after MCP tools execute.
 *
 * States:
 * - Processing: Shows spinner and current step
 * - Success: Shows summary and link to editor
 * - Error: Shows error message
 */

import React from 'react';

export default function StatusWidget({ status, data, onOpenEditor }) {
    // status: 'processing' | 'success' | 'error'
    // data: { message, component_count, wireframe_id, error }

    if (status === 'processing') {
        return (
            <div style={styles.container}>
                <div style={styles.spinner}>
                    <div style={styles.spinnerCircle}></div>
                </div>
                <h3 style={styles.title}>Analyzing your sketch...</h3>
                <div style={styles.steps}>
                    <Step label="Running CV detection" completed />
                    <Step label="Mapping to components" active />
                    <Step label="Refining with AI" />
                </div>
            </div>
        );
    }

    if (status === 'success') {
        return (
            <div style={styles.container}>
                <div style={styles.successIcon}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" style={styles.icon}>
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                </div>
                <h3 style={styles.title}>Wireframe Generated!</h3>
                <div style={styles.stats}>
                    <div style={styles.statItem}>
                        <span style={styles.statValue}>{data.component_count || 0}</span>
                        <span style={styles.statLabel}>Components</span>
                    </div>
                    <div style={styles.statItem}>
                        <span style={styles.statValue}>Ready</span>
                        <span style={styles.statLabel}>Status</span>
                    </div>
                </div>
                {data.message && (
                    <p style={styles.message}>{data.message}</p>
                )}
                {onOpenEditor && (
                    <button
                        onClick={() => onOpenEditor(data.wireframe_id)}
                        style={styles.editorButton}
                    >
                        Open in Editor
                    </button>
                )}
            </div>
        );
    }

    if (status === 'error') {
        return (
            <div style={styles.container}>
                <div style={styles.errorIcon}>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" style={styles.icon}>
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </div>
                <h3 style={styles.title}>Something went wrong</h3>
                <p style={styles.errorMessage}>
                    {data?.error || 'Failed to process your request'}
                </p>
                <p style={styles.errorHelp}>
                    Try uploading a different image or describing your layout in text.
                </p>
            </div>
        );
    }

    return null;
}

function Step({ label, active, completed }) {
    return (
        <div style={styles.step}>
            <div style={{
                ...styles.stepIndicator,
                ...(completed ? styles.stepCompleted : {}),
                ...(active ? styles.stepActive : {})
            }}>
                {completed && '✓'}
            </div>
            <span style={{
                ...styles.stepLabel,
                ...(active ? styles.stepLabelActive : {})
            }}>
                {label}
            </span>
        </div>
    );
}

const styles = {
    container: {
        width: '100%',
        maxWidth: '400px',
        padding: '24px',
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        boxShadow: '0 2px 12px rgba(0,0,0,0.1)',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        textAlign: 'center',
    },
    spinner: {
        width: '48px',
        height: '48px',
        margin: '0 auto 16px',
    },
    spinnerCircle: {
        width: '100%',
        height: '100%',
        border: '4px solid #e5e7eb',
        borderTopColor: '#3b82f6',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
    },
    title: {
        margin: '0 0 20px',
        fontSize: '18px',
        fontWeight: 600,
        color: '#1a1a1a',
    },
    steps: {
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        alignItems: 'flex-start',
    },
    step: {
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
    },
    stepIndicator: {
        width: '24px',
        height: '24px',
        borderRadius: '50%',
        border: '2px solid #d1d5db',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '12px',
        color: '#ffffff',
        flexShrink: 0,
    },
    stepCompleted: {
        backgroundColor: '#10b981',
        borderColor: '#10b981',
    },
    stepActive: {
        borderColor: '#3b82f6',
        borderWidth: '3px',
    },
    stepLabel: {
        fontSize: '14px',
        color: '#6b7280',
    },
    stepLabelActive: {
        color: '#1a1a1a',
        fontWeight: 500,
    },
    successIcon: {
        width: '56px',
        height: '56px',
        margin: '0 auto 16px',
        backgroundColor: '#d1fae5',
        borderRadius: '50%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    errorIcon: {
        width: '56px',
        height: '56px',
        margin: '0 auto 16px',
        backgroundColor: '#fee2e2',
        borderRadius: '50%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    icon: {
        width: '32px',
        height: '32px',
        color: '#10b981',
    },
    stats: {
        display: 'flex',
        justifyContent: 'center',
        gap: '32px',
        marginBottom: '16px',
    },
    statItem: {
        display: 'flex',
        flexDirection: 'column',
        gap: '4px',
    },
    statValue: {
        fontSize: '24px',
        fontWeight: 700,
        color: '#1a1a1a',
    },
    statLabel: {
        fontSize: '12px',
        color: '#6b7280',
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
    },
    message: {
        margin: '0 0 20px',
        fontSize: '14px',
        color: '#4b5563',
    },
    editorButton: {
        width: '100%',
        padding: '12px 24px',
        backgroundColor: '#3b82f6',
        color: '#ffffff',
        border: 'none',
        borderRadius: '8px',
        fontSize: '15px',
        fontWeight: 600,
        cursor: 'pointer',
        transition: 'background-color 0.2s ease',
    },
    errorMessage: {
        margin: '0 0 12px',
        fontSize: '14px',
        color: '#ef4444',
    },
    errorHelp: {
        margin: 0,
        fontSize: '13px',
        color: '#6b7280',
    },
};

// Add CSS animation for spinner
if (typeof document !== 'undefined') {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}
