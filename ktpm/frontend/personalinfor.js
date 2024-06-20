$(document).ready(function() {
    var username = localStorage.getItem('username');
    var name = localStorage.getItem('name'); 

    if (name && username) {
        $('#username-display').text(name);
        $('#userDropdown').show();
        $('#loginSignup').hide();
    } else {
        $('#userDropdown').hide();
        $('#loginSignup').show();
    }

    $('#logout-button').click(function() {
        localStorage.removeItem('username');
        localStorage.removeItem('name');
        window.location.href = 'login.html'; 
    });
    $('#service-button').click(function() {
        window.location.href = 'service.html';
    });
    $('#classform-button').click(function() {
        window.location.href = 'classform.html';
    })
    $('#searching-button').click(function() {
        window.location.href = 'search.html';
    })
    $('#mainpage-button').click(function() {
        window.location.href = 'mainpage.html';
    })

    const storedUsername = localStorage.getItem('username');
    console.log('Stored username:', storedUsername); // Kiểm tra giá trị username
    if (storedUsername) {
        console.log('Sending request to /userinfo with username:', storedUsername);
        fetch(`http://localhost:5009/userinfo?username=${encodeURIComponent(storedUsername)}`)
            .then(response => {
                if (!response.ok) {
                    if (response.status === 404) {
                        throw new Error('Resource not found');
                    } else {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                }
                return response.json(); // Chuyển trực tiếp response thành JSON
            })
            .then(data => {
                console.log('Received response from /userinfo:', data);
                if (data.error) {
                    alert(data.error);
                } else {
                    // Hiển thị thông tin lên trang web
                    $('#username').text(data.username);
                    $('#name').text(data.name);
                    $('#gender').text(data.gender);
                    $('#role').text(data.role);
                    $('#area').text(data.area);
                    $('#phone').text(data.phone);
                    $('#academic').text(data.academic);
                }
            })
            .catch(error => {
                if (error.message === 'Resource not found') {
                    console.error('User info resource not found. Please check the endpoint.');
                } else {
                    console.error('Fetch error:', error);
                }
            });

    }
});
