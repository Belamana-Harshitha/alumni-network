/**
 * Main JavaScript file for Alumni Networking Portal
 * Provides enhanced interactivity and user experience
 */

// Global utility functions
const AlumniPortal = {
    
    // Initialize all components
    init: function() {
        this.setupFormValidation();
        this.setupTooltips();
        this.setupAutoTextareaResize();
        this.setupSearchFilters();
        this.setupModalHandling();
        this.setupNotifications();
        this.setupTableSorting();
        this.setupImageLazyLoading();
        console.log('Alumni Portal initialized');
    },

    // Form validation enhancements
    setupFormValidation: function() {
        const forms = document.querySelectorAll('form[novalidate], form:not([novalidate])');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Focus on first invalid field
                    const firstInvalid = form.querySelector(':invalid');
                    if (firstInvalid) {
                        firstInvalid.focus();
                        firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
                form.classList.add('was-validated');
            });

            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', function() {
                    if (this.checkValidity()) {
                        this.classList.remove('is-invalid');
                        this.classList.add('is-valid');
                    } else {
                        this.classList.remove('is-valid');
                        this.classList.add('is-invalid');
                    }
                });
            });
        });

        // Password confirmation validation
        const confirmPasswordFields = document.querySelectorAll('input[name="confirm_password"]');
        confirmPasswordFields.forEach(field => {
            const passwordField = document.querySelector('input[name="password"]');
            if (passwordField) {
                const validatePasswords = () => {
                    if (field.value !== passwordField.value) {
                        field.setCustomValidity('Passwords do not match');
                    } else {
                        field.setCustomValidity('');
                    }
                };
                
                field.addEventListener('input', validatePasswords);
                passwordField.addEventListener('input', validatePasswords);
            }
        });
    },

    // Setup Bootstrap tooltips
    setupTooltips: function() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    },

    // Auto-resize textareas
    setupAutoTextareaResize: function() {
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            // Initial resize
            this.autoResize(textarea);
            
            // Resize on input
            textarea.addEventListener('input', () => this.autoResize(textarea));
        });
    },

    autoResize: function(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    },

    // Enhanced search and filtering
    setupSearchFilters: function() {
        const searchForm = document.querySelector('.search-filters form');
        if (searchForm) {
            // Add loading state to search button
            searchForm.addEventListener('submit', function() {
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.classList.add('btn-loading');
                    submitBtn.disabled = true;
                }
            });

            // Clear filters functionality
            const clearBtn = searchForm.querySelector('.btn-outline-secondary');
            if (clearBtn && clearBtn.textContent.includes('Clear')) {
                clearBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    const inputs = searchForm.querySelectorAll('input, select');
                    inputs.forEach(input => {
                        if (input.type === 'text' || input.type === 'number') {
                            input.value = '';
                        } else if (input.tagName === 'SELECT') {
                            input.selectedIndex = 0;
                        }
                    });
                    searchForm.submit();
                });
            }
        }

        // Live search functionality for user search
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    // Could implement live search here
                    console.log('Search term:', this.value);
                }, 300);
            });
        }
    },

    // Modal handling enhancements
    setupModalHandling: function() {
        // Auto-focus first input in modals
        document.addEventListener('shown.bs.modal', function(e) {
            const firstInput = e.target.querySelector('input:not([type="hidden"]), textarea, select');
            if (firstInput) {
                firstInput.focus();
            }
        });

        // Reset forms when modals are closed
        document.addEventListener('hidden.bs.modal', function(e) {
            const form = e.target.querySelector('form');
            if (form) {
                form.reset();
                form.classList.remove('was-validated');
            }
        });
    },

    // Enhanced notifications/alerts
    setupNotifications: function() {
        // Auto-dismiss alerts after 5 seconds
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            if (!alert.querySelector('.btn-close')) {
                setTimeout(() => {
                    this.fadeOut(alert);
                }, 5000);
            }
        });

        // Smooth fade out for alerts
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-close')) {
                const alert = e.target.closest('.alert');
                if (alert) {
                    e.preventDefault();
                    AlumniPortal.fadeOut(alert);
                }
            }
        });
    },

    fadeOut: function(element) {
        element.style.transition = 'opacity 0.3s ease';
        element.style.opacity = '0';
        setTimeout(() => {
            element.remove();
        }, 300);
    },

    // Table sorting functionality
    setupTableSorting: function() {
        const tables = document.querySelectorAll('table.sortable');
        tables.forEach(table => {
            const headers = table.querySelectorAll('th[data-sort]');
            headers.forEach(header => {
                header.style.cursor = 'pointer';
                header.addEventListener('click', () => this.sortTable(table, header));
            });
        });
    },

    sortTable: function(table, header) {
        const columnIndex = Array.from(header.parentNode.children).indexOf(header);
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const sortOrder = header.dataset.sortOrder === 'asc' ? 'desc' : 'asc';

        rows.sort((a, b) => {
            const aText = a.children[columnIndex].textContent.trim();
            const bText = b.children[columnIndex].textContent.trim();
            
            // Try to compare as numbers first
            const aNum = parseFloat(aText);
            const bNum = parseFloat(bText);
            
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return sortOrder === 'asc' ? aNum - bNum : bNum - aNum;
            }
            
            // Compare as strings
            return sortOrder === 'asc' 
                ? aText.localeCompare(bText)
                : bText.localeCompare(aText);
        });

        // Update table
        rows.forEach(row => tbody.appendChild(row));
        
        // Update header indicators
        table.querySelectorAll('th').forEach(th => {
            th.classList.remove('sort-asc', 'sort-desc');
            delete th.dataset.sortOrder;
        });
        
        header.classList.add(`sort-${sortOrder}`);
        header.dataset.sortOrder = sortOrder;
    },

    // Lazy loading for images (future enhancement)
    setupImageLazyLoading: function() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    },

    // Utility functions
    showLoading: function(element) {
        if (element) {
            element.classList.add('btn-loading');
            element.disabled = true;
        }
    },

    hideLoading: function(element) {
        if (element) {
            element.classList.remove('btn-loading');
            element.disabled = false;
        }
    },

    // Format date for display
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // Debounce function for performance
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }
};

// Form submission helpers
function submitFormWithLoading(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    AlumniPortal.showLoading(submitBtn);
    
    // Re-enable after 5 seconds as fallback
    setTimeout(() => {
        AlumniPortal.hideLoading(submitBtn);
    }, 5000);
}

// Admin panel specific functionality
function setupAdminPanel() {
    // Confirmation dialogs for admin actions
    document.querySelectorAll('a[href*="toggle_status"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const action = this.textContent.trim().toLowerCase();
            if (!confirm(`Are you sure you want to ${action} this item?`)) {
                e.preventDefault();
            }
        });
    });

    // Admin stats refresh functionality
    const refreshStatsBtn = document.querySelector('#refresh-stats');
    if (refreshStatsBtn) {
        refreshStatsBtn.addEventListener('click', function() {
            location.reload();
        });
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    AlumniPortal.init();
    
    // Initialize admin panel if on admin page
    if (document.querySelector('.admin-dashboard') || window.location.pathname.includes('/admin')) {
        setupAdminPanel();
    }
    
    // Initialize feather icons after any dynamic content is loaded
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
});

// Handle page unload to show loading states
window.addEventListener('beforeunload', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
            AlumniPortal.showLoading(submitBtn);
        }
    });
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AlumniPortal;
}
