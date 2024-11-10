import http from '../utils/request'

export function getOCR(dataurl: string) {
    let formData = new FormData();
    formData.append("dataurl",dataurl);
    return http.request({
        url: '/ocr',
        method: 'post',
        data: formData
    })
}

export function getASR(dataurl: string) {
    let formData = new FormData();
    formData.append("dataurl",dataurl);
    return http.request({
        url: '/asr',
        method: 'post',
        data: formData
    })
}

export function getFormula(dataurl: string) {
    let formData = new FormData();
    formData.append("dataurl",dataurl);
    return http.request({
        url: '/formula',
        method: 'post',
        data: formData
    })
}

export function getTranslate(q: string, to: string) {
    let formData = new FormData();
    formData.append("q",q);
    formData.append("to",to);
    console.log(formData)
    return http.request({
        url: '/translate',
        method: 'post',
        data: formData
    })
}

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

export function login(username: string, password: string) {
    let formData = new FormData();
    formData.append("username",username);
    formData.append("password",password);
    return http.request({
        url: '/login',
        method: 'post',
        data: formData
    })
}

export function getPolish(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return fetch('/api/getpolish', {
        method: 'post',
        credentials: 'include',
        body: formData
    });
}

export function getAbbreviate(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return fetch('/api/getabbreviate', {
        method: 'post',
        credentials: 'include',
        body: formData
    });
}

export function getExpand(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return fetch('/api/getexpand', {
        method: 'post',
        credentials: 'include',
        body: formData
    });
}

export function getExtend(user:string, key: string, cont: string){
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return fetch('/api/getextend', {
        method: 'post',
        credentials: 'include',
        body: formData
    });
}