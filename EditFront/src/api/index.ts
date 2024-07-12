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

export function getOCR(user:string, key: string, dataURL: string) {
    const base64Part = dataURL.split(',')[1];

    // 构造 URL 编码的字符串
    const params = new URLSearchParams();
    params.append("user", user);
    params.append("key", key);
    params.append('cont', base64Part); // 注意这里只是 base64 编码的部分

    // 发送请求，使用 params.toString() 获取 URL 编码的字符串作为请求体
    return http.request({
        url: '/getOCR',
        method: 'post',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: params.toString() // 使用 toString() 方法将 URLSearchParams 转换为字符串
    });
}

export function getDecribe(user:string, key: string, dataURL: string) {
    const base64Part = dataURL.split(',')[1];

    // 构造 URL 编码的字符串
    const params = new URLSearchParams();
    params.append("user", user);
    params.append("key", key);
    params.append('cont', base64Part); // 注意这里只是 base64 编码的部分

    // 发送请求，使用 params.toString() 获取 URL 编码的字符串作为请求体
    return http.request({
        url: '/getdescribe',
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        },
        data: params.toString() // 使用 toString() 方法将 URLSearchParams 转换为字符串
    });
}


export function getObjectDetection(user: string, key: string, dataURL: string) {
    // 内部函数：将dataURL转换为Blob对象
    function dataURLtoBlob(dataurl: string) {
        let arr = dataurl.split(','),
            mimeMatch = arr[0].match(/:(.*?);/), // 尝试匹配MIME类型
            mime = mimeMatch ? mimeMatch[1] : ''; // 确保mimeMatch不为null或undefined

        // 其他代码保持不变，除非需要额外的空值检查
        let bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], {type: mime});
    }

    // 其他代码保持不变
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);

    let blob = dataURLtoBlob(dataURL);
    formData.append("cont", blob, "image.png");

    return http.request({
        url: '/getobjectdetection',
        method: 'post',
        data: formData
    });
}

export function getAudioRecognition(user: string, key: string, dataURL: string) {
    // 内部函数：将dataURL转换为Blob对象
    function dataURLtoBlob(dataurl: string) {
        let arr = dataurl.split(','),
            mimeMatch = arr[0].match(/:(.*?);/), // 尝试匹配MIME类型
            mime = mimeMatch ? mimeMatch[1] : ''; // 确保mimeMatch不为null或undefined

        // 其他代码保持不变，除非需要额外的空值检查
        let bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], {type: mime});
    }

    // 其他代码保持不变
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);

    let blob = dataURLtoBlob(dataURL);
    formData.append("cont", blob, "image.png");

    return http.request({
        url: '/getaudiorecognition',
        method: 'post',
        data: formData
    });
}

export function getVideoSummary(user: string, key: string, dataURL: string) {
    // 内部函数：将dataURL转换为Blob对象
    function dataURLtoBlob(dataurl: string) {
        let arr = dataurl.split(','),
            mimeMatch = arr[0].match(/:(.*?);/), // 尝试匹配MIME类型
            mime = mimeMatch ? mimeMatch[1] : ''; // 确保mimeMatch不为null或undefined

        // 其他代码保持不变，除非需要额外的空值检查
        let bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], {type: mime});
    }

    // 其他代码保持不变
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);

    let blob = dataURLtoBlob(dataURL);
    formData.append("cont", blob, "image.png");

    return http.request({
        url: '/getvideosummary',
        method: 'post',
        data: formData
    });
}

export function getImageGeneration(user: string, key: string, cont: string) {
    // 内部函数：将dataURL转换为Blob对象
    let formData = new FormData();
    formData.append("user", user);
    formData.append("key", key);
    formData.append("cont", cont);
    return http.request({
        url: '/getimagegeneration',
        method: 'post',
        data: formData
    })
}