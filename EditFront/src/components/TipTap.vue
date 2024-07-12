<template>
  <div v-if="editor" class="common-layout" style="width: 100vw; height: 100vh;display: flex;flex-direction: column;">
    <div class="control-group">
      <EditorButtons :editor="editor" />
    </div>
    <el-container style="flex:1;height: 95%">
      <el-aside style="height: 100%;">
        <h3 style="margin-top: 0;">大纲</h3>
        <div id="table-of-contents" style="height: 90%; overflow-y: auto;"/>
      </el-aside>
      <el-main style="height: 100%; overflow-y: auto;">
        <div class="editor-container">
          <bubble-menu
            class="bubble-menu"
            style="font-size: small"
            :tippy-options="{ duration: 100}"
            :editor="editor"
          >
            <button @click="polishText">
              <i class="ri-magic-line"></i>
              润色
            </button>
            <button @click="abbreviateText">
              <i class="ri-collapse-horizontal-line"></i>
              缩写
            </button>
            <button @click="expandText">
              <i class="ri-expand-horizontal-line"></i>
              扩写
            </button>
            <button @click="extendText">
              <i class="ri-expand-right-line"></i>
              续写
            </button>
            <button @click="OCRImage">
              <i class="ri-character-recognition-line"></i>
              OCR
            </button>
            <button @click="describeImage">
              <i class="ri-file-image-line"></i>
              图片描述
            </button>
            <button @click="detectObject">
              <i class="ri-file-image-fill"></i>
              目标检测
            </button>
            <button @click="recognizeAudio">
              <i class="ri-mist-line"></i>
              语音识别
            </button>
            <button @click="summarizeVideo">
              <i class="ri-sidebar-unfold-fill"></i>
              视频总结
            </button>
            <button @click="generateImage">
              <i class="ri-remixicon-line"></i>
              图片生成
            </button>
          </bubble-menu>
          <floating-menu
            class="floating-menu"
            :tippy-options="{ duration: 100 }"
            :editor="editor"
          >
            <button @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }">
              H1
            </button>
            <button @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }">
              H2
            </button>
            <button @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
              Bullet list
            </button>
          </floating-menu>
          <editor-content :editor="editor"/>
        </div>
      </el-main>
    </el-container>
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
import {BubbleMenu, Editor, EditorContent, FloatingMenu, generateText,} from '@tiptap/vue-3'
import EditorButtons from "./EditorButtons.vue";

import {getPolish, getAbbreviate, getExpand, getExtend, getOCR, getDecribe, getObjectDetection, getAudioRecognition, getVideoSummary, getImageGeneration} from "../api/";

import 'remixicon/fonts/remixicon.css'
import 'katex/dist/katex.min.css'
import { getActivePinia } from 'pinia'

export default {
  components: {
    EditorButtons,
    EditorContent,
    BubbleMenu,
    FloatingMenu,
  },

  data() {
    return {
      editor: null,
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
        TableOfContents.configure({
          getIndex: getHierarchicalIndexes,
          onUpdate: (anchors) => {
            let tocElement = document.getElementById("table-of-contents");
            tocElement.innerHTML = '';
            console.log(anchors)

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
  },

  beforeUnmount() {
    this.editor.destroy()
  },

  methods: {
    polishText() {
      // 确保编辑器有选中的文本
      if (!this.editor.state.selection.empty) {
        this.editor.setEditable(false);

        const { view, state } = this.editor
        const { from, to } = view.state.selection

        const text = state.doc.textBetween(from, to, '');

        let response = getPolish("test","test",text);
        console.log(response);
        console.log(from);
        response.then(
            res => {
              const newText = res?.answer;
              if (newText) {
                this.editor.chain().focus().insertContentAt({from, to}, newText).run();
              }
              this.editor.setEditable(true);
            }
        )
      }
    },
    abbreviateText() {
      // 确保编辑器有选中的文本
      if (!this.editor.state.selection.empty) {
        this.editor.setEditable(false);

        const { view, state } = this.editor
        const { from, to } = view.state.selection

        const text = state.doc.textBetween(from, to, '');

        let response = getAbbreviate("test","test",text);
        console.log(response);
        console.log(from);
        response.then(
            res => {
              const newText = res?.answer;
              if (newText) {
                this.editor.chain().focus().insertContentAt({from, to}, newText).run();
              }
              this.editor.setEditable(true);
            }
        )
      }
    },
    expandText() {
      // 确保编辑器有选中的文本
      if (!this.editor.state.selection.empty) {
        this.editor.setEditable(false);

        const { view, state } = this.editor
        const { from, to } = view.state.selection

        const text = state.doc.textBetween(from, to, '');

        let response = getExpand("test","test",text);
        console.log(response);
        console.log(from);
        response.then(
            res => {
              const newText = res?.answer;
              if (newText) {
                this.editor.chain().focus().insertContentAt({from, to}, newText).run();
              }
              this.editor.setEditable(true);
            }
        )
      }
    },
    extendText() {
      // 确保编辑器有选中的文本
      if (!this.editor.state.selection.empty) {
        this.editor.setEditable(false);

        const { view, state } = this.editor
        const { from, to } = view.state.selection

        const text = state.doc.textBetween(from, to, '');

        let response = getExtend("test","test",text);
        console.log(response);
        console.log(from);
        response.then(
            res => {
              const newText = res?.answer;
              if (newText) {
                this.editor.chain().focus().insertContentAt(to, newText).run();
              }
              this.editor.setEditable(true);
            }
        )
      }
    },
  OCRImage() {
  // 确保编辑器有选中的对象
      if (this.editor.state.selection.empty) {
        console.log("没有选中任何内容");
        return;
      }

      this.editor.setEditable(false);

      const { view, state } = this.editor;
      const { from, to } = view.state.selection;

      // 在选中范围内查找图片节点并获取其 dataURL
      let imageDataURL = null;
      state.doc.nodesBetween(from, to, (node, pos) => {
        if (node.type.name === 'image') {
          imageDataURL = node.attrs.src;
          return false; // 停止遍历
        }
      });

      if (!imageDataURL) {
        console.log("没有找到选中的图片");
        this.editor.setEditable(true);
        return;
      }

      // 发送 dataURL 到后端进行 OCR 处理
      getOCR("test", "test", imageDataURL)
        .then(res => {
          console.log(res);
          console.log(from);
          const newText = res;
          if (newText) {
            // 在选中区域后插入 OCR 结果
            this.editor.chain().focus().insertContentAt(to, newText).run();
          } else {
            console.log("OCR 未返回有效文本");
          }
        })
        .catch(error => {
          console.error("OCR 处理过程中出错:", error);
        })
        .finally(() => {
          this.editor.setEditable(true);
        });
    },

    describeImage() {
  // 确保编辑器有选中的对象
      if (this.editor.state.selection.empty) {
        console.log("没有选中任何内容");
        return;
      }

      this.editor.setEditable(false);

      const { view, state } = this.editor;
      const { from, to } = view.state.selection;

      // 在选中范围内查找图片节点并获取其 dataURL
      let imageDataURL = null;
      state.doc.nodesBetween(from, to, (node, pos) => {
        if (node.type.name === 'image') {
          imageDataURL = node.attrs.src;
          return false; // 停止遍历
        }
      });

      if (!imageDataURL) {
        console.log("没有找到选中的图片");
        this.editor.setEditable(true);
        return;
      }

      getDecribe("test", "test", imageDataURL)
        .then(res => {
          console.log(res);
          console.log(from);
          const newText = res;
          if (newText) {
            this.editor.chain().focus().insertContentAt(to, newText).run();
          } else {
            console.log("Describe 未返回有效文本");
          }
        })
        .catch(error => {
          console.error("Describe 处理过程中出错:", error);
        })
        .finally(() => {
          this.editor.setEditable(true);
        });
    },

  //   describeImage() {
  // // 确保编辑器有选中的对象（这里假设是图片）
  //     if (!this.editor.state.selection.empty) {
  //       this.editor.setEditable(false);

  //       const { view, state } = this.editor;
  //       const { from, to } = view.state.selection;


  //       // 获取选中图片的 dataURL
  //       getSelectedImageDataURL(this.editor).then(dataURL => {
  //         // 发送 dataURL 到后端进行 describe 处理
  //         let response = getDescribe("test","test",dataURL); 

  //         response.then(res => {
  //           const newText = res?.answer;
  //           if (newText) {
  //             this.editor.chain().focus().insertContent(to, newText).run();
  //           }
  //           this.editor.setEditable(true);
  //         }).catch(error => {
  //           // 处理错误
  //           console.error(error);
  //           this.editor.setEditable(true);
  //         });
  //       }).catch(error => {
  //         // 处理获取 dataURL 时的错误
  //         console.error(error);
  //         this.editor.setEditable(true);
  //       });
  //     }
  //   },
    detectObject() {
  // 确保编辑器有选中的对象（这里假设是图片）
      if (!this.editor.state.selection.empty) {
        this.editor.setEditable(false);

        const { view, state } = this.editor;
        const { from, to } = view.state.selection;


        // 获取选中图片的 dataURL
        getSelectedImageDataURL(this.editor).then(dataURL => {
          // 发送 dataURL 到后端进行 describe 处理
          let response = getObjectDetection("test","test",dataURL); 

          response.then(res => {
            const newText = res?.answer;
            if (newText) {
              this.editor.chain().focus().insertContent(to, newText).run();
            }
            this.editor.setEditable(true);
          }).catch(error => {
            // 处理错误
            console.error(error);
            this.editor.setEditable(true);
          });
        }).catch(error => {
          // 处理获取 dataURL 时的错误
          console.error(error);
          this.editor.setEditable(true);
        });
      }
    },
    recognizeAudio() {
  // 确保编辑器有选中的对象（这里假设是图片）
      if (!this.editor.state.selection.empty) {
        this.editor.setEditable(false);

        const { view, state } = this.editor;
        const { from, to } = view.state.selection;


        // 获取选中图片的 dataURL
        getSelectedImageDataURL(this.editor).then(dataURL => {
          // 发送 dataURL 到后端进行 describe 处理
          let response = getAudioRecognition("test","test",dataURL); 

          response.then(res => {
            const newText = res?.answer;
            if (newText) {
              this.editor.chain().focus().insertContent(to, newText).run();
            }
            this.editor.setEditable(true);
          }).catch(error => {
            // 处理错误
            console.error(error);
            this.editor.setEditable(true);
          });
        }).catch(error => {
          // 处理获取 dataURL 时的错误
          console.error(error);
          this.editor.setEditable(true);
        });
      }
    },
    summarizeVideo() {
  // 确保编辑器有选中的对象（这里假设是图片）
      if (!this.editor.state.selection.empty) {
        this.editor.setEditable(false);

        const { view, state } = this.editor;
        const { from, to } = view.state.selection;


        // 获取选中图片的 dataURL
        getSelectedImageDataURL(this.editor).then(dataURL => {
          // 发送 dataURL 到后端进行 describe 处理
          let response = getVideoSummary("test","test",dataURL); 

          response.then(res => {
            const newText = res?.answer;
            if (newText) {
              this.editor.chain().focus().insertContent(to, newText).run();
            }
            this.editor.setEditable(true);
          }).catch(error => {
            // 处理错误
            console.error(error);
            this.editor.setEditable(true);
          });
        }).catch(error => {
          // 处理获取 dataURL 时的错误
          console.error(error);
          this.editor.setEditable(true);
        });
      }
    },
    generateImage() {
      // 确保编辑器有选中的文本
      if (!this.editor.state.selection.empty) {
        this.editor.setEditable(false);

        const { view, state } = this.editor
        const { from, to } = view.state.selection

        const text = state.doc.textBetween(from, to, '');

        let response = getImageGeneration("test","test",text);
        console.log(response);
        console.log(from);
        response.then(
            res => {
              const newText = res?.answer;
              if (newText) {
                this.editor.chain().focus().insertContentAt(to, newText).run();
              }
              this.editor.setEditable(true);
            }
        )
      }
    },
  }
}
</script>

<style lang="scss">
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

  text-align: left;
  margin-top: 1.5em;
  margin-bottom: 1.5em;
  margin-left: 2em;
  margin-right: 2em;

  :focus{
    outline: none;
  }
}

.ProseMirror-focused {
    outline: none;
}

.el-aside {
  width: 15%;
  padding-left: 2%;
  padding-right: 2%;
  padding-top: 10px;
  padding-bottom: 0px;
  background-color: azure;
  text-align: left;
}

.el-main {
  padding-left: 10%;
  padding-right: 10%;
  padding-top: 10px;
  padding-bottom: 0;
  background-color: aquamarine;
}

/* Bubble menu */
.bubble-menu {
  background-color: var(--white);
  border: 1px solid var(--gray-1);
  border-radius: 0.7rem;
  box-shadow: var(--shadow);
  display: flex;
  padding: 0.2rem;

  button {
    background-color: unset;

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
  background-color: #e3e3e3;
}

#app {
  max-width: unset;
  padding:  0;
  height: 100vh;
}

.editor-container {
  border: solid;
}
</style>