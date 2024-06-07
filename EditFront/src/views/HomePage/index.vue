<template>
  <div class="mainbody">
    <h1 class="headtitle">首页</h1>
    <div>
      <h2 class="">{{ demoStore.helloPinia}}</h2>
    </div>
    <el-button type="primary">你好，这里使用Elemet-Plus</el-button>
  </div>
</template>
<script setup lang="ts">
import { mainStore} from '../../store/index'
/* 得到countStore */
const demoStore =mainStore()

import {adduser} from "../../api";
//进行测试接口调用
let a = adduser("12345","54321");
a.then(res => {
  alert(res)
});
</script>

<style scoped>
.mainbody {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.headtitle {
  filter: drop-shadow(0 0 2em #646cffaa);
}
</style>