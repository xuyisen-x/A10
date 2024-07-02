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

export function getPolish(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return http.request({
        url: '/getpolish',
        method: 'post',
        data: formData
    })
}

export function getAbbreviate(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return http.request({
        url: '/getabbreviate',
        method: 'post',
        data: formData
    })
}

export function getExpand(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return http.request({
        url: '/getexpand',
        method: 'post',
        data: formData
    })
}

export function getExtend(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return http.request({
        url: '/getextend',
        method: 'post',
        data: formData
    })
}

export function getOCR(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return http.request({
        url: '/getextend',
        method: 'post',
        data: formData
    })
}

export function getDescribe(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return http.request({
        url: '/getextend',
        method: 'post',
        data: formData
    })
}