<template>
  <div class="bg-bg-light-tone-panel dark:bg-bg-dark-tone-panel p-2 rounded-lg shadow-sm">
    <pre  class="hljs p-1 rounded-md break-all grid grid-cols-1">
      <div class="code-container">
        <div 
          class="code-content overflow-x-auto break-all scrollbar-thin scrollbar-track-bg-light-tone scrollbar-thumb-bg-light-tone-panel hover:scrollbar-thumb-primary dark:scrollbar-track-bg-dark-tone dark:scrollbar-thumb-bg-dark-tone-panel dark:hover:scrollbar-thumb-primary active:scrollbar-thumb-secondary"
          v-html="highlightedCode"
          contenteditable="true"
          @input="updateCode"
        ></div>
        </div>

    </pre>    
    <div class="flex flex-row bg-bg-light-tone-panel dark:bg-bg-dark-tone-panel p-2 rounded-lg shadow-sm">
      <span class="text-2xl mr-2">{{ language.trim() }}</span>
      <button @click="copyCode"
              :title="isCopied ? 'Copied!' : 'Copy code'"
              :class="isCopied ? 'bg-green-500' : ''" 
              class="px-2 py-1 mr-2 mb-2 text-left text-sm font-medium rounded-lg hover:bg-primary dark:hover:bg-primary text-white transition-colors duration-200"
              >
        <i data-feather="copy"></i>
      </button>
      <button 
        v-if="['function', 'python', 'sh', 'shell', 'bash', 'cmd', 'powershell', 'latex', 'mermaid', 'graphviz', 'dot', 'javascript', 'html', 'html5', 'svg', 'lilypond'].includes(language)" 
        ref="btn_code_exec" 
        @click="executeCode"  
        title="execute"
        class="execute-button px-2 py-1 mr-2 mb-2 text-left text-sm font-medium rounded-lg hover:bg-primary dark:hover:bg-primary text-white transition-colors duration-200"
        :class="isExecuting ? 'bg-green-500' : ''"
      >
        <i data-feather="play-circle"></i>
      </button>      
      <button 
        v-if="['airplay', 'mermaid', 'graphviz', 'dot', 'javascript', 'html', 'html5', 'svg', 'css'].includes(language.trim())" 
        ref="btn_code_exec_in_new_tab" 
        @click="executeCode_in_new_tab"  
        title="execute"
        class="execute-button px-2 py-1 mr-2 mb-2 text-left text-sm font-medium rounded-lg hover:bg-primary dark:hover:bg-primary text-white transition-colors duration-200"
        :class="isExecuting ? 'bg-green-500' : ''"
      >
        <i data-feather="airplay"></i>
      </button>
      <button @click="openFolder"  title="open code project folder"
      class="px-2 py-1 mr-2 mb-2 text-left text-sm font-medium rounded-lg hover:bg-primary dark:hover:bg-primary text-white transition-colors duration-200"
      >
        <i data-feather="folder"></i>
      </button>
      <button v-if="['python', 'latex', 'html'].includes(language.trim())" @click="openFolderVsCode"  title="open code project folder in vscode"
      class="px-2 py-1 mr-2 mb-2 text-left text-sm font-medium rounded-lg hover:bg-primary dark:hover:bg-primary text-white transition-colors duration-200"
      >
        <img src="@/assets/vscode_black.svg" width="25" height="25">
      </button>
      <button v-if="['python', 'latex', 'html'].includes(language.trim())" @click="openVsCode"  title="open code in vscode"
      class="px-2 py-1 mr-2 mb-2 text-left text-sm font-medium rounded-lg hover:bg-primary dark:hover:bg-primary text-white transition-colors duration-200"
      >
        <img src="@/assets/vscode.svg" width="25" height="25">
      </button>
    </div>
    <span v-if="executionOutput" class="text-2xl">Execution output</span>
    <pre  class="hljs mt-0 p-1 rounded-md break-all grid grid-cols-1" v-if="executionOutput">
      <div class="container h-[200px] overflow-x-auto break-all scrollbar-thin scrollbar-track-bg-light-tone scrollbar-thumb-bg-light-tone-panel hover:scrollbar-thumb-primary dark:scrollbar-track-bg-dark-tone dark:scrollbar-thumb-bg-dark-tone-panel dark:hover:scrollbar-thumb-primary active:scrollbar-thumb-secondary">
        <div ref="execution_output" class="w-full h-full overflow-y-auto scrollbar-thin scrollbar-track-bg-light-tone scrollbar-thumb-bg-light-tone-panel hover:scrollbar-thumb-primary dark:scrollbar-track-bg-dark-tone dark:scrollbar-thumb-bg-dark-tone-panel dark:hover:scrollbar-thumb-primary active:scrollbar-thumb-secondary" v-html="executionOutput"></div>
      </div>
    </pre>    

</div>
</template>
<script>
import { nextTick } from 'vue'
import hljs from 'highlight.js'
import feather from 'feather-icons';
import 'highlight.js/styles/tomorrow-night-blue.css';
import 'highlight.js/styles/tokyo-night-dark.css';

hljs.configure({ languages: [] }); // Reset languages
hljs.configure({ languages: ['bash'] }); // Set bash as the default language

hljs.highlightAll();
export default {
  props: {
    host: {
      type: String,
      required: false,
      default: "http://localhost:9600",
    },
    language: {
      type: String,
      required: true,
    },
    client_id: {
      type: String,
      required: true,
    },
    code: {
      type: String,
      required: true,
    },
    discussion_id: {
      type: [String, Number],
      required: true,
    },
    message_id: {
      type: [String, Number],
      required: true,
    },
  },
  data() {
    return {
      isExecuting:false,
      isCopied: false,
      executionOutput: '',  // new property
    };
  },
  mounted() {
    nextTick(() => {
          feather.replace()
    })
  },
  computed: {
    highlightedCode() {
      let validLanguage;
      if (this.language === 'vue' || this.language === 'vue.js') {
        validLanguage = 'javascript';
      } else 
      if (this.language === 'function') {
        validLanguage = 'json';
      } else {
        validLanguage = hljs.getLanguage(this.language) ? this.language : 'plaintext';
      }
      const trimmedCode = this.code.trim(); // Remove leading and trailing whitespace
      const lines = trimmedCode.split('\n');
      const lineNumberWidth = lines.length.toString().length;
      const lineNumbers = lines.map((line, index) => {
        const lineNumber = index + 1;
        return lineNumber.toString().padStart(lineNumberWidth, ' ');
      });
      const lineNumbersContainer = document.createElement('div');
      lineNumbersContainer.classList.add('line-numbers');
      lineNumbersContainer.innerHTML = lineNumbers.join('<br>');
      const codeContainer = document.createElement('div');
      codeContainer.classList.add('code-container');
      const codeContent = document.createElement('pre');
      const codeContentCode = document.createElement('code');
      codeContentCode.classList.add('code-content');
      codeContentCode.innerHTML = hljs.highlight(trimmedCode,  {language: validLanguage, ignoreIllegals: true }).value;
      codeContent.appendChild(codeContentCode);
      codeContainer.appendChild(lineNumbersContainer);
      codeContainer.appendChild(codeContent);
      return codeContainer.outerHTML;
    }


  },
  methods: {
    copyCode() {
      this.isCopied = true;
      console.log("Copying code")
      const el = document.createElement('textarea');
      el.value = this.code;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      nextTick(() => {
          feather.replace()
      })
    },
    executeCode() {
      this.isExecuting=true;
      nextTick(() => {
        feather.replace()
      })

      const json = JSON.stringify({
                                    'client_id': this.client_id, 
                                    'code': this.code, 
                                    'discussion_id': this.discussion_id?this.discussion_id:0, 
                                    'message_id': this.message_id?this.message_id:0, 
                                    'language': this.language
                                  })   
      console.log(json)     
      fetch(`${this.host}/execute_code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: json
      }).then(response=>{
        this.isExecuting=false;
        // Parse the JSON data from the response body
        return response.json();
      })
      .then(jsonData => {
        // Now you can work with the JSON data
        console.log(jsonData);
        this.executionOutput = jsonData.output;
      })
      .catch(error => {
        this.isExecuting=false;
        // Handle any errors that occurred during the fetch process
        console.error('Fetch error:', error);
      });
    },
    executeCode_in_new_tab(){
      this.isExecuting=true;
      nextTick(() => {
        feather.replace()
      })      
      const json = JSON.stringify({
                                    'client_id': this.client_id, 
                                    'code': this.code, 
                                    'discussion_id': this.discussion_id, 
                                    'message_id': this.message_id, 
                                    'language': this.language
                                  })   
      console.log(json)     
      fetch(`${this.host}/execute_code_in_new_tab`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: json
      }).then(response=>{
        console.log("done")
        this.isExecuting=false;
        // Parse the JSON data from the response body
        return response.json();
      })
      .then(jsonData => {
        // Now you can work with the JSON data
        console.log("done2")
        console.log(jsonData);
        this.executionOutput = jsonData.output;
      })
      .catch(error => {
        this.isExecuting=false;
        // Handle any errors that occurred during the fetch process
        console.error('Fetch error:', error);
      });
    },
    openFolderVsCode(){
      const json = JSON.stringify({
                                      'client_id': this.client_id, 
                                      'code': this.code, 
                                      'discussion_id': this.discussion_id, 
                                      'message_id': this.message_id
                                    })   
      console.log(json)     
      fetch(`${this.host}/open_discussion_folder_in_vs_code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: json
      }).then(response=>{
        // Parse the JSON data from the response body
        return response.json();
      })
      .then(jsonData => {
        // Now you can work with the JSON data
        console.log(jsonData);
      })
      .catch(error => {
        // Handle any errors that occurred during the fetch process
        console.error('Fetch error:', error);
      });      
    },
    openVsCode() {
      const json = JSON.stringify({ 
                          'client_id': this.client_id, 
                          'discussion_id': typeof this.discussion_id === 'string' ? parseInt(this.discussion_id) : this.discussion_id , 
                          'message_id': this.message_id,
                          'code': this.code
                          })   
      console.log(json)     
      fetch(`${this.host}/open_code_in_vs_code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: json
      }).then(response=>{
        // Parse the JSON data from the response body
        return response.json();
      })
      .then(jsonData => {
        // Now you can work with the JSON data
        console.log(jsonData);
      })
      .catch(error => {
        // Handle any errors that occurred during the fetch process
        console.error('Fetch error:', error);
      });
    },
    openFolder() {
      const json = JSON.stringify({ 'client_id': this.client_id, 'discussion_id': this.discussion_id })   
      console.log(json)     
      fetch(`${this.host}/open_discussion_folder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: json
      }).then(response=>{
        // Parse the JSON data from the response body
        return response.json();
      })
      .then(jsonData => {
        // Now you can work with the JSON data
        console.log(jsonData);
      })
      .catch(error => {
        // Handle any errors that occurred during the fetch process
        console.error('Fetch error:', error);
      });
    },
  },
};
</script>
<style>
.code-container {
  display: flex;
  margin: 0; /* Remove the default margin */
}
.line-numbers {
  flex-shrink: 0;
  padding-right: 5px; /* Adjust the padding as needed */
  color: #999;
  user-select: none; /* Prevent line numbers from being selected */
  white-space: nowrap; /* Prevent line numbers from wrapping */
  margin: 0; /* Remove the default margin */
}
.code-content {
  flex-grow: 1;
  margin: 0; /* Remove the default margin */
  outline: none; /* Remove the default focus outline */
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.execute-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>