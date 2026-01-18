import React from 'react';
import { Link } from 'react-router-dom';
import './ProjectGallery.css';

const ProjectGallery = () => {
    // Mock project data - will be replaced with actual saved projects
    const projects = [
        { id: 1, name: 'E-commerce Landing', date: '2026-01-15', thumbnail: null },
        { id: 2, name: 'Dashboard UI', date: '2026-01-14', thumbnail: null },
        { id: 3, name: 'Mobile App Design', date: '2026-01-12', thumbnail: null },
        { id: 4, name: 'Portfolio Website', date: '2026-01-10', thumbnail: null },
    ];

    return (
        <div className="gallery-page">
            <nav className="gallery-nav">
                <div className="nav-container">
                    <Link to="/" className="gallery-brand">
                        <img src="/synthframe logo.svg" alt="SynthFrame Logo" className="brand-logo" />
                        <span>SynthFrame</span>
                    </Link>
                    <div className="nav-actions">
                        <Link to="/sketchpad" className="nav-link">
                            Back to Sketchpad
                        </Link>
                    </div>
                </div>
            </nav>

            <main className="gallery-main">
                <div className="gallery-header">
                    <h1 className="gallery-title">Project Gallery</h1>
                    <Link to="/sketchpad" className="new-project-btn">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <line x1="12" y1="5" x2="12" y2="19" />
                            <line x1="5" y1="12" x2="19" y2="12" />
                        </svg>
                        New Project
                    </Link>
                </div>

                <div className="gallery-content">
                    {projects.length === 0 ? (
                        <div className="gallery-empty">
                            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                                <rect x="3" y="3" width="7" height="7" />
                                <rect x="14" y="3" width="7" height="7" />
                                <rect x="14" y="14" width="7" height="7" />
                                <rect x="3" y="14" width="7" height="7" />
                            </svg>
                            <p className="empty-text">No saved projects yet</p>
                            <p className="empty-subtext">Start creating and save your first project</p>
                            <Link to="/sketchpad" className="start-creating-btn">
                                Start Creating
                            </Link>
                        </div>
                    ) : (
                        <div className="projects-grid">
                            {projects.map((project) => (
                                <div key={project.id} className="project-card">
                                    <div className="project-thumbnail">
                                        {project.thumbnail ? (
                                            <img src={project.thumbnail} alt={project.name} />
                                        ) : (
                                            <div className="thumbnail-placeholder">
                                                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                    <rect x="3" y="3" width="18" height="18" rx="2" />
                                                    <path d="M9 3v18" />
                                                </svg>
                                            </div>
                                        )}
                                    </div>
                                    <div className="project-info">
                                        <h3 className="project-name">{project.name}</h3>
                                        <p className="project-date">{new Date(project.date).toLocaleDateString()}</p>
                                    </div>
                                    <div className="project-actions">
                                        <Link to="/sketchpad" className="action-btn" title="Open Project">
                                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
                                                <polyline points="15 3 21 3 21 9" />
                                                <line x1="10" y1="14" x2="21" y2="3" />
                                            </svg>
                                        </Link>
                                        <button className="action-btn delete-btn" title="Delete Project">
                                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                <polyline points="3 6 5 6 21 6" />
                                                <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
};

export default ProjectGallery;
