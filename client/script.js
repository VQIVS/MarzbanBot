document.addEventListener('DOMContentLoaded', function() {
    fetch('') 
        .then(response => response.json())
        .then(data => {
            const usersList = document.getElementById('users-list');
            const userCountElement = document.getElementById('user-count');
            const userDates = [];
            const userCounts = [];

            data.forEach((user, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.username}</td>
                    <td>${new Date(user.id * 10000000000).toLocaleDateString()}</td>
                `;
                usersList.appendChild(row);

                
                userDates.push(new Date(user.id * 10000000000).toLocaleDateString());
                userCounts.push(index + 1);
            });

            const totalUsers = data.length;
            userCountElement.textContent = totalUsers;

           
            const userChartContext = document.getElementById('userChart').getContext('2d');
            new Chart(userChartContext, {
                type: 'line',
                data: {
                    labels: userDates,
                    datasets: [{
                        label: 'Total Users Over Time',
                        data: userCounts,
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
        })
        .catch(error => console.error('Error fetching users data:', error));
});
