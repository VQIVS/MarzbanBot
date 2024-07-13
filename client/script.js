document.addEventListener('DOMContentLoaded', function() {
    fetch('http://135.181.100.53:8000/api/users') 
        .then(response => response.json())
        .then(data => {
            const usersList = document.getElementById('users-list');
            const userCountElement = document.getElementById('user-count');

            data.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.username}</td>
                    <td>${user.join_date}</td>
                `;
                usersList.appendChild(row);
            });

            // Update total users count
            const totalUsers = data.length;
            userCountElement.textContent = totalUsers;
        })
        .catch(error => console.error('Error fetching users data:', error));
});
