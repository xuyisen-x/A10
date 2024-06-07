<template>
  <div>
    <h1 class="headtitle">请在下方编辑</h1>
  </div>
  <div id="tiptapEditor">
    <Tiptap />
  </div>
</template>

<script setup lang="ts">
import Tiptap from '../../components/TipTap.vue'
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