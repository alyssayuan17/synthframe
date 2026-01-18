/**
 * Frontend Integration Guide for MongoDB Persistence
 * ===================================================
 * 
 * This file shows exactly how to integrate MongoDB persistence
 * with your frontend widget/canvas.
 * 
 * FLOW:
 * 1. User generates wireframe → Save project_id
 * 2. User refreshes page → Load wireframe from project_id
 * 3. User edits wireframe → Update project in MongoDB
 * 4. User clicks "Save" → Manual save to MongoDB
 */

// =============================================================================
// CONFIGURATION
// =============================================================================

const API_BASE_URL = 'http://localhost:8000';

// =============================================================================
// 1. AFTER GENERATION - SAVE PROJECT ID
// =============================================================================

/**
 * Call this after generating a wireframe from text prompt
 */
async function handleGenerateFromText(userInput) {
  try {
    const response = await fetch(`${API_BASE_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_input: userInput,
        device_type: 'laptop', // or get from UI
        use_scraper: true // Optional: scrape web for design patterns
      })
    });

    const data = await response.json();

    if (data.success) {
      // NEW: Save the project ID
      const projectId = data.project_id;
      
      if (projectId) {
        // Save to localStorage (persists across page refreshes)
        localStorage.setItem('currentProjectId', projectId);
        
        // Optional: Add to URL for sharing
        const url = new URL(window.location);
        url.searchParams.set('project', projectId);
        window.history.pushState({}, '', url);
        
        console.log(`✅ Project saved with ID: ${projectId}`);
      }

      // Render the wireframe on your canvas
      renderWireframe(data.wireframe_layout);
      
      // Update project name input if you have one
      updateProjectNameUI(data.wireframe_layout.name);
      
      return {
        projectId: projectId,
        wireframe: data.wireframe_layout
      };
    } else {
      console.error('Generation failed:', data);
      return null;
    }
  } catch (error) {
    console.error('Error generating wireframe:', error);
    return null;
  }
}

/**
 * Call this after analyzing a sketch/mockup image
 */
async function handleAnalyzeSketch(imageBase64) {
  try {
    const response = await fetch(`${API_BASE_URL}/vision/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image_base64: imageBase64,
        name: 'My Sketch', // User can edit this later
        image_type: 'sketch',
        device_type: 'laptop'
      })
    });

    const data = await response.json();

    if (data.success) {
      // NEW: Save the project ID
      const projectId = data.project_id;
      
      if (projectId) {
        localStorage.setItem('currentProjectId', projectId);
        
        const url = new URL(window.location);
        url.searchParams.set('project', projectId);
        window.history.pushState({}, '', url);
        
        console.log(`✅ Sketch project saved with ID: ${projectId}`);
      }

      // Render the wireframe
      renderWireframe(data.wireframe);
      
      return {
        projectId: projectId,
        wireframe: data.wireframe
      };
    } else {
      console.error('Vision analysis failed:', data);
      return null;
    }
  } catch (error) {
    console.error('Error analyzing sketch:', error);
    return null;
  }
}

// =============================================================================
// 2. ON PAGE LOAD - RESTORE PROJECT
// =============================================================================

/**
 * Call this when the page loads or widget initializes
 */
async function restoreProject() {
  // Check URL first (for shared links like ?project=abc-123)
  const urlParams = new URLSearchParams(window.location.search);
  let projectId = urlParams.get('project');
  
  // Fallback to localStorage
  if (!projectId) {
    projectId = localStorage.getItem('currentProjectId');
  }
  
  if (!projectId) {
    console.log('No project to restore');
    return null;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        console.warn('Project not found, may have been deleted');
        localStorage.removeItem('currentProjectId');
        return null;
      }
      throw new Error(`HTTP ${response.status}`);
    }

    const project = await response.json();
    
    console.log(`✅ Restored project: ${project.name}`);
    
    // Render the wireframe on your canvas
    renderWireframe(project.wireframe);
    
    // Update UI with project metadata
    updateProjectNameUI(project.name);
    updateProjectMetadata({
      created: new Date(project.created_at),
      updated: new Date(project.updated_at),
      method: project.generation_method,
      device: project.device_type
    });
    
    return project;
    
  } catch (error) {
    console.error('Error restoring project:', error);
    return null;
  }
}

/**
 * Initialize on page load
 */
window.addEventListener('DOMContentLoaded', async () => {
  console.log('🔄 Checking for saved project...');
  const project = await restoreProject();
  
  if (project) {
    showNotification(`Restored: ${project.name}`);
  } else {
    showWelcomeScreen(); // Your UI for new users
  }
});

// =============================================================================
// 3. MANUAL SAVE - USER CLICKS "SAVE" BUTTON
// =============================================================================

/**
 * Call this when user clicks "Save" button (Option B)
 */
async function saveProject() {
  const projectId = localStorage.getItem('currentProjectId');
  
  if (!projectId) {
    showNotification('No project to save', 'error');
    return false;
  }

  try {
    // Get current wireframe state from your canvas
    const wireframe = getCurrentWireframeFromCanvas();
    
    // Get project name from input (if user edited it)
    const projectName = document.getElementById('projectNameInput')?.value;
    
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}/save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        wireframe: wireframe,
        name: projectName, // Optional
        instruction: 'User manually saved changes'
      })
    });

    const data = await response.json();

    if (response.ok) {
      console.log('✅ Project saved successfully');
      showNotification('Project saved!', 'success');
      
      // Update UI to show last saved time
      updateLastSavedTime(new Date());
      
      return true;
    } else {
      console.error('Save failed:', data);
      showNotification('Failed to save project', 'error');
      return false;
    }
    
  } catch (error) {
    console.error('Error saving project:', error);
    showNotification('Error saving project', 'error');
    return false;
  }
}

/**
 * Attach to save button
 */
document.getElementById('saveButton')?.addEventListener('click', saveProject);

/**
 * Optional: Auto-save every 30 seconds
 */
setInterval(async () => {
  const projectId = localStorage.getItem('currentProjectId');
  if (projectId && hasUnsavedChanges()) {
    console.log('💾 Auto-saving...');
    await saveProject();
  }
}, 30000); // 30 seconds

// =============================================================================
// 4. EDIT WITH NATURAL LANGUAGE
// =============================================================================

/**
 * Call this when user edits wireframe with instruction
 */
async function editWireframe(instruction) {
  const projectId = localStorage.getItem('currentProjectId');
  const currentWireframe = getCurrentWireframeFromCanvas();

  try {
    const response = await fetch(`${API_BASE_URL}/edit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        project_id: projectId, // Include to update MongoDB
        wireframe_layout: currentWireframe,
        instruction: instruction,
        use_scraper: false // Set true to search web for examples
      })
    });

    const data = await response.json();

    if (data.success) {
      console.log('✅ Wireframe edited');
      
      // Render the updated wireframe
      renderWireframe(data.wireframe_layout);
      
      // Show what changed
      showNotification(`Edited: ${instruction}`, 'success');
      
      return data.wireframe_layout;
    } else {
      console.error('Edit failed:', data);
      return null;
    }
    
  } catch (error) {
    console.error('Error editing wireframe:', error);
    return null;
  }
}

// =============================================================================
// 5. PROJECT NAME EDITING
// =============================================================================

/**
 * Call this when user changes project name
 */
async function renameProject(newName) {
  const projectId = localStorage.getItem('currentProjectId');
  
  if (!projectId) return false;

  try {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}/rename`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: newName
      })
    });

    if (response.ok) {
      console.log(`✅ Renamed to: ${newName}`);
      return true;
    }
    
    return false;
    
  } catch (error) {
    console.error('Error renaming project:', error);
    return false;
  }
}

/**
 * Attach to project name input
 */
document.getElementById('projectNameInput')?.addEventListener('blur', async (e) => {
  const newName = e.target.value.trim();
  if (newName) {
    await renameProject(newName);
  }
});

// =============================================================================
// 6. PROJECT GALLERY/LIST (OPTIONAL)
// =============================================================================

/**
 * Load and display all projects
 */
async function loadProjectGallery() {
  try {
    const response = await fetch(`${API_BASE_URL}/projects?limit=50&sort_by=updated_at&sort_order=-1`);
    const projects = await response.json();
    
    // Render project list
    const listContainer = document.getElementById('projectList');
    if (!listContainer) return;
    
    listContainer.innerHTML = projects.map(project => `
      <div class="project-item" data-project-id="${project._id}">
        <h3>${escapeHtml(project.name)}</h3>
        <p class="meta">
          ${project.component_count} components · 
          ${project.device_type} · 
          Updated ${formatDate(project.updated_at)}
        </p>
        <button onclick="loadProject('${project._id}')">Open</button>
        <button onclick="deleteProjectConfirm('${project._id}')">Delete</button>
      </div>
    `).join('');
    
    console.log(`📚 Loaded ${projects.length} projects`);
    
  } catch (error) {
    console.error('Error loading project gallery:', error);
  }
}

/**
 * Load a specific project
 */
async function loadProject(projectId) {
  localStorage.setItem('currentProjectId', projectId);
  
  // Update URL
  const url = new URL(window.location);
  url.searchParams.set('project', projectId);
  window.history.pushState({}, '', url);
  
  // Restore it
  await restoreProject();
  
  // Close gallery if open
  document.getElementById('projectGallery')?.classList.add('hidden');
}

// =============================================================================
// 7. DELETE PROJECT
// =============================================================================

/**
 * Delete a project
 */
async function deleteProject(projectId) {
  try {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      console.log(`🗑️ Deleted project: ${projectId}`);
      
      // If this was current project, clear it
      if (localStorage.getItem('currentProjectId') === projectId) {
        localStorage.removeItem('currentProjectId');
        clearCanvas();
      }
      
      // Refresh gallery if showing
      await loadProjectGallery();
      
      return true;
    }
    
    return false;
    
  } catch (error) {
    console.error('Error deleting project:', error);
    return false;
  }
}

function deleteProjectConfirm(projectId) {
  if (confirm('Are you sure you want to delete this project?')) {
    deleteProject(projectId);
  }
}

// =============================================================================
// 8. NEW PROJECT
// =============================================================================

/**
 * Start a new project (clears current state)
 */
function startNewProject() {
  if (hasUnsavedChanges()) {
    if (!confirm('You have unsaved changes. Start a new project anyway?')) {
      return;
    }
  }
  
  // Clear current project
  localStorage.removeItem('currentProjectId');
  
  // Clear URL parameter
  const url = new URL(window.location);
  url.searchParams.delete('project');
  window.history.pushState({}, '', url);
  
  // Clear canvas
  clearCanvas();
  
  // Show welcome/generate screen
  showWelcomeScreen();
  
  console.log('📄 Started new project');
}

// =============================================================================
// HELPER FUNCTIONS (IMPLEMENT BASED ON YOUR UI)
// =============================================================================

/**
 * Render wireframe on canvas
 * IMPLEMENT THIS based on your rendering logic
 */
function renderWireframe(wireframe) {
  console.log('Rendering wireframe with', wireframe.components.length, 'components');
  
  // YOUR CODE HERE:
  // - Clear canvas
  // - Loop through wireframe.components
  // - Create draggable elements for each component
  // - Position them based on component.position (x, y)
  // - Size them based on component.size (width, height)
  // - Style based on component.type (NAVBAR, HERO, BUTTON, etc.)
  
  // Example (pseudo-code):
  /*
  clearCanvas();
  
  wireframe.components.forEach(component => {
    const element = createComponentElement(component.type);
    element.style.left = component.position.x + 'px';
    element.style.top = component.position.y + 'px';
    element.style.width = component.size.width + 'px';
    element.style.height = component.size.height + 'px';
    element.dataset.componentId = component.id;
    
    // Add to canvas
    document.getElementById('canvas').appendChild(element);
    
    // Make draggable
    makeDraggable(element);
  });
  */
}

/**
 * Get current wireframe state from canvas
 * IMPLEMENT THIS based on your canvas structure
 */
function getCurrentWireframeFromCanvas() {
  // YOUR CODE HERE:
  // - Get all component elements from canvas
  // - Extract position, size, props for each
  // - Return WireframeLayout object
  
  // Example (pseudo-code):
  /*
  const components = Array.from(document.querySelectorAll('.component')).map(el => ({
    id: el.dataset.componentId,
    type: el.dataset.componentType,
    position: {
      x: parseInt(el.style.left),
      y: parseInt(el.style.top)
    },
    size: {
      width: parseInt(el.style.width),
      height: parseInt(el.style.height)
    },
    props: JSON.parse(el.dataset.props || '{}'),
    source: 'user'
  }));
  
  return {
    id: localStorage.getItem('wireframeId') || generateId(),
    name: document.getElementById('projectNameInput')?.value || 'Untitled',
    canvas_size: {
      width: 1440,
      height: 900
    },
    source_type: 'edit',
    components: components
  };
  */
  
  return {}; // Replace with actual implementation
}

/**
 * Update project name in UI
 */
function updateProjectNameUI(name) {
  const input = document.getElementById('projectNameInput');
  if (input) {
    input.value = name;
  }
}

/**
 * Update project metadata display
 */
function updateProjectMetadata(metadata) {
  // Display created date, last updated, etc.
  console.log('Project metadata:', metadata);
}

/**
 * Show notification to user
 */
function showNotification(message, type = 'info') {
  console.log(`[${type.toUpperCase()}] ${message}`);
  // Implement your notification UI here
}

/**
 * Check if there are unsaved changes
 */
function hasUnsavedChanges() {
  // Implement based on your state management
  return false;
}

/**
 * Update last saved time display
 */
function updateLastSavedTime(date) {
  const el = document.getElementById('lastSaved');
  if (el) {
    el.textContent = `Last saved: ${formatDate(date)}`;
  }
}

/**
 * Clear the canvas
 */
function clearCanvas() {
  // Implement based on your canvas structure
  console.log('Clearing canvas');
}

/**
 * Show welcome screen for new users
 */
function showWelcomeScreen() {
  console.log('Showing welcome screen');
  // Implement your welcome UI
}

/**
 * Format date for display
 */
function formatDate(date) {
  return new Date(date).toLocaleString();
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// =============================================================================
// EXPORT FOR USE IN YOUR APP
// =============================================================================

// If using modules:
/*
export {
  handleGenerateFromText,
  handleAnalyzeSketch,
  restoreProject,
  saveProject,
  editWireframe,
  renameProject,
  loadProjectGallery,
  deleteProject,
  startNewProject
};
*/
