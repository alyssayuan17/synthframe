import React, { useState } from 'react';
import './SaveDialog.css';

const SaveDialog = ({ isOpen, onClose, onSave }) => {
    const [projectName, setProjectName] = useState('');

    if (!isOpen) return null;

    const handleSave = () => {
        if (projectName.trim()) {
            onSave(projectName.trim());
            setProjectName('');
            onClose();
        }
    };

    const handleCancel = () => {
        setProjectName('');
        onClose();
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && projectName.trim()) {
            handleSave();
        } else if (e.key === 'Escape') {
            handleCancel();
        }
    };

    return (
        <div className="save-overlay" onClick={handleCancel}>
            <div className="save-dialog" onClick={(e) => e.stopPropagation()}>
                <div className="save-header">
                    <h2 className="save-title">Save Project</h2>
                </div>

                <div className="save-content">
                    <label className="save-label" htmlFor="project-name">
                        Project Name
                    </label>
                    <input
                        id="project-name"
                        type="text"
                        className="save-input"
                        placeholder="Enter project name"
                        value={projectName}
                        onChange={(e) => setProjectName(e.target.value)}
                        onKeyDown={handleKeyPress}
                        autoFocus
                    />
                </div>

                <div className="save-actions">
                    <button className="save-btn-cancel" onClick={handleCancel}>
                        Cancel
                    </button>
                    <button 
                        className="save-btn-confirm" 
                        onClick={handleSave}
                        disabled={!projectName.trim()}
                    >
                        Save
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SaveDialog;
