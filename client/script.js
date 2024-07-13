document.addEventListener('DOMContentLoaded', function() {
    fetch('') 
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

           
            const totalUsers = data.length;
            userCountElement.textContent = totalUsers;
        })
        .catch(error => console.error('Error fetching users data:', error));
});

const userChartContext = document.getElementById('userChart').getContext('2d');
const userChart = new Chart(userChartContext, {
    type: 'line',
    data: {
        labels: users.map(user => user.joinDate),
        datasets: [{
            label: 'Total Users Over Time',
            data: users.map((user, index) => index + 1),
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
                    text: 'Join Date'
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

