<template>
  <div v-if="editor" class="common-layout" style="width: 100vw; height: 100vh;">
    <div class="control-group">
      <EditorButtons :editor="editor" @childEvent="handleChildEvent" />
    </div>
    <el-container class="main-container">
      <el-aside style="height: 100%;">
        <h3 id="title-of-contents">大纲</h3>
        <div id="table-of-contents"/>
      </el-aside>
      <el-main style="height: 100%; overflow-y: auto;">
        <div class="editor-container">
          <BubbleMenu
            class="bubble-menu bm1"
            style="font-size: small"
            :tippy-options="{ duration: 100 }"
            :editor="editor"
            :should-show="props => {
                return !props.editor.isActive('image') && props.from !== props.to
            }"
          >
            <el-dropdown>
              <button class="buble-btn">
                <i class="ri-pen-nib-line"></i>
                AI工具
                <i class="ri-arrow-down-s-line"></i>
              </button>
              <template #dropdown>
                <div>
                  <button class="buble-btn boxbtn" @click="polishText">
                    <i class="ri-magic-line"></i>
                    润色
                  </button>
                  <button class="buble-btn boxbtn" @click="abbreviateText">
                    <i class="ri-collapse-horizontal-line"></i>
                    缩写
                  </button>
                  <button class="buble-btn boxbtn" @click="expandText">
                    <i class="ri-expand-horizontal-line"></i>
                    扩写
                  </button>
                  <button class="buble-btn boxbtn" @click="extendText">
                    <i class="ri-expand-right-line"></i>
                    续写
                  </button>
                </div>
              </template>
            </el-dropdown>
            <el-dropdown>
              <button class="buble-btn">
                <i class="ri-translate"></i>
                翻译
                <i class="ri-arrow-down-s-line"></i>
              </button>
              <template #dropdown>
                <div>
                  <button class="buble-btn boxbtn" @click="translate('zh')">
                    <i class="ri-translate-2"></i>
                    中文
                  </button>
                  <button class="buble-btn boxbtn" @click="translate('en')">
                    <i class="ri-english-input"></i>
                    英文
                  </button>
                </div>
              </template>
            </el-dropdown>
          </BubbleMenu>
          <BubbleMenu
              class="bubble-menu bm1"
              style="font-size: small"
              :tippy-options="{ duration: 100 }"
              :editor="editor"
              :should-show="props => {
                return props.editor.isActive('image')
            }"
          >
            <button class="buble-btn" @click="OCRImg">
              <i class="ri-character-recognition-line"></i>
              OCR
            </button>
            <button class="buble-btn" @click="formulaImg">
              <i class="ri-formula"></i>
              公式识别
            </button>
          </BubbleMenu>
          <editor-content :editor="editor"/>
        </div>
      </el-main>
    </el-container>
    <AIDialog v-model:visible="AIDialogVisible"
    :AItype="AIType" :from="editorFrom" :to="editorTo"
    :editor="editor" ref="aiDialog"></AIDialog>
    <imgDialog v-model:visible="OCRDialogVisible"
    :imgAIType="imgAIType" :from="editorFrom" :to="editorTo"
    :editor="editor" :dataUrl="imgDialogDataUrl" ref="ocrDialog"></imgDialog>
  </div>
  <input type="file" id="fileInput" style="display: none;" @change="loadFile" accept=".json,application/json"/>
  <input type="file" id="fileInput-Img" style="display: none;" @change="loadFileImg" accept="image/*"/>
  <input type="file" id="fileInput-Audio" style="display: none;" @change="loadFileAudio" accept=".pcm,.wav,.amr,.m4a"/>
  <div class="user-info">
      <span>当前用户: {{ username }}</span>
    </div>
</template>

<script>
import {Color} from '@tiptap/extension-color'
import ListItem from '@tiptap/extension-list-item'
import TextStyle from '@tiptap/extension-text-style'
import Highlight from '@tiptap/extension-highlight'
import TextAlign from '@tiptap/extension-text-align'
import StarterKit from '@tiptap/starter-kit'
import Typography from '@tiptap/extension-typography'
import Underline from '@tiptap/extension-underline'
import Link from '@tiptap/extension-link'
import FileHandler from '@tiptap-pro/extension-file-handler'
import Mathematics from '@tiptap-pro/extension-mathematics'
import Image from '@tiptap/extension-image'
import { getHierarchicalIndexes, TableOfContents } from '@tiptap-pro/extension-table-of-contents'
import {BubbleMenu, Editor, EditorContent, FloatingMenu} from '@tiptap/vue-3'
import EditorButtons from "./EditorButtons.vue";
import Table from '@tiptap/extension-table'
import TableCell from '@tiptap/extension-table-cell'
import TableHeader from '@tiptap/extension-table-header'
import TableRow from '@tiptap/extension-table-row'
import Document from '@tiptap/extension-document'
import Gapcursor from '@tiptap/extension-gapcursor'
import Paragraph from '@tiptap/extension-paragraph'

import {getUserName} from "../api/"

import showdown from 'showdown'

import AIDialog from './AIDialog.vue'
import imgDialog from './imgDialog.vue'

import 'remixicon/fonts/remixicon.css'
import 'katex/dist/katex.min.css'

export default {
  components: {
    AIDialog,
    imgDialog,
    EditorButtons,
    EditorContent,
    BubbleMenu,
    FloatingMenu,
  },
  data() {
    return {
      editor: null,
      AIDialogVisible: false,
      AIType: "缩写",
      OCRDialogVisible: false,
      imgAIType: "OCR",
      editorFrom: 1,
      editorTo: 1,
      imgDialogDataUrl: "",
      mdConverter: new showdown.Converter(),
      username: "unknown"
    }
  },
  mounted() {
    this.editor = new Editor({
      extensions: [
        Link.configure({
          openOnClick: true,
          defaultProtocol: 'https',
        }),
        StarterKit,
        Mathematics,
        Color.configure({ types: [TextStyle.name, ListItem.name] }),
        TextStyle.configure({ types: [ListItem.name] }),
        TextAlign.configure({
          types: ['heading', 'paragraph'],
        }),
        Highlight,
        Typography,
        Underline,
        Image,
        Table.configure({
          resizable: true,
        }),
        TableRow,
        TableHeader,
        TableCell,
        Text,
        TableOfContents.configure({
          getIndex: getHierarchicalIndexes,
          onUpdate: (anchors) => {
            let tocElement = document.getElementById("table-of-contents");
            tocElement.innerHTML = '';

            anchors.forEach((anchor) => {
              const anchorElement = document.createElement('div');
              anchorElement.className = 'content-item';
              // anchorElement.innerHTML = anchor.itemIndex + ". " + anchor.textContent;
              // anchorElement.dataset.id = anchor.id
              anchorElement.dataset.depth = anchor.originalLevel
              // anchorElement.dataset.active = anchor.active
              // anchorElement.dataset.scrolled = anchor.scrolled

              const aElement = document.createElement('a');
              aElement.innerHTML = anchor.itemIndex + ". " + anchor.textContent;
              aElement.href = "#" + anchor.id;
              aElement.style = "color: var(--black)"

              anchorElement.appendChild(aElement);
              tocElement.appendChild(anchorElement);
            })
          }
        }),
        FileHandler.configure({
          allowedMimeTypes: ['image/png', 'image/jpeg', 'image/gif', 'image/webp'],
          onDrop: (currentEditor, files, pos) => {
            files.forEach(file => {
              const fileReader = new FileReader()

              fileReader.readAsDataURL(file)
              fileReader.onload = () => {
                currentEditor.chain().insertContentAt(pos, {
                  type: 'image',
                  attrs: {
                    src: fileReader.result,
                  },
                }).focus().run()
              }
            })
          },
          onPaste: (currentEditor, files, htmlContent) => {
            files.forEach(file => {
              if (htmlContent) {
                // if there is htmlContent, stop manual insertion & let other extensions handle insertion via inputRule
                // you could extract the pasted file from this url string and upload it to a server for example
                console.log(htmlContent) // eslint-disable-line no-console
                return false
              }

              const fileReader = new FileReader()

              fileReader.readAsDataURL(file)
              fileReader.onload = () => {
                currentEditor.chain().insertContentAt(currentEditor.state.selection.anchor, {
                  type: 'image',
                  attrs: {
                    src: fileReader.result,
                  },
                }).focus().run()
              }
            })
          },
        }),
      ],
    })
    let resUserName = getUserName()
    resUserName.then((res)=>{
      if (res.success === false){
        this.username = "未登录"
      }
      else{
        this.username = res.username
      }
    })
  },
  beforeUnmount() {
    this.editor.destroy()
  },
  methods: {
    handleChildEvent(payload) {
      switch(payload) {
        case 'exportJson':{
          const jsonData = this.editor.getJSON()
          const jsonBlob = new Blob([JSON.stringify(jsonData, null, 2)], { type: "application/json" });
          const downloadElem = document.createElement("a");
          const url = URL.createObjectURL(jsonBlob);
          document.body.appendChild(downloadElem);
          downloadElem.href = url;
          downloadElem.download = "doc.json";
          downloadElem.click();
          downloadElem.remove();
          window.URL.revokeObjectURL(url);
        }
          break;
        case 'exportHTML':{
          const htmlData = this.editor.getHTML()
          const htmlBlob = new Blob([htmlData], { type: "text/html" });
          const downloadElem = document.createElement("a");
          const url = URL.createObjectURL(htmlBlob);
          document.body.appendChild(downloadElem);
          downloadElem.href = url;
          downloadElem.download = "doc.html";
          downloadElem.click();
          downloadElem.remove();
          window.URL.revokeObjectURL(url);
        }
          break;
        case 'importJson':{
          const fileInput = document.getElementById("fileInput");
          fileInput.value = "";
          fileInput.click();
        }
          break
        case 'exportMarkdown':{
          const mdText = this.mdConverter.makeMarkdown(this.editor.getHTML())
          const mdBlob = new Blob([mdText], { type: "text/markdown" });
          const downloadElem = document.createElement("a");
          const url = URL.createObjectURL(mdBlob);
          document.body.appendChild(downloadElem);
          downloadElem.href = url;
          downloadElem.download = "doc.md";
          downloadElem.click();
          downloadElem.remove();
          window.URL.revokeObjectURL(url);
        }
          break
        case '润色':
          this.polishText()
          break
        case '缩写':
          this.abbreviateText()
          break
        case '扩写':
          this.expandText()
          break;
        case '续写':
          this.extendText()
          break;
        case '翻译为中文':
          this.translate('zh')
          break;
        case '翻译为英文':
          this.translate('en')
          break
        case 'OCR':
          this.OCRImg()
          break;
        case '公式识别':
          this.formulaImg()
          break;
        case '插入图片':{
          const fileInput = document.getElementById("fileInput-Img");
          fileInput.value = "";
          fileInput.click();
        }
          break
        case '音频转文本':{
          const fileInput = document.getElementById("fileInput-Audio");
          fileInput.value = "";
          fileInput.click();
        }
          break
        default:
          console.log(`Sorry, we are out of ${payload}.`);
      }
    },
    loadFile(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.editor.commands.setContent(JSON.parse(e.target.result))
        };
        reader.readAsText(file);
      }
    },
    loadFileImg(event){
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.editor.chain().insertContent({
            type: 'image',
            attrs: {
              src: e.target.result
            },
          }).focus().run()
        };
        reader.readAsDataURL(file)
      }
    },
    loadFileAudio(event){
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imgAIType = "语音转文字"
          const dataUrl = e.target.result
          if (dataUrl === "") {
            return
          }
          this.imgDialogDataUrl = dataUrl
          this.$nextTick(() => {
            this.showImgDialog()
          })
        };
        reader.readAsDataURL(file)
      }
    },
    polishText() {
      this.AIType = "润色"
      this.$nextTick(() => {
        this.showDialog()
      })
    },
    abbreviateText() {
      this.AIType = "缩写"
      this.$nextTick(() => {
        this.showDialog()
      })
    },
    expandText() {
      this.AIType = "扩写"
      this.$nextTick(() => {
        this.showDialog()
      })
    },
    extendText() {
      this.AIType = "续写"
      this.$nextTick(() => {
        this.showDialog()
      })
    },
    translate(type) {
      if (type === "en"){
        this.AIType = "翻译为英文"
      }
      else{
        this.AIType = "翻译为中文"
      }
      this.$nextTick(() => {
        this.showDialog()
      })
    },
    showDialog() {
      this.AIDialogVisible = true
      const { view, state } = this.editor
      const { from, to } = view.state.selection
      const contents = state.doc.slice(from, to).content;
      this.editor.chain().focus(from).run()
      this.editorFrom = from
      this.editorTo = to
      this.$nextTick(() => {
        this.$refs.aiDialog.setLeftHtml(contents)
        this.$refs.aiDialog.generateText()
      })
    },
    OCRImg() {
      this.imgAIType = "OCR"
      const dataUrl = this.getDataUrl()
      if (dataUrl === "") {
        return
      }
      this.imgDialogDataUrl = dataUrl
      this.$nextTick(() => {
        this.showImgDialog()
      })
    },
    formulaImg() {
      this.imgAIType = "公式识别"
      const dataUrl = this.getDataUrl()
      if (dataUrl === "") {
        return
      }
      this.imgDialogDataUrl = dataUrl
      this.$nextTick(() => {
        this.showImgDialog()
      })
    },
    getDataUrl() {
      const { view, state } = this.editor
      const { from, to } = view.state.selection
      const contents = state.doc.slice(from, to).content;
      if (contents.size !== 1) {
        return ""
      }
      const temp = contents.content[0]
      if (temp.type.name !== "image"){
        return ""
      }
      return temp.attrs.src
    },
    showImgDialog() {
      this.OCRDialogVisible = true
      const { view, state } = this.editor
      const { from, to } = view.state.selection
      this.editor.chain().focus(from).run()
      this.editorFrom = from
      this.editorTo = to
      this.$nextTick(() => {
        this.$refs.ocrDialog.getText()
      })
    }
  },
}
</script>

<style lang="scss">

$control-group-height: 120px;
$title-of-contents-height: 46.8px;

:root {
  --purple-light: #d3c4f3;
  --black: #000000;
  --white: #ffffff;
  --gray-3: #e3e3e3;
  --level: 1;
}

.content-item{
  text-indent: calc((var(--level) - 1) * 1em);
}

.content-item[data-depth="1"]{
  --level: 1;
}

.content-item[data-depth="2"]{
  --level: 2;
}

.content-item[data-depth="3"]{
  --level: 3;
}

.content-item[data-depth="4"]{
  --level: 4;
}

.content-item[data-depth="5"]{
  --level: 5;
}

.content-item[data-depth="6"]{
  --level: 6;
}

/* Basic editor styles */
.tiptap {

  font-synthesis: weight style;

  :first-child {
    margin-top: 0;
  }
  /* List styles */
  ul,
  ol {
    padding: 0 1rem;
    margin: 1.25rem 1rem 1.25rem 0.4rem;

    li p {
      margin-top: 0.25em;
      margin-bottom: 0.25em;
    }
  }

  /* Heading styles */
  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 1.1;
    margin-top: 2.5rem;
    text-wrap: pretty;
  }

  //h1,
  //h2 {
  //  margin-top: 3.5rem;
  //  margin-bottom: 1.5rem;
  //}

  h1 {
    font-size: 1.4rem;
  }

  h2 {
    font-size: 1.2rem;
  }

  h3 {
    font-size: 1.1rem;
  }

  h4,
  h5,
  h6 {
    font-size: 1rem;
  }

  /* Code and preformatted text styles */
  code {
    background-color: var(--purple-light);
    border-radius: 0.4rem;
    color: var(--black);
    font-size: 0.85rem;
    padding: 0.25em 0.3em;
  }

  pre {
    background: var(--black);
    border-radius: 0.5rem;
    color: var(--white);
    font-family: 'JetBrainsMono', monospace;
    margin: 1.5rem 0;
    padding: 0.75rem 1rem;

    code {
      background: none;
      color: inherit;
      font-size: 0.8rem;
      padding: 0;
    }
  }

  blockquote {
    border-left: 3px solid var(--gray-3);
    margin: 1.5rem 0;
    padding-left: 1rem;
  }

  hr {
    // border: solid;
    border-top: 1px solid var(--gray-2);
    margin: 2rem 5%;
  }

  a {
    color: #409EFF;
    cursor: pointer;

    &:hover {
      color: #0080ff;
    }
  }

  img {
    display: block;
    height: auto;
    margin: 1.5rem 0;
    max-width: 100%;

    &.ProseMirror-selectednode {
      outline: 3px solid #409EFF;
    }
  }

  & {
    text-align: left;
    margin: 32px 48px;
  }

  :focus{
    outline: none;
  }

  table {
    border-collapse: collapse;
    margin: 0;
    overflow: hidden;
    table-layout: fixed;
    width: 100%;

    td,
    th {
      border: 1px solid #999999;
      box-sizing: border-box;
      min-width: 1em;
      padding: 6px 8px;
      position: relative;
      vertical-align: top;

      > * {
        margin-bottom: 0;
      }
    }

    th {
      background-color: #E5E5E5;
      font-weight: bold;
      text-align: left;
    }

    .selectedCell:after {
      background: #CCCCCC;
      content: "";
      left: 0; right: 0; top: 0; bottom: 0;
      pointer-events: none;
      position: absolute;
      z-index: -2;
    }

    .column-resize-handle {
      background-color: #409EFF;
      bottom: -2px;
      pointer-events: none;
      position: absolute;
      right: -2px;
      top: 0;
      width: 4px;
    }
  }

  .tableWrapper {
    margin: 1.5rem 0;
    overflow-x: auto;
  }

  &.resize-cursor {
    cursor: ew-resize;
    cursor: col-resize;
  }
}

.ProseMirror-focused {
    outline: none;
}

.el-aside {
  width: 15%;
  padding: 10px 2% 0px;
  text-align: left;
  border-right: solid 1px var(--el-border-color);
}

.el-main {
  padding: 30px 10% 20px;
}

/* Bubble menu */
.bubble-menu {
  background-color: var(--white);
  border: 1px solid var(--gray-1);
  border-radius: 0.7rem;
  box-shadow: var(--shadow);
  display: flex;
  padding: 0.2rem;

  .buble-btn {
    background-color: #f4f4f4;

    &:hover {
      background-color: var(--gray-3);
    }

    &.is-active {
      background-color: #409EFF;

      &:hover {
        background-color: #0080ff;
      }
    }
  }
}

/* Floating menu */
.floating-menu {
  display: flex;
  background-color: var(--gray-3);
  padding: 0.1rem;
  border-radius: 0.5rem;

  button {
    background-color: unset;
    padding: 0.275rem 0.425rem;
    border-radius: 0.3rem;

    &:hover {
      background-color: var(--gray-3);
    }

    &.is-active {
      background-color: var(--white);
      color: var(--purple);

      &:hover {
        color: var(--purple-contrast);
      }
    }
  }
}

.control-group{
  height: $control-group-height;
  min-width: 800px;
}

#app {
  max-width: unset;
  padding:  0;
  height: 100vh;
}

.editor-container {
  border: solid;
  border-radius: 12px;
}

.main-container{
  box-sizing: border-box;
  height: calc(100% - $control-group-height);
  min-width: 800px;
}

.boxbtn{
  display: block;
}

#table-of-contents{
  height: calc(100% - $title-of-contents-height);
  overflow-y: auto;
}

#title-of-contents{
  margin: 0;
  padding-bottom: 18.72px;
  box-sizing: border-box;
  height: $title-of-contents-height;
}

.user-info{
  position: fixed;
  bottom: 0;
  right: 0;
  padding: 10px;
  background-color: #f4f4f4;
  border-radius: 5px;
}
</style>