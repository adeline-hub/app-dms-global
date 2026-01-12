// Add drag and drop styling
document.addEventListener('DOMContentLoaded', function() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        area.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragging');
        });
        
        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragging');
        });
        
        area.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragging');
        });
    });
});