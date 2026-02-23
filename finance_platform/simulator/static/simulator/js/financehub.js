/**
 * FinanceHub Pro — Main JavaScript
 * Tema, sidebar, modal, toast, CountUp animasyonları
 */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSidebar();
    initUserDropdown();
    initModals();
    initCountUp();
});

/* ======== THEME ======== */
function initTheme() {
    const toggle = document.getElementById('themeToggle');
    if (!toggle) return;

    toggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('fh-theme', next);
        updateThemeIcon(next);
    });
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
}

/* ======== SIDEBAR ======== */
function initSidebar() {
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (!toggle || !sidebar) return;

    toggle.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            sidebar.classList.toggle('mobile-open');
            overlay?.classList.toggle('show');
        } else {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('fh-sidebar', sidebar.classList.contains('collapsed') ? 'collapsed' : 'expanded');
        }
    });

    overlay?.addEventListener('click', () => {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('show');
    });

    // Restore sidebar state
    if (window.innerWidth > 768 && localStorage.getItem('fh-sidebar') === 'collapsed') {
        sidebar.classList.add('collapsed');
    }
}

/* ======== USER DROPDOWN ======== */
function initUserDropdown() {
    const avatarBtn = document.getElementById('userAvatar');
    const menu = document.getElementById('userDropdownMenu');
    if (!avatarBtn || !menu) return;

    avatarBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        menu.classList.toggle('show');
    });

    document.addEventListener('click', () => {
        menu.classList.remove('show');
    });
}

/* ======== MODALS ======== */
function initModals() {
    // Open modal buttons
    document.querySelectorAll('[data-modal]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = document.getElementById(btn.dataset.modal);
            if (modal) modal.classList.add('show');
        });
    });

    // Close modal buttons
    document.querySelectorAll('[data-modal-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.closest('.fh-modal-overlay').classList.remove('show');
        });
    });

    // Close on overlay click
    document.querySelectorAll('.fh-modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) overlay.classList.remove('show');
        });
    });
}

function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.add('show');
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove('show');
}

/* ======== COUNT UP ======== */
function initCountUp() {
    document.querySelectorAll('[data-countup]').forEach(el => {
        const target = parseFloat(el.dataset.countup);
        const prefix = el.dataset.prefix || '';
        const suffix = el.dataset.suffix || '';
        const decimals = parseInt(el.dataset.decimals) || 0;
        const duration = parseInt(el.dataset.duration) || 1500;

        animateValue(el, 0, target, duration, decimals, prefix, suffix);
    });
}

function animateValue(el, start, end, duration, decimals, prefix, suffix) {
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = start + (end - start) * eased;

        el.textContent = prefix + formatNumber(current, decimals) + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function formatNumber(num, decimals) {
    return num.toLocaleString('tr-TR', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
    });
}

/* ======== TOAST ======== */
function showToast(message, type = 'success') {
    let container = document.querySelector('.fh-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'fh-toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `fh-toast ${type}`;
    const iconMap = { success: 'bi-check-circle-fill', error: 'bi-exclamation-circle-fill', info: 'bi-info-circle-fill' };
    toast.innerHTML = `<i class="bi ${iconMap[type] || iconMap.info}"></i><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => toast.remove(), 3000);
}

/* ======== FORM FIELD TOGGLE (Transaction) ======== */
function initTransactionForm(formId, billCategoryIds) {
    const form = document.getElementById(formId);
    if (!form) return;

    const typeSelect = form.querySelector('#id_type');
    const categorySelect = form.querySelector('#id_category');
    const dueDateField = form.querySelector('#dueDateField') || form.querySelector('[data-field="due_date"]');
    const isPaidField = form.querySelector('#isPaidField') || form.querySelector('[data-field="is_paid"]');
    const categoryField = form.querySelector('#categoryField') || form.querySelector('[data-field="category"]');
    const recurringField = form.querySelector('#recurringField') || form.querySelector('[data-field="recurring"]');

    if (!typeSelect) return;

    function toggleFields() {
        const isExpense = typeSelect.value === 'expense';

        if (categoryField) categoryField.style.display = isExpense ? '' : 'none';
        if (!isExpense && categorySelect) categorySelect.value = '';

        const catId = categorySelect ? parseInt(categorySelect.value) : 0;
        const isBill = catId && billCategoryIds.includes(catId);

        if (dueDateField) dueDateField.style.display = isBill ? '' : 'none';
        if (isPaidField) isPaidField.style.display = isBill ? '' : 'none';
    }

    typeSelect.addEventListener('change', toggleFields);
    if (categorySelect) categorySelect.addEventListener('change', toggleFields);
    toggleFields();
}
