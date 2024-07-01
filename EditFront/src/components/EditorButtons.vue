<script>
import 'remixicon/fonts/remixicon.css'

export default {
  props: {
    editor: {
      type: Object,
      required: true,
    },
  },
}
</script>

<template>
  <div class="button-group">
    <button title="加粗" @click="editor.chain().focus().toggleBold().run()" :disabled="!editor.can().chain().focus().toggleBold().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('bold') }">
      <i class="ri-bold"></i>
    </button>
    <button title="斜体" @click="editor.chain().focus().toggleItalic().run()" :disabled="!editor.can().chain().focus().toggleItalic().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('italic') }">
      <i class="ri-italic"></i>
    </button>
    <button title="删除线" @click="editor.chain().focus().toggleStrike().run()" :disabled="!editor.can().chain().focus().toggleStrike().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('strike') }">
      <i class="ri-strikethrough"></i>
    </button>
    <button title="下划线" @click="editor.chain().focus().toggleUnderline().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('underline') }">
      <i class="ri-underline"></i>
    </button>
    <button title="代码" @click="editor.chain().focus().toggleCode().run()" :disabled="!editor.can().chain().focus().toggleCode().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('code') }">
      <i class="ri-code-view"></i>
    </button>
    <button title="清除格式" @click="editor.chain().focus().unsetAllMarks().run()" :class="{ 'menu-item ': true }">
      <i class="ri-format-clear"></i>
    </button>
<!--    <button @click="editor.chain().focus().clearNodes().run()">-->
<!--      Clear nodes-->
<!--    </button>-->
    <button title="正文" @click="editor.chain().focus().setParagraph().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('paragraph') }">
      <i class="ri-text"></i>
    </button>
    <button title="一级标题" @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 1 }) }">
      <i class="ri-h-1"></i>
    </button>
    <button title="二级标题" @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 2 }) }">
      <i class="ri-h-2"></i>
    </button>
    <button title="三级标题" @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 3 }) }">
      <i class="ri-h-3"></i>
    </button>
    <button title="四级标题" @click="editor.chain().focus().toggleHeading({ level: 4 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 4 }) }">
      <i class="ri-h-4"></i>
    </button>
    <button title="五级标题" @click="editor.chain().focus().toggleHeading({ level: 5 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 5 }) }">
      <i class="ri-h-4"></i>
    </button>
    <button title="六级标题" @click="editor.chain().focus().toggleHeading({ level: 6 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 6 }) }">
      <i class="ri-h-6"></i>
    </button>
    <button title="无序列表" @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('bulletList') }">
      <i class="ri-list-unordered"></i>
    </button>
    <button title="有序列表" @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('orderedList') }">
      <i class="ri-list-ordered"></i>
    </button>
    <button title="代码块" @click="editor.chain().focus().toggleCodeBlock().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('codeBlock') }">
      <i class="ri-code-block"></i>
    </button>
    <button title="块引用" @click="editor.chain().focus().toggleBlockquote().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('blockquote') }">
      <i class="ri-quote-text"></i>
    </button>
    <button title="水平分割线" @click="editor.chain().focus().setHorizontalRule().run()" :class="{ 'menu-item ': true }">
      <i class="ri-separator"></i>
    </button>
    <button title="硬换行" @click="editor.chain().focus().setHardBreak().run()" :class="{ 'menu-item ': true }">
      <i class="ri-corner-down-left-line"></i>
    </button>
    <button title="撤销" @click="editor.chain().focus().undo().run()" :disabled="!editor.can().chain().focus().undo().run()" :class="{ 'menu-item ': true }">
      <i class="ri-arrow-go-back-line"></i>
    </button>
    <button title="重做" @click="editor.chain().focus().redo().run()" :disabled="!editor.can().chain().focus().redo().run()" :class="{ 'menu-item ': true }">
      <i class="ri-arrow-go-forward-line"></i>
    </button>
    <button title="高亮" @click="editor.chain().focus().toggleHighlight().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('highlight') }">
      <i class="ri-mark-pen-line"></i>
    </button>
    <button title="左对齐" @click="editor.chain().focus().setTextAlign('left').run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive({ textAlign: 'left' }) }">
      <i class="ri-align-left"></i>
    </button>
    <button title="居中" @click="editor.chain().focus().setTextAlign('center').run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive({ textAlign: 'center' }) }">
      <i class="ri-align-center"></i>
    </button>
    <button title="右对齐" @click="editor.chain().focus().setTextAlign('right').run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive({ textAlign: 'right' }) }">
      <i class="ri-align-right"></i>
    </button>
    <button title="两端对齐" @click="editor.chain().focus().setTextAlign('justify').run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive({ textAlign: 'justify' }) }">
      <i class="ri-align-justify"></i>
    </button>
  </div>
</template>

<style lang="scss">

.menu-item {
  background: white;
  border: none;
  border-radius: 0.4rem;
  color: #333;
  cursor: pointer;
  height: 1.75rem;
  padding: 0.25rem;
  margin-right: 0.25rem;
  width: 1.75rem;

  svg {
    fill: currentColor;
    height: 100%;
    width: 100%;
  }
}

.is-active {
  background-color: #409EFF;
  color: white;
  &:hover {
    background-color: #0080ff;
  }
}
</style>