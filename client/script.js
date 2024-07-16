document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('http://135.181.100.53:8000/api/v1/bot/bot-user/', {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'X-CSRFToken': 'YB8ilm7z3oFXXgUFnPeNCx3kMUgjM2JdDbN4MSq8YbJoo48zYFYJmh8Iu225xvVT'
            }
        });

        if (!response.ok) {
            console.error('Response status:', response.status);
            console.error('Response status text:', response.statusText);
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('Data received:', data);

        const usersList = document.getElementById('users-list');
        const userCountElement = document.getElementById('user-count');
        usersList.innerHTML = ''; 

        const userIds = [];

        data.forEach((item, index) => {
            const userId = item.user_id;  
            const row = document.createElement('tr');
            row.innerHTML = `<td>${userId}</td>`;
            usersList.appendChild(row);

            userIds.push(userId);
        });

        const totalUsers = data.length;
        userCountElement.textContent = totalUsers;

        const userChartContext = document.getElementById('userChart').getContext('2d');
        new Chart(userChartContext, {
            type: 'line',
            data: {
                labels: userIds.map((id, index) => index + 1),
                datasets: [{
                    label: 'Total Users Over Time',
                    data: userIds.map((id, index) => index + 1),
                    borderColor: 'rgba(41, 128, 185, 1)',
                    backgroundColor: 'rgba(41, 128, 185, 0.2)',
                    fill: true,
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'User Index'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Total Users'
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const previousValue = context.raw - 1;
                                const difference = context.raw - previousValue;
                                return `Total Users: ${context.raw} (Change: +${difference})`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching users data:', error);
    }
});
