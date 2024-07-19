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

import {getOCR, getFormula, getASR} from "../api/";

import 'remixicon/fonts/remixicon.css'

export default {
  components: {
    EditorContent,
  },
  data(){
    return {
      command:"OCR",
      editor2show:null,
      isRunning:false,
      functionMap:{
        "OCR":getOCR,
        "公式识别":getFormula,
        "语音转文字":getASR
      },
    }
  },
  mounted() {
    this.editor2show = new Editor({
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
    this.editor2show.destroy()
  },
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    imgAIType: {
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
    },
    dataUrl: {
      type: String,
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
      let from = this.from
      let to = this.to
      if (from !== to){
        this.editor.chain().insertContentAt({from, to}, this.editor2show.getHTML()).run();
      }
      else{
        this.editor.chain().insertContentAt(from, this.editor2show.getHTML()).run();
      }
      this.$emit('update:visible', false);
    },
    stopRunning() {
      this.editor2show.setEditable(true);
      this.isRunning=false;
    },
    getRunning() {
      return this.isRunning;
    },
    getText() {
      this.editor2show.chain().clearContent().run();
      const f = this.functionMap[this.imgAIType]
      this.isRunning = true
      this.editor2show.setEditable(false);
      let rep = f(this.dataUrl)
      rep.then(res => {
        this.editor2show.chain().insertContentAt(1, res.string).run();
        this.stopRunning()
      })
    }
  }
}
</script>

<template>
    <el-dialog
    :model-value="visible"
    width="35%"
    :destroy-on-close=true
    :draggable=true
    :overflow=true
    :before-close="handleClose">
    <div id="mainDiv">
      <div class="textDiv" v-if="editor2show">
        <editor-content class="tiptapDiv2" :editor="editor2show"/>
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
    height:35vh;
    flex-direction: column;
    padding-left: 10px;
    padding-right: 10px;
  }
  .textDiv{
    height: calc(100% - 50px);
    position: relative;
    width: 100%;
    border-radius: 6px;
    border: solid 2px black;
    overflow: auto; /* 隐藏溢出内容，防止影响布局 */
    margin-bottom: 20px;
  }
</style>

<style lang="scss">
  .el-dialog{
    border-radius: 12px;
  }
  .tiptapDiv2 > .tiptap{
    margin-top: 16px;
    margin-bottom: 16px;
    margin-left: 24px;
    margin-right: 24px;
  }
</style>