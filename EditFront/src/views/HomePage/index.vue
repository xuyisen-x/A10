<!-- <template>
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
</style> -->
<template>
  <el-button link type="primary" @click="centerDialogVisible = true">点击打开 Dialog</el-button>

  <el-dialog
    header="提示"
    :model-value="centerDialogVisible"
    width="30%"
    center>
    <span>需要注意的是内容是默认不居中的</span>
    <span slot="footer" class="dialog-footer">
      <el-button @click="centerDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="centerDialogVisible = false">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
  export default {
    data() {
      return {
        centerDialogVisible: false
      };
    }
  };
</script>
