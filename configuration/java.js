document.getElementById('settingsButton').addEventListener('click', async function() {
    // نمایش کارت تنظیمات
    document.getElementById('settingsContainer').classList.remove('hidden');
    
    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/users/1'); // گرفتن کارت با ID 1
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        populateCard(data);
    } catch (error) {
        console.error('Error:', error);
    }
});

function populateCard(data) {
    const container = document.getElementById('settingsContainer');
    container.innerHTML = `
        <div class="card">
            <h3>Configuration Details</h3>
            <label for="username">Username:</label>
            <input type="text" id="username" value="${data.username}" disabled>
            <label for="password">Password:</label>
            <input type="password" id="password" value="${data.password}" disabled>
            <label for="botname">Bot Name:</label>
            <input type="text" id="botname" value="Bot${data.id}" disabled>
            <label for="bot_url">Bot URL:</label>
            <input type="text" id="bot_url" value="${data.bot_url || ''}" disabled>
            <label for="panel_url">Panel URL:</label>
            <input type="text" id="panel_url" value="http://example.com/panel${data.id}" disabled>
            <label for="token">Token:</label>
            <input type="text" id="token" value="token${data.id}" disabled>
            <div>
                <button class="edit-button" onclick="enableEditing()">Edit</button>
                <button class="save-button" onclick="updateCard()" style="display: none;">Save</button>
                <button class="delete-button" onclick="deleteCard()" style="display: none;">Delete</button>
            </div>
        </div>
    `;
}

function enableEditing() {
    const inputs = document.querySelectorAll('#settingsContainer input');
    inputs.forEach(input => input.disabled = false);
    document.querySelector('.edit-button').style.display = 'none';
    document.querySelector('.save-button').style.display = 'inline';
    document.querySelector('.delete-button').style.display = 'inline';
}

async function updateCard() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const botname = document.getElementById('botname').value;
    const bot_url = document.getElementById('bot_url').value;
    const panel_url = document.getElementById('panel_url').value;
    const token = document.getElementById('token').value;

    const updatedData = {
        username,
        password,
        botname,
        bot_url,  // اضافه کردن فیلد جدید
        panel_url,
        token
    };

    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/users/1', {  // به‌روزرسانی کارت با ID 1
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        });

        if (!response.ok) {
            throw new Error('Failed to update data');
        }

        showMessage('Data updated successfully!', 'success');
        disableEditing();
    } catch (error) {
        showMessage('Failed to update data', 'error');
        console.error('Error:', error);
    }
}

async function deleteCard() {
    if (confirm('Are you sure you want to delete this card?')) {
        try {
            const response = await fetch('https://jsonplaceholder.typicode.com/users/1', {  // حذف کارت با ID 1
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to delete data');
            }

            showMessage('Card deleted successfully!', 'success');
            document.getElementById('settingsContainer').innerHTML = ''; // پاک کردن محتوای کارت
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

function disableEditing() {
    const inputs = document.querySelectorAll('#settingsContainer input');
    inputs.forEach(input => input.disabled = true);
    document.querySelector('.edit-button').style.display = 'inline';
    document.querySelector('.save-button').style.display = 'none';
    document.querySelector('.delete-button').style.display = 'none';
}
