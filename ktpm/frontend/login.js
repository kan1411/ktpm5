$(document).ready(function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault();
  
        var username = $('#username').val();
        var password = $('#password').val();
  
        console.log('Submitting form with:', username, password);
  
        $.ajax({
            url: 'http://localhost:5010/login', // Điều chỉnh cổng
            method: 'POST',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
                console.log('Response from server:', response); // Kiểm tra phản hồi từ máy chủ
                console.log('Response keys:', Object.keys(response)); // In ra các key của đối tượng phản hồi
                
                if (response.username && response.name) { // Kiểm tra thuộc tính trong phản hồi
                    console.log('Saving to localStorage:', response.username, response.name);
                    localStorage.setItem('username', response.username);
                    localStorage.setItem('name', response.name);
                    
                    // Hiển thị thông báo thành công và chờ 2 giây trước khi điều hướng
                    Swal.fire({
                        title: 'Thành công!',
                        text: response.message,
                        icon: 'success',
                        timer: 2000,
                        showConfirmButton: false
                    }).then(() => {
                        // Điều hướng sau khi lưu trữ
                        window.location.href = 'mainpage.html'; 
                    });
                } else {
                    console.error('Phản hồi không chứa username hoặc name');
                }
            },
            error: function(error) {
                console.log('Error from server:', error); // Kiểm tra lỗi
                Swal.fire({
                    title: 'Lỗi!',
                    text: 'Tài khoản hoặc mật khẩu lỗi',
                    icon: 'error'
                });
            }
        });
    });
  
    var username = localStorage.getItem('username');
    console.log('Username in localStorage:', username);
    if (username) {
        $('#userDropdown').text(username);
    }
});
