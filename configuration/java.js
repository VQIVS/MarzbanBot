document.getElementById('settingsButton').addEventListener('click', async function() {
    document.getElementById('settingsTable').style.display = 'table';

    try {
        const response = await fetch('http://135.181.100.53:8000/api/v1/website/configuration');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        populateTable(data);
    } catch (error) {
        console.error('Error:', error);
    }
});

function populateTable(data) {
    const tbody = document.querySelector('#settingsTable tbody');
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.id}</td>
            <td><input type="text" value="${item. panelusername}" data-id="${item.id}" data-field="username" disabled></td>
            <td><input type="password" value="${item.panelpassword}" data-id="${item.id}" data-field="password" disabled></td>
            <td><input type="text" value="${item.botname}" data-id="${item.id}" data-field="name" disabled></td>
            <td><input type="text" value="${item.boturl}" data-id="${item.id}" data-field="website" disabled></td>
            <td><input type="text" value="${item.panel_url}" data-id="${item.id}" data-field="panel_url" disabled></td>
            <td><input type="text" value="${item.token}" data-id="${item.id}" data-field="token" disabled></td>
            <td>
                <button class="edit-button" onclick="enableEditing(${item.id})">Edit</button>
                <button class="save-button" onclick="updateRow(${item.id})">Save</button>
                <button class="delete-button" onclick="deleteRow(${item.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function enableEditing(id) {
    const row = document.querySelector(`tr td input[data-id="${id}"]`).closest('tr');
    const inputs = row.querySelectorAll('input');

    inputs.forEach(input => input.disabled = false);
    row.classList.add('editing'); 
    row.querySelector('.edit-button').style.display = 'none';
    row.querySelector('.save-button').style.display = 'inline';
    row.querySelector('.delete-button').style.display = 'inline';
}

async function updateRow(id) {
    const row = document.querySelector(`tr td input[data-id="${id}"]`).closest('tr');
    const inputs = row.querySelectorAll('input');

    const updatedData = {
        username: row.querySelector('input[data-field="panelusername"]').value,
        password: row.querySelector('input[data-field="panelpassword"]').value,
        name: row.querySelector('input[data-field="botname"]').value,
        website: row.querySelector('input[data-field="boturl"]').value,
        panel_url: row.querySelector('input[data-field="panel_url"]').value,
        token: row.querySelector('input[data-field="token"]').value,
    };

    try {
        const response = await fetch( 'http://135.181.100.53:8000/api/v1/website/configuration/1/', {
            method: 'Patch', 
            headers: {
                'Content-Type': 'application/json' ,

                "X-CSRFToken" : 'IylYPy75aQ1cx38lMxWXtNV3iJXK57MVLQ5lCTxxBOOgyIHwNDfbKTxIwTEIXZtU',
            },
            body: JSON.stringify(updatedData)
        });

        if (!response.ok) {
            throw new Error('Failed to update data');
        }

        showMessage('Data updated successfully!', 'success');
        
        inputs.forEach(input => input.disabled = true);
        row.classList.remove('editing'); 
        row.querySelector('.edit-button').style.display = 'inline';
        row.querySelector('.save-button').style.display = 'none';
        row.querySelector('.delete-button').style.display = 'none';
    } catch (error) {
        showMessage('Failed to update data', 'error');
        console.error('Error:', error);
    }
}

async function deleteRow(id) {
    if (confirm('Are you sure you want to delete this row?')) {
        try {
            const response = await fetch( 'http://135.181.100.53:8000/api/v1/website/configuration/1/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json' ,
    
                    "X-CSRFToken" : 'f1WelCOSI4tzUQ2W9PnTKuK0ZfDYkn6DijGB8Xek92gDVvB7aVG71AmFdpkWcfNC',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to delete data');
            }

            showMessage('Row deleted successfully!', 'success');
            document.querySelector(`tr td input[data-id="${id}"]`).closest('tr').remove();
        } catch (error) {
            showMessage('Failed to delete data', 'error');
            console.error('Error:', error);
        }
    }
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = message;
    messageDiv.className = type;
    messageDiv.classList.remove('hidden');
    
    setTimeout(() => {
        messageDiv.classList.add('hidden');
    }, 3000);
}
