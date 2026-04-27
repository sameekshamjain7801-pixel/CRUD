document.addEventListener('DOMContentLoaded', () => {
    const userForm = document.getElementById('user-form');
    const userTableBody = document.getElementById('user-table-body');
    const formTitle = document.getElementById('form-title');
    const submitBtn = document.getElementById('submit-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const userIdInput = document.getElementById('user-id');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const phnoInput = document.getElementById('phno');
    const toast = document.getElementById('toast');

    // Fetch and display users
    const fetchUsers = async () => {
        try {
            const response = await fetch('/users');
            const users = await response.json();
            
            userTableBody.innerHTML = '';
            users.forEach(user => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${user.name}</td>
                    <td>${user.email}</td>
                    <td>${user.phno || ''}</td>
                    <td class="actions">
                        <button class="btn-edit" onclick="editUser('${user.id}', '${user.name}', '${user.email}', '${user.phno || ''}')">Edit</button>
                        <button class="btn-delete" onclick="deleteUser('${user.id}')">Delete</button>
                    </td>
                `;
                userTableBody.appendChild(tr);
            });
        } catch (error) {
            showToast('Error fetching users', 'error');
        }
    };

    // Show toast message
    const showToast = (message, type = 'success') => {
        toast.textContent = message;
        toast.style.background = type === 'success' ? '#6366f1' : '#ef4444';
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 3000);
    };

    // Handle form submit (Create/Update)
    userForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const id = userIdInput.value;
        const userData = {
            name: nameInput.value,
            email: emailInput.value,
            phno: phnoInput.value
        };

        const method = id ? 'PUT' : 'POST';
        const url = id ? `/users/${id}` : '/users';

        try {
            const response = await fetch(url, {
                method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });

            if (response.ok) {
                showToast(id ? 'User updated successfully' : 'User added successfully');
                resetForm();
                fetchUsers();
            } else {
                const err = await response.json();
                showToast(err.error || 'Operation failed', 'error');
            }
        } catch (error) {
            showToast('Network error', 'error');
        }
    });

    // Reset form to initial state
    const resetForm = () => {
        userForm.reset();
        userIdInput.value = '';
        formTitle.textContent = 'Add New User';
        submitBtn.textContent = 'Add User';
        cancelBtn.classList.add('hidden');
    };

    // Edit user (Populate form)
    window.editUser = (id, name, email, phno) => {
        userIdInput.value = id;
        nameInput.value = name;
        emailInput.value = email;
        phnoInput.value = phno;
        
        formTitle.textContent = 'Update User';
        submitBtn.textContent = 'Update User';
        cancelBtn.classList.remove('hidden');
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // Delete user
    window.deleteUser = async (id) => {
        if (!confirm('Are you sure you want to delete this user?')) return;

        try {
            const response = await fetch(`/users/${id}`, { method: 'DELETE' });
            if (response.ok) {
                showToast('User deleted successfully');
                fetchUsers();
            } else {
                const err = await response.json();
                showToast(err.error || 'Failed to delete user', 'error');
            }
        } catch (error) {
            showToast('Error deleting user', 'error');
        }
    };

    cancelBtn.addEventListener('click', resetForm);

    // AI Assistant Logic
    const askAiBtn = document.getElementById('ask-ai-btn');
    const aiQuestion = document.getElementById('ai-question');
    const aiResponseContainer = document.getElementById('ai-response-container');
    const aiResponseText = document.getElementById('ai-response-text');
    const aiLoader = document.getElementById('ai-loader');
    const btnText = document.getElementById('btn-text');

    askAiBtn.addEventListener('click', async () => {
        const question = aiQuestion.value.trim();
        if (!question) {
            showToast('Please enter a question', 'error');
            return;
        }

        // UI State: Loading
        askAiBtn.disabled = true;
        aiLoader.classList.remove('hidden');
        btnText.textContent = 'Analyzing...';
        aiResponseContainer.classList.add('hidden');

        try {
            const response = await fetch('/ai/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });

            const data = await response.json();

            if (response.ok) {
                aiResponseText.textContent = data.answer;
                aiResponseContainer.classList.remove('hidden');
                // Smooth scroll to response
                aiResponseContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                showToast(data.error || 'AI analysis failed', 'error');
            }
        } catch (error) {
            showToast('Failed to connect to AI service', 'error');
        } finally {
            // UI State: Reset
            askAiBtn.disabled = false;
            aiLoader.classList.add('hidden');
            btnText.textContent = 'Ask Assistant';
        }
    });

    // Initial load
    fetchUsers();
});
