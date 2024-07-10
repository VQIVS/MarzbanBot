document.addEventListener('DOMContentLoaded', function() {
    
    fetch('/get_users') 
        .then(response => response.json())
        .then(data => {
            const usersList = document.getElementById('users-list');

            
            data.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.username}</td>
                    <td>${user.join_date}</td>
                `;
                usersList.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching users data:', error));
});
