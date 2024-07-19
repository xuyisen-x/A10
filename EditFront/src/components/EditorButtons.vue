<script>
import 'remixicon/fonts/remixicon.css'

export default {
  props: {
    editor: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      tabNum: "1"
    }
  },
  methods: {
    textBtnDisable() {
      const { view, state } = this.editor
      const { from, to } = view.state.selection
      let a = !this.editor.isActive('image') && from !== to
      return !a
    },
    imgBtnDisable() {
      return !this.editor.isActive('image')
    }
  }
}
</script>

<template>
  <el-tabs type="border-card" class="control-tabs" v-model="tabNum">
    <el-tab-pane label="文件">
      <div class="panediv">
        <div class="miniblock">
          <div class="miniblock-above">
            <button @click="this.$emit('childEvent', 'exportJson');" :class="{ 'menu-item ': true }">
              <i class="ri-export-line"></i> JSON
            </button>
            <button @click="this.$emit('childEvent', 'exportHTML');" :class="{ 'menu-item ': true }">
              <i class="ri-html5-line"></i> HTML
            </button>
            <button title="不兼容表格" @click="this.$emit('childEvent', 'exportMarkdown');" :class="{ 'menu-item ': true }">
              <i class="ri-markdown-line"></i> Markdown
            </button>
          </div>
          <div class="miniblock-below">导出</div>
        </div>
        <el-divider direction="vertical" class="v-divider"/>
        <div class="miniblock">
          <div class="miniblock-above">
            <button @click="this.$emit('childEvent', 'importJson');" :class="{ 'menu-item ': true }">
              <i class="ri-import-line"></i> JSON
            </button>
          </div>
          <div class="miniblock-below">导入</div>
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="开始">
      <div class="panediv">
        <div class="miniblock">
          <div class="miniblock-above">
            <button title="Ctrl + Z" @click="editor.chain().focus().undo().run()" :disabled="!editor.can().chain().focus().undo().run()" :class="{ 'menu-item ': true }">
              <i class="ri-arrow-go-back-line"></i> 撤销
            </button>
            <button title="Ctrl + Shift + Z" @click="editor.chain().focus().redo().run()" :disabled="!editor.can().chain().focus().redo().run()" :class="{ 'menu-item ': true }">
              <i class="ri-arrow-go-forward-line"></i> 重做
            </button>
          </div>
          <div class="miniblock-below">编辑</div>
        </div>
        <el-divider direction="vertical" class="v-divider"/>
        <div class="miniblock">
          <div class="miniblock-above">
            <button title="Ctrl + B" @click="editor.chain().focus().toggleBold().run()" :disabled="!editor.can().chain().focus().toggleBold().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('bold') }">
              <i class="ri-bold"></i> 加粗
            </button>
            <button title="Ctrl + I" @click="editor.chain().focus().toggleItalic().run()" :disabled="!editor.can().chain().focus().toggleItalic().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('italic') }">
              <i class="ri-italic"></i> 斜体
            </button>
            <button title="Ctrl + Shift + S" @click="editor.chain().focus().toggleStrike().run()" :disabled="!editor.can().chain().focus().toggleStrike().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('strike') }">
              <i class="ri-strikethrough"></i> 删除线
            </button>
            <button title="Ctrl + U" @click="editor.chain().focus().toggleUnderline().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('underline') }">
              <i class="ri-underline"></i> 下划线
            </button>
            <button title="Ctrl + E" @click="editor.chain().focus().toggleCode().run()" :disabled="!editor.can().chain().focus().toggleCode().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('code') }">
              <i class="ri-code-view"></i> 代码
            </button>
            <button title="Ctrl + Shift + H" @click="editor.chain().focus().toggleHighlight().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('highlight') }">
              <i class="ri-mark-pen-line"></i> 高亮
            </button>
            <button @click="editor.chain().focus().unsetAllMarks().run()" :class="{ 'menu-item ': true }">
              <i class="ri-format-clear"></i> 清除格式
            </button>
          </div>
          <div class="miniblock-below">格式</div>
        </div>
        <el-divider direction="vertical" class="v-divider"/>
        <div class="miniblock">
          <div class="miniblock-above">
            <button title="Ctrl + Alt + 1" @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 1 }) }">
              <i class="ri-h-1"></i> 一级标题
            </button>
            <button title="Ctrl + Alt + 2" @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 2 }) }">
              <i class="ri-h-2"></i> 二级标题
            </button>
            <button title="Ctrl + Alt + 3" @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 3 }) }">
              <i class="ri-h-3"></i> 三级标题
            </button>
            <button title="Ctrl + Alt + 4" @click="editor.chain().focus().toggleHeading({ level: 4 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 4 }) }">
              <i class="ri-h-4"></i> 四级标题
            </button>
            <button title="Ctrl + Alt + 5" @click="editor.chain().focus().toggleHeading({ level: 5 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 5 }) }">
              <i class="ri-h-5"></i> 五级标题
            </button>
            <button title="Ctrl + Alt + 6" @click="editor.chain().focus().toggleHeading({ level: 6 }).run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('heading', { level: 6 }) }">
              <i class="ri-h-6"></i> 六级标题
            </button>
            <button title="Ctrl + Alt + 0" @click="editor.chain().focus().setParagraph().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('paragraph') }">
              <i class="ri-text"></i> 正文
            </button>
          </div>
          <div class="miniblock-below">样式</div>
        </div>
        <el-divider direction="vertical" class="v-divider"/>
        <div class="miniblock">
          <div class="miniblock-above">
            <button title="Ctrl + Shitt + L" @click="editor.chain().focus().setTextAlign('left').run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive({ textAlign: 'left' }) }">
            <i class="ri-align-left"></i> 左对齐
          </button>
          <button title="Ctrl + Shitt + R" @click="editor.chain().focus().setTextAlign('right').run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive({ textAlign: 'right' }) }">
            <i class="ri-align-right"></i> 右对齐
          </button>
          <button title="Ctrl + Shitt + E" @click="editor.chain().focus().setTextAlign('center').run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive({ textAlign: 'center' }) }">
            <i class="ri-align-center"></i>  居中对齐
          </button>
          <button title="Ctrl + Shitt + J" @click="editor.chain().focus().setTextAlign('justify').run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive({ textAlign: 'justify' }) }">
            <i class="ri-align-justify"></i> 两端对齐
          </button>
          <button title="Ctrl + Shift + 8" @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('bulletList') }">
            <i class="ri-list-unordered"></i>无序列表
          </button>
          <button title="Ctrl + Shift + 7" @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('orderedList') }">
            <i class="ri-list-ordered"></i>有序列表
          </button>
          <button title="Crtl + Alt + C" @click="editor.chain().focus().toggleCodeBlock().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('codeBlock') }">
            <i class="ri-code-block"></i>代码块
          </button>
          <button title="Ctrl + Shift + B" @click="editor.chain().focus().toggleBlockquote().run()" :class="{ 'menu-item ': true, 'is-active': editor.isActive('blockquote') }">
            <i class="ri-quote-text"></i>块引用
          </button>
          <button @click="editor.chain().focus().setHorizontalRule().run()" :class="{ 'menu-item ': true }">
            <i class="ri-separator"></i>水平分割线
          </button>
          <button title="Shift + Enter" @click="editor.chain().focus().setHardBreak().run()" :class="{ 'menu-item ': true }">
            <i class="ri-corner-down-left-line"></i>硬换行
          </button>
          </div>
          <div class="miniblock-below">段落</div>
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="插入">
      <div class="panediv">
        <div class="miniblock">
          <div class="miniblock-above">
            <button @click="this.$emit('childEvent', '插入图片');" :class="{ 'menu-item ': true }">
              <i class="ri-file-image-line"></i> 插入图片
            </button>
          </div>
          <div class="miniblock-below">图片</div>
        </div>
        <el-divider direction="vertical" class="v-divider"/>
        <div class="miniblock">
          <div class="miniblock-above">
            <button @click="this.$emit('childEvent', '音频转文本');" :class="{ 'menu-item ': true }">
              <i class="ri-mic-line"></i> 音频转文本
            </button>
          </div>
          <div class="miniblock-below">音频</div>
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="表格">
      <div class="panediv">
        <div class="miniblock">
          <div class="miniblock-above">
            <button @click="editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()" :class="{ 'menu-item ': true }">
              <i class="ri-table-2"></i>插入表格
            </button>
            <button @click="editor.chain().focus().deleteTable().run()" :class="{ 'menu-item ': true }">
              <i class="ri-table-2"></i>删除表格
            </button>
            <button @click="editor.chain().focus().addColumnBefore().run()" :class="{ 'menu-item ': true }">
              <i class="ri-insert-column-left"></i> 在左方插入列
            </button>
            <button @click="editor.chain().focus().addColumnAfter().run()" :class="{ 'menu-item ': true }">
              <i class="ri-insert-column-right"></i> 在右方插入列
            </button>
            <button @click="editor.chain().focus().addRowBefore().run()" :class="{ 'menu-item ': true }">
              <i class="ri-insert-row-top"></i> 在上方插入行
            </button>
            <button @click="editor.chain().focus().addRowAfter().run()" :class="{ 'menu-item ': true }">
              <i class="ri-insert-row-bottom"></i> 在下方插入行
            </button>
            <button @click="editor.chain().focus().deleteColumn().run()" :class="{ 'menu-item ': true }">
              <i class="ri-delete-column"></i> 删除列
            </button>
            <button @click="editor.chain().focus().deleteRow().run()" :class="{ 'menu-item ': true }">
              <i class="ri-delete-row"></i> 删除行
            </button>
            <button @click="editor.chain().focus().mergeCells().run()" :class="{ 'menu-item ': true }">
              <i class="ri-merge-cells-horizontal"></i> 合并单元格
            </button>
            <button @click="editor.chain().focus().splitCell().run()" :class="{ 'menu-item ': true }">
              <i class="ri-split-cells-horizontal"></i> 拆分单元格
            </button>
          </div>
          <div class="miniblock-below">表格工具</div>
        </div>
        <el-divider direction="vertical" class="v-divider"/>
        <div class="miniblock">
          <div class="miniblock-above">
            <button @click="editor.chain().focus().toggleHeaderColumn().run()" :class="{ 'menu-item ': true }">
              <i class="ri-h-5"></i> 标题列
            </button>
            <button @click="editor.chain().focus().toggleHeaderRow().run()" :class="{ 'menu-item ': true }">
              <i class="ri-h-5"></i> 标题行
            </button>
            <button @click="editor.chain().focus().toggleHeaderCell().run()" :class="{ 'menu-item ': true }">
              <i class="ri-h-5"></i> 标题单元格
            </button>
          </div>
          <div class="miniblock-below">格式</div>
        </div>
      </div>
    </el-tab-pane>
    <el-tab-pane label="工具">
      <div class="panediv">
        <div class="miniblock">
          <div class="miniblock-above">
            <button @click="this.$emit('childEvent', '润色');" :class="{ 'menu-item ': true }" :disabled="textBtnDisable()">
              <i class="ri-magic-line"></i> 润色
            </button>
            <button @click="this.$emit('childEvent', '缩写');" :class="{ 'menu-item ': true }" :disabled="textBtnDisable()">
              <i class="ri-collapse-horizontal-line"></i> 缩写
            </button>
            <button @click="this.$emit('childEvent', '扩写');" :class="{ 'menu-item ': true }" :disabled="textBtnDisable()">
              <i class="ri-expand-horizontal-line"></i> 扩写
            </button>
            <button @click="this.$emit('childEvent', '续写');" :class="{ 'menu-item ': true }" :disabled="textBtnDisable()">
              <i class="ri-expand-right-line"></i> 续写
            </button>
          </div>
          <div class="miniblock-below">AI工具</div>
        </div>
        <el-divider direction="vertical" class="v-divider"/>
        <div class="miniblock">
          <div class="miniblock-above">
            <button @click="this.$emit('childEvent', '翻译为中文');" :class="{ 'menu-item ': true }" :disabled="textBtnDisable()">
              <i class="ri-translate-2"></i> 翻译为中文
            </button>
            <button @click="this.$emit('childEvent', '翻译为英文');" :class="{ 'menu-item ': true }" :disabled="textBtnDisable()">
              <i class="ri-english-input"></i> 翻译为英文
            </button>
          </div>
          <div class="miniblock-below">翻译</div>
        </div>
        <el-divider direction="vertical" class="v-divider"/>
        <div class="miniblock">
          <div class="miniblock-above">
            <button @click="this.$emit('childEvent', 'OCR');" :class="{ 'menu-item ': true }" :disabled="imgBtnDisable()">
              <i class="ri-character-recognition-line"></i> OCR
            </button>
            <button @click="this.$emit('childEvent', '公式识别');" :class="{ 'menu-item ': true }" :disabled="imgBtnDisable()">
              <i class="ri-formula"></i> 公式识别
            </button>
          </div>
          <div class="miniblock-below">图片工具</div>
        </div>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<style lang="scss" scoped>

.menu-item {
  background: white;
  border-radius: 0.4rem;
  color: #333;
  cursor: pointer;
  height: 1.75rem;
  width: max-content;
  padding: 0.25rem;
  margin-right: 0.25rem;

  &:hover {
    border-color: #409EFF;
  }

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

.panediv {
  height:80px;
  display: flex;
  flex-direction: row;
  overflow-x: auto;
}

.miniblock{
  height: 100%;
  display: grid;
  grid-template-rows: 70% 30%;
  grid-template-columns: auto;
}

.miniblock-below{
  text-align: center;
}

.v-divider{
  height:75%;
  position: relative;
  top:12.5%;
}

.miniblock-above{
  display: grid;
  grid-template-rows: repeat(2, auto); /* 固定两行 */
  grid-auto-flow: column; /* 自动按列填充 */
}

</style>

<style lang="scss">
.control-tabs > .el-tabs__content {
  padding: 0px;
}

.el-tabs{
  border-bottom-left-radius: 12px;  /* 左下角 */
  border-bottom-right-radius: 12px; /* 右下角 */
}

.el-tabs--border-card > .el-tabs__header .el-tabs__item {
  border-top-left-radius: 6px;  /* 左下角 */
  border-top-right-radius: 6px; /* 右下角 */
}
</style>