// 页面加载时获取所有用户
window.onload = function() {
    loadUsers();
};

// 加载所有用户
function loadUsers() {
    fetch('/api/users')
        // 函数体只有一行返回语句时，可以省略大括号和 return
        .then(response => response.json())
        .then(users => {
            const tableBody = document.getElementById('userTableBody');
            tableBody.innerHTML = '';
            
            users.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.username}</td>
                    <td>${user.nickname}</td>
                    <td>${user.level}</td>
                    <td>${user.experience}</td>
                    <td>${new Date(user.registration_time).toLocaleString()}</td>
                    <td>
                        <a href="/user/${user.id}" class="btn btn-sm btn-info">详情</a>
                        <button class="btn btn-sm btn-danger" onclick="deleteUser('${user.id}')">删除</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
}

// 添加用户
function addUser() {
    const form = document.getElementById('addUserForm');
    const formData = new FormData(form);
    const userData = Object.fromEntries(formData);
    
    // 转换数字类型
    userData.level = parseInt(userData.level);
    
    fetch('/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())
    .then(data => {
        // 关闭模态框
        const modal = bootstrap.Modal.getInstance(document.getElementById('addUserModal'));
        modal.hide();
        
        // 重置表单
        form.reset();
        
        // 重新加载用户列表
        loadUsers();
        
        alert('用户添加成功！');
    })
    .catch(error => console.error('Error:', error));
}

// 删除用户
function deleteUser(userId) {
    if (confirm('确定要删除这个用户吗？')) {
        fetch(`/api/users/${userId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadUsers();
                alert('用户删除成功！');
            } else {
                alert('删除失败：' + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}