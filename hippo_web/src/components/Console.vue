<template>
  <div class="console">
    <div class="console_header">
      <div class="info">
        {{host_info.hostname}} | {{host_info.username}}@{{host_info.ip_addr}}:{{host_info.port}}
      </div>
      <div class="file_part">
        <button type="button" class="ant-btn ant-btn-primary" @click="showDrawer">
          <a-icon type="folder-open"/>
          文件管理器
        </button>
      </div>
    </div>

    <div class="file_show">

      <div>

        <a-drawer
          title="文件管理器"
          :width="900"
          :visible="visible"
          :body-style="{ paddingBottom: '80px' }"
          @close="onClose"
        >
          <div class="file_nav">
            <div>
              <a-breadcrumb>
                <a-breadcrumb-item>
                  <a-icon @click="back_folder('/',1)" type="home"/>
                </a-breadcrumb-item>

                <a-breadcrumb-item v-for="(folder_path,f_index) in path" :key="f_index" v-show="folder_path!=='/'">
                  <span style="cursor: pointer;" @click="back_folder(folder_path,f_index)">{{folder_path}}</span>
                </a-breadcrumb-item>
              </a-breadcrumb>
            </div>
            <div style="display: flex; align-items: center;">
              <span>显示隐藏文件：</span>
              <a-switch @change="switch_on_off" checked-children="开" un-checked-children="关"/>
              <div style="margin-left: 10px">
                <a-upload
                  name="file"
                  :multiple="true"
                  :action="visit_url+'?folder_path=' + folder_path_str"
                  :headers="headers"
                  @change="handleChange"
                >
                  <a-button type="primary">
                    <a-icon type="upload"/>
                    上传文件
                  </a-button>
                </a-upload>
              </div>

            </div>


          </div>
          <div>
            <a-table
              :columns="columns"
              :data-source="data"
              :pagination="false"
              :scroll="{ y: 400 }"
            >

              <a slot="name" slot-scope="text,record"> <!-- record表示该条记录，是个字典 -->
                <span @click="join_folder(text)" v-if="record.file_attr.substr(0,1)==='d'">
                  <a-icon type="folder"/>

                {{ text }}
                </span>
                <span v-else>
                  <a-popconfirm placement="top" ok-text="下载" cancel-text="取消" @confirm="confirm(text)">
                    <template slot="title">
                      <p>确认下载该文件吗？</p>
                      <p>{{ text }}</p>
                    </template>

                      <a-icon type="file"/>
                      {{ text }}

                  </a-popconfirm>

<!--                  <a-popconfirm title="Are you sure？">-->
<!--                    <a-icon slot="icon" type="question-circle-o" style="color: red"/>-->
<!--                    <a href="#">{{text}}</a>-->
<!--                  </a-popconfirm>-->

<!--                  <a-icon type="file"/>-->
<!--                  {{ text }}-->
                </span>

                <!--                <a-icon type="folder" v-if="record.file_attr.substr(0,1)==='d'"/>-->
                <!--                <a-icon type="file" v-else/>-->
                <!--                {{ text }}-->


              </a>


            </a-table>
          </div>
        </a-drawer>
      </div>
    </div>


    <div id="terminal"></div>
  </div>
</template>

<script>
  import {Terminal} from 'xterm'

  const columns = [

    {
      title: '名称',
      dataIndex: 'file_name',
      width: 300,
      scopedSlots: {customRender: 'name'},
    },
    {
      title: '大小',
      dataIndex: 'file_size',

    },
    {
      title: '修改时间',
      dataIndex: 'file_modify_time',
      width: 200,
    },
    {
      title: '属性',
      dataIndex: 'file_attr',
      width: 150,
      scopedSlots: {customRender: 'file_attr'},
    },
    {
      title: '操作',
      dataIndex: 'action',
    },
  ];

  const data = [];
  // for (let i = 0; i < 3; i++) {
  //   data.push({
  //     key: i,
  //     name: `home`,
  //     age: 32,
  //     address: `London, Park Lane no. ${i}`,
  //   });
  // }
  export default {
    name: 'Console',
    data() {
      return {
        host_info: {},
        visible: false,
        headers: {
          authorization: 'authorization-text',
        },
        ws: null, // websocket连接
        data,
        columns,
        path: ['/',], // 默认是根路径，获取根路径下所有的文件和文件夹 ls-l /
        // shell_or_folder:0, // 判断用户是在操作shell还是在操作文件管理器
        file_folder_list: [], // 存放目录和文件信息数据
        // cmd1:`\\ls -l -h --time-style '+%Y/%m/%d %H:%M:%S'`,
        // cmd2:`\\ls -l -h -a --time-style '+%Y/%m/%d %H:%M:%S'`,
        ls_cmd: "\\ls -l -h --time-style '+%Y/%m/%d %H:%M:%S'",
        folder_path_str: '/',
        visit_url:'',
      }
    },
    methods: {
      // 下载文件
      confirm(text){
        // 拼接文件下载路径
        let file_path = `${this.folder_path_str}/${text}`;
        console.log(file_path);
        // 发送请求，下载文件数据
        // this.$axios.post(`${this.$settings.host}/host/file/${this.$route.params.id}/`,{
        //
        // })

      },


			// 显示隐藏文件和隐藏显示文件
      switch_on_off(e) {
        // console.log('>>>',e);  // true\false
        if (e) {
          // 开启显示隐藏文件
          this.ls_cmd = `\\ls -l -h -a --time-style '+%Y/%m/%d %H:%M:%S'`
          this.send_show_folder_cmd(this.folder_path_str, this.ls_cmd);

        } else {
          // 关闭显示隐藏文件
          this.ls_cmd = `\\ls -l -h --time-style '+%Y/%m/%d %H:%M:%S'`
          this.send_show_folder_cmd(this.folder_path_str, this.ls_cmd);
        }

      },

      back_folder(text, f_index) {
        // this.path = this.path.slice(0,f_index+1);
        this.path = this.path.slice(0, f_index);  // ['/' ,'bin', 'xx']  /bin

        this.join_folder(text);
      },

			// 拼接访问的目录路径
      join_folder(text) {
        // console.log(text);
        // 发请求获取路径下的文件或者文件夹信息
        // this.$axios.get(`${this.settings.host}/`)
        // 拼接路径
        // console.log(text);
        // this.path.push(text);
        // let now_year = (new Date()).getFullYear();


        this.file_folder_list = [];  //

        if (text === '/') {  // bin
          this.path = ['/',]
        } else {
          this.path.push(text);  // ['/','bin',]  //bin/xx
        }
        // console.log('>>>>>',this.path);

        let folder_path = this.path.join('/');  //   //
        // folder_path = '/'
        if (this.path.length > 1) {
          folder_path = folder_path.slice(1); //   /bin
        }
        this.folder_path_str = folder_path;  // '/'
        // console.log(this.path,'|||||',folder_path)
        // console.log(this.ws);
        // folder_path = '/home'
        // this.ws.send(`xx*ls -l ${folder_path}`);
        this.send_show_folder_cmd(this.folder_path_str, this.ls_cmd);

      },

      // 发送ls指令
      send_show_folder_cmd(folder_path, cmd) {
        this.$axios.get(this.visit_url, {
          params: {
            cmd: `${cmd} ${folder_path}`,  // ls -a /
          }
        }).then((res) => {
          console.log('>>>>>>',this.folder_path_str);
          console.log('>>>>>>',res);
          this.data = [];
          let data = res.data;
          // console.log(data);
          let data_l = data[1].split('\n').slice(1);

          // console.log('///',data_l);
          data_l.forEach((file_info, file_index) => {
            // console.log(v);
            if (file_info) {
              // console.log(file_info,file_index);
              //["drwxr-xr-x", "2", "root", "root", "4096", "2020/09/14", "17:34:06", "bin"]
              let files_list = file_info.trim().split(/\s+/);
              // console.log(files_list);
              let a_list = files_list.slice(5, 7);
              let timer = a_list.join(' ');

              this.data.push({
                key: `${files_list[7] + 1}`,
                file_name: files_list[7],  //[-1]， 不支持负数索引
                file_size: files_list[4],
                file_modify_time: timer,
                file_attr: files_list[0],

              })

            }


          })
          // this.file_folder_list = this.file_folder_list.concat(data_l_2);

        }).catch((error) => {
          console.log('报错啦！！！');
        })
      },


      show_comand_result() {
        let pk = this.$route.params.id;
        let token = this.$settings.check_login(this);
        this.$axios.get(`${this.$settings.HOST}/host/list/${pk}/`,{
          headers:{
            'Authorization': `jwt ${token}`,
          }
        })
          .then((res) => {
            console.log('>>>>>',res);
            this.host_info = res.data;
          })
          .catch((error) => {

          })

        // var term = new Terminal();
        var term = new Terminal({
          rendererType: "canvas", //渲染类型
          rows: 40, //行数
          convertEol: true, //启用时，光标将设置为下一行的开头
          scrollback: 100,//终端中的回滚量
          disableStdin: false, //是否应禁用输入。
          cursorStyle: 'bar', //光标样式
          cursorBlink: true, //光标闪烁
          theme: {
            // foreground: '#ffffff', //字体
            background: '#060101', //背景色
            cursor: 'help',//设置光标
          }
        });
        let ws = new WebSocket(`ws://api.hippo.com:8000/ws/ssh/${this.$route.params.id}/`);
        this.ws = ws;
        var keyWord = '';
        this.ws.onmessage = function (event) {
          // msg += event.data
          // term.prompt();
          // console.log('收到消息:' + event.data)
          if (!this.visible) {
            if (!keyWord) {
              //所要执行的操作
              term.write(event.data);
            } else {
              keyWord = ''
              // 对响应回来的数据进行一些加工处理，筛选出结果内容部分
              let a = event.data.replace(event.data.split('\r\n', 1)[0], '');
              let b = a.split('\r\n', -1).slice(0, -1).join('\r\n');
              term.write('\r\n'+b);
            }
          } else {
            // console.log('>>>>>>',event.data);
          }

        }
        term.prompt = () => {
          term.write('\r\n');
          // term.write('\r\n$ ')
          let msg;
          msg = '';
        };


        term.onKey(e => {
          // console.log(e)
          const ev = e.domEvent
          const printable = !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey

          // console.log('>>>>', ev.keyCode);
          if (ev.keyCode === 13) {
            // ws.send()
            // console.log(keyWord);
            this.ws.send(keyWord);
            // keyWord=''

          } else if (ev.keyCode === 8) {
            // Do not delete the prompt
            if (term._core.buffer.x > 2) {
              term.write('\b \b')
            }
          } else if (printable) {
            term.write(e.key);
            keyWord += e.key
          }
        })
        term.open(document.getElementById('terminal'));
        // term.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ')


      },


      afterVisibleChange(val) {
        console.log('visible', val);
      },
      showDrawer() {
        // 向后台发请求，获取根目录下的目录和文件信息列表
        this.visible = true;
        this.visit_url = `${this.$settings.HOST}/host/file/${this.$route.params.id}/`;
        this.join_folder('/');
      },
      onClose() {
        this.visible = false;
      },
      handleChange(info) {
        if (info.file.status !== 'uploading') {
          // console.log(info.file, info.fileList);

        }
        if (info.file.status === 'done') {
          this.send_show_folder_cmd(this.folder_path_str, this.ls_cmd);
          this.$message.success(`${info.file.name} file uploaded successfully`);


        } else if (info.file.status === 'error') {
          this.$message.error(`${info.file.name} file upload failed.${info.file.response.error}`);
        }
      },
    },

    mounted() {
      this.show_comand_result();

    },


  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .console_header {
    display: flex;
    align-items: center;
    height: 46px;
    justify-content: space-between;
    padding: 0 10px;
    background-color: #e6f7ff;
  }

  .file_nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
  }

</style>
