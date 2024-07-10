document.addEventListener('DOMContentLoaded', function() {
    // Fetch users data from server
    fetch('/get_users') // Replace with your backend endpoint
        .then(response => response.json())
        .then(data => {
            const usersList = document.getElementById('users-list');

            // Iterate through users data and create table rows
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
