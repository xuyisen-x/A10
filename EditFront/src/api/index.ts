import http from '../utils/request'

export function adduser(username: string, password: string) {
    let formData = new FormData();
    formData.append("username",username);
    formData.append("password",password);
    return http.request({
        url: '/adduser',
        method: 'post',
        data: formData
    })
}