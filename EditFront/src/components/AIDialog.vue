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
import Mathematics from '@tiptap-pro/extension-mathematics'
import Image from '@tiptap/extension-image'
import {Editor, EditorContent} from '@tiptap/vue-3'
import Table from '@tiptap/extension-table'
import TableCell from '@tiptap/extension-table-cell'
import TableHeader from '@tiptap/extension-table-header'
import TableRow from '@tiptap/extension-table-row'
import Document from '@tiptap/extension-document'
import Gapcursor from '@tiptap/extension-gapcursor'
import Paragraph from '@tiptap/extension-paragraph'

import { DOMSerializer } from 'prosemirror-model'
import showdown from 'showdown'

import {getPolish, getAbbreviate, getExpand, getExtend, getTranslate} from "../api/";

import 'remixicon/fonts/remixicon.css'

export default {
  components: {
    EditorContent,
  },
  data(){
    return {
      command:"润色",
      editorLeft:null,
      editorRight:null,
      isRunning:false,
      functionMap:{
        "润色":getPolish,
        "缩写":getAbbreviate,
        "扩写":getExpand,
        "续写":getExtend,
      },
      mdConverter: new showdown.Converter(),
    }
  },
  mounted() {
    this.editorLeft = new Editor({
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
      ],
      editable: false,
    })
    this.editorRight = new Editor({
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
      ],
    })
  },
  beforeUnmount() {
    this.editorLeft.destroy()
    this.editorRight.destroy()
  },
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    AItype: {
      type: String,
      required: true,
    },
    editor: {
      type: Object,
      required: true,
    },
    from: {
      type: Number,
      required: true
    },
    to: {
      type: Number,
      required: true
    }
  },
  methods: {
    handleClose(done) {
      this.isRunning=false
      this.$emit('update:visible', false);
      done()
    },
    handleCancel() {
      this.$emit('update:visible', false);
    },
    handleConfirm() {
      let from = this.from - 1
      let to = this.to
      if (this.AItype === "续写"){
        this.editor.chain().insertContentAt(to, this.editorRight.getHTML()).run();
      }
      else{
        this.editor.chain().insertContentAt({from, to}, this.editorRight.getHTML()).run();
      }
      this.$emit('update:visible', false);
    },
    setLeftHtml(contents) {
      const { view, state } = this.editor
      const serializer = DOMSerializer.fromSchema(state.schema)
      // 创建一个临时的 div 元素来存放序列化的 HTML
      const tempDiv = document.createElement('div')
      // 将片段中的内容序列化为 HTML 并添加到临时 div 中
      tempDiv.appendChild(serializer.serializeFragment(contents))
      // 获取临时 div 中的 HTML 内容
      tempDiv.querySelectorAll('img').forEach(node => {
        node.remove();
      });
      tempDiv.querySelectorAll('[id]').forEach(node => {
        node.removeAttribute('id')
      })
      tempDiv.querySelectorAll('[data-toc-id]').forEach(node => {
        node.removeAttribute('data-toc-id')
      })
      const htmlContent = tempDiv.innerHTML
      tempDiv.remove()
      this.editorLeft.chain().clearContent().insertContent(htmlContent).run();
    },
    stopRunning() {
      this.editorRight.setEditable(true);
      this.isRunning=false;
    },
    getRunning() {
      return this.isRunning;
    },
    getTextNodes(node) {
      let nodesWithText = [];
      if (node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() !== '') {
        nodesWithText.push(node);
      } else {
        for (let child of node.childNodes) {
          nodesWithText = nodesWithText.concat(this.getTextNodes(child));
        }
      }
      return nodesWithText;
    },
    async transLateText() {
      this.editorRight.setEditable(false);
      this.isRunning=true;
      this.editorRight.chain().clearContent().run();

      try{
        let htmlStr = this.editorLeft.getHTML()
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlStr, 'text/html');
        const body = doc.body;
        const textNodes = this.getTextNodes(body);

        let to = ""

        if (this.AItype.endsWith("中文")){
          to = 'zh'
        }
        else if(this.AItype.endsWith("英文")){
          to = 'en'
        }
        else{
          throw new Error("找不到目标语言")
        }

        let textToTranslate = ""
        textNodes.forEach((node) => {
          textToTranslate += node.nodeValue + '\n';
        });
        let temp = await getTranslate(textToTranslate, to)
        textNodes.forEach((node, index) => {
          node.nodeValue = temp.string[index];
        });
        this.editorRight.chain().focus().clearContent().insertContent(body.innerHTML).run();
        this.stopRunning()
      }
      catch (error){
        this.stopRunning()
      }
    },
    generateText() {
      // 确保编辑器中有文本
      if (this.editorLeft.state.empty){
        return;
      }

      // 如果是翻译任务，从在这里执行，不执行后续逻辑，翻译任务api不同
      if (this.AItype.startsWith("翻译")){
        this.transLateText()
        return;
      }

      this.editorRight.setEditable(false);
      this.isRunning=true;
      this.editorRight.chain().clearContent().run();

      const text = this.mdConverter.makeMarkdown(this.editorLeft.getHTML())

      const dealF = this.functionMap[this.AItype];

      let response = dealF("test","test",text);
      response.then(
          res => {
              const reader = res.body.getReader();
              const decoder = new TextDecoder();
              const editor = this.editorRight;
              const sr     = this.stopRunning;
              const gr     = this.getRunning;
              let text = "";
              const mdConverter = this.mdConverter;
              
              function read() {
                  reader.read().then(({ done, value }) => {
                      if (done) {
                        sr()
                        return; 
                      }
                      if (gr() === false) {
                        return;
                      }
                      const chunk = decoder.decode(value, { stream: true });
                      text = text + chunk;
                      text = text.replaceAll("$$","$")
                      editor.chain().focus().clearContent().insertContent(mdConverter.makeHtml(text)).run();
                      console.log(mdConverter.makeHtml(text))
                      read();
                  });
              }
              read();
          }
      ).catch(error => {
          console.error('Error:', error);
          this.stopRunning()
      });
    }
}
}
</script>

<template>
    <el-dialog
    :model-value="visible"
    width="70%"
    :destroy-on-close=true
    :draggable=true
    :overflow=true
    :before-close="handleClose">
    <div id="mainDiv">
      <div id="divideDiv">
        <div class="dialogCol" id="leftDiv">
          <div class="miniHeader">原文：</div>
          <div class="textDiv" v-if="editorLeft">
            <editor-content class="tiptapDiv" :editor="editorLeft"/>
          </div>
        </div>
        <div id="arrowDiv">
          <el-button id="arrowBtn" size="large" title="重新生成" :disabled="isRunning" @click="generateText()" plain >
            <i :class="['ri-arrow-right-double-fill', { 'gradient-text': isRunning }]" style="font-size: 45px;"></i>
          </el-button>
        </div>
        <div class="dialogCol" id="rightDiv">
          <div class="miniHeader">{{AItype}}后：</div>
          <div class="textDiv" v-if="editorRight">
            <editor-content class="tiptapDiv" :editor="editorRight"/>
          </div>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
          <el-button @click="handleCancel()">取 消</el-button>
          <el-button type="primary" @click="handleConfirm()" :disabled="isRunning">接 受</el-button>
      </span>
    </div>
    </el-dialog>
</template>

<style lang="scss" scoped>
  #mainDiv{
    height:65vh;
    flex-direction: column;
    padding-left: 10px;
    padding-right: 10px;
  }
  #divideDiv{
    display: grid;
    height: calc(100% - 32px);
    grid-template-columns: 48% 4% 48%;
    grid-template-rows: 100%;
    box-sizing: border-box;
    padding-bottom: 20px;
  }
  #arrowDiv{
    display: flex;
    justify-content: center;
    align-items: center;
  }
  #arrow{
    height: 14px;
  }
  .dialogCol{
    text-align: left;
    box-sizing: border-box;
    max-height: 100%;
    padding: 10px 20px;
  }
  .miniHeader{
    font-size: 20px;
  }
  .textDiv{
    height: calc(100% - 30px);
    position: relative;
    width: 100%;
    border-radius: 6px;
    border: solid 2px black;
    overflow: auto; /* 隐藏溢出内容，防止影响布局 */
  }
  #arrowBtn{
    border-color: white;
    outline: white none;
    padding: 0 0;
  }
  .gradient-text{
    background-image: linear-gradient(to right, rgb(232, 255, 252), #409EFF, rgb(232, 255, 252));
    /* 将文字与背景分离，以显示渐变效果 */
    -webkit-background-clip: text;
    background-clip: text;
    /* 使用透明色将文字颜色设置为透明 */
    color: transparent;
    background-size: 200% 100%;
    animation: gradientMove 3s linear infinite;
  }
  @keyframes gradientMove {
    0% {
      background-position: 100% 0;
    }
    100% {
      background-position: -100% 0;
    }
  }
</style>

<style lang="scss">
  .el-dialog{
    border-radius: 12px;
  }
  .tiptapDiv > .tiptap{
    margin-top: 16px;
    margin-bottom: 16px;
    margin-left: 24px;
    margin-right: 24px;
  }
</style>