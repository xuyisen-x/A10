<template>
  <div class="auth-container">
    <div class="auth-toggle">
      <button @click="toggleForm('login')" :class="{ active: isLogin }">登录</button>
      <button @click="toggleForm('register')" :class="{ active: !isLogin }">注册</button>
    </div>
    <div class="auth-form">
      <form v-if="isLogin" @submit.prevent="handleLogin">
        <h2>登录</h2>
        <div class="form-group">
          <label for="loginUsername">用户名:</label>
          <input type="text" id="loginUsername" v-model="loginData.username" required />
        </div>
        <div class="form-group">
          <label for="loginPassword">密码:</label>
          <input type="password" id="loginPassword" v-model="loginData.password" required />
        </div>
        <button type="submit">登录</button>
      </form>
      <form v-else @submit.prevent="handleRegister">
        <h2>注册</h2>
        <div class="form-group">
          <label for="registerUsername">用户名:</label>
          <input type="text" id="registerUsername" v-model="registerData.username" required />
        </div>
        <div class="form-group">
          <label for="registerPassword">密码:</label>
          <input type="password" id="registerPassword" v-model="registerData.password" required />
        </div>
        <div class="form-group">
  <label for="registerConfirmPassword">确认密码:</label>
  <input type="password" id="registerConfirmPassword" v-model="registerData.confirmPassword" required />
  <span v-if="passwordMismatch" class="error-message">密码和确认密码不匹配</span>
        </div>
        <button type="submit">注册</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthComponent',
  data() {
  return {
  passwordMismatch: false,
      isLogin: true,
      loginData: {
        username: '',
        password: ''
      },
      registerData: {
        username: '',
        password: '',
        confirmPassword: ''
      }
    };
  },
  methods: {
    toggleForm(form) {
      this.isLogin = form === 'login';
    },
    handleLogin() {
      // 处理登录逻辑，例如调用 API
      console.log('登录信息:', this.loginData);
      // 可以在这里添加更多的验证和请求逻辑
    },
    handleRegister() {
// 处理注册逻辑，例如调用 API
  if (this.registerData.password !== this.registerData.confirmPassword) {
  this.passwordMismatch = true;
  return;
  } else {
  this.passwordMismatch = false;
  }
      console.log('注册信息:', this.registerData);
      // 可以在这里添加更多的验证和请求逻辑
    }
  }
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 15px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}
.auth-toggle {
  display: flex;
  gap: 10px;
  justify-content: space-around;
  margin-bottom: 30px;
}
.auth-toggle button {
  padding: 12px;
  width: 160px;
  cursor: pointer;
  border: none;
  background-color: #e0e0e0;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
}
.auth-toggle button:hover {
  background-color: #d0d0d0;
  transform: scale(1.05);
}
.auth-toggle button.active {
  font-weight: bold;
  background-color: #0080ff;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 128, 255, 0.4);
}
.auth-form h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
  font-weight: 500;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}
.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  transition: border-color 0.3s;
}
.form-group input:focus {
  border-color: #0080ff;
  outline: none;
}
button[type="submit"] {
  width: 100%;
  padding: 12px;
  background-color: #0080ff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
}
button[type="submit"]:hover {
  background-color: #0066cc;
  transform: scale(1.05);
}
.error-message {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}
</style>
