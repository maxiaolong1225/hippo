<template>
  <div class="host">
    <div class="host_search">
      <a-row>
        <a-col :span="6">
          <a-form-item
            :label-col="formItemLayout.labelCol"
            :wrapper-col="formItemLayout.wrapperCol"
            label="主机类别："
          >
            <a-select v-model="host_search_form.form.category"
                      placeholder="请选择"
                      style="width: 120px;"
                      @change="handleSelectChange"
            >

              <a-select-option v-for="(value, index) in host_category_data" :key="value.id" :value="value.id">
                {{ value.name }}
              </a-select-option>

            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="6">
          <a-form-item
            :label-col="formItemLayout.labelCol"
            :wrapper-col="formItemLayout.wrapperCol"
            label="主机别名："
          >
            <a-input
              placeholder="请输入"
            />
          </a-form-item>
        </a-col>
        <a-col :span="6">
          <a-form-item
            :label-col="formItemLayout.labelCol"
            :wrapper-col="formItemLayout.wrapperCol"
            label="连接地址："
          >
            <a-input
              v-decorator="[
          'nickname',
          { rules: [{ required: checkNick, message: 'Please input your nickname' }] },
        ]"
              placeholder="请输入"
            />
          </a-form-item>
        </a-col>
        <a-col :span="6">
          <router-link to="/hippo/hosts/">
            <a-button icon="search" style="margin-top: 3px;" type="primary">
              搜索
            </a-button>
          </router-link>
        </a-col>
      </a-row>

    </div>

    <div class="host_add" style="margin-bottom: 15px;">
      <span><a-button icon="plus" type="primary" @click="showModal">新建</a-button></span>
      <span><a-button icon="import" style="margin-left: 20px;" type="primary"
                      @click="showExcelModal">批量导入</a-button></span>
      <span><a style="color:green;margin-left: 20px;" :href="host_excel_url"> 导出主机列表数据</a></span>
    </div>

    <div class="host_table">
      <a-table :columns="columns" :data-source="host_data" rowKey="id">
        <a slot="action" slot-scope="text,scope" href="javascript:;">
          <a-button size="small" type="link">编辑 |</a-button>
          <a-button size="small" type="link" @click="delete_one_host(scope.id)">
            删除 |
          </a-button>
          <a-button size="small" type="link">
            <router-link :to="'/hippo/console/' + scope.id +'/'">console</router-link>
          </a-button>
        </a>
      </a-table>

    </div>


    <!--  新建主机模态对话框-->
    <div>
      <a-modal v-model="visible" title="新建主机" width="800px" @ok="handleOk">
        <a-form-model
          ref="ruleForm"
          :label-col="add_host_form.labelCol"
          :model="add_host_form.form"
          :rules="add_host_form.rules"
          :wrapper-col="add_host_form.wrapperCol"
        >

          <a-form-model-item label="选择主机类别" prop="category">
            <a-select v-model="add_host_form.form.category" placeholder="请选择主机类别">
              <a-select-option v-for="(host_category_value,host_category_index) in host_category_data"
                               :key="host_category_index"
                               :value="host_category_value.id">
                {{ host_category_value.name }}
              </a-select-option>

            </a-select>
          </a-form-model-item>
          <a-form-model-item ref="hostname" label="输入主机名" prop="hostname">
            <a-input v-model="add_host_form.form.hostname"
                     placeholder="请输入主机名"
                     @blur="
          () => {
            $refs.hostname.onFieldBlur();
          }
        "
            />
          </a-form-model-item>

          <a-form-model-item ref="name" label="输入链接信息" prop="name">

            <a-row>
              <a-col :span="8">
                <a-input v-model="add_host_form.form.username" addon-before="用户名" placeholder="请输入用户名"/>
              </a-col>
              <a-col :span="8">
                <a-input v-model="add_host_form.form.ip_addr" addon-before="@" placeholder="请输入IP地址"/>
              </a-col>
              <a-col :span="8">
                <a-input v-model="add_host_form.form.port" addon-before="端口号" placeholder="请输入端口号"/>
              </a-col>

            </a-row>

          </a-form-model-item>

          <a-form-model-item ref="password" label="输入连接密码" prop="password">
            <a-input v-model="add_host_form.form.password" placeholder="请输入密码"
                     type="password"
                     @blur="
          () => {
            $refs.password.onFieldBlur();
          }
        "
            />
          </a-form-model-item>

          <a-form-model-item label="描述" prop="desc">
            <a-input v-model="add_host_form.form.desc" placeholder="请输入描述信息" type="textarea"/>
          </a-form-model-item>

        </a-form-model>

      </a-modal>
    </div>

    <!--    批量导入对话框-->
    <div>
      <a-modal v-model="excel_model_visible" title="批量导入" @ok="handleExcelOk">
        <template slot="footer">
          <a-button key="back" @click="handleUploadExcelCancel">
            取消
          </a-button>
          <a-button
            :disabled="excel_fileList.length === 0"
            :loading="excel_uploading"
            style="margin-top: 16px"
            type="primary"
            @click="handleExcelUpload"
          >
            {{ excel_uploading ? 'Uploading' : 'Start Upload' }}
          </a-button>
        </template>

        <div>
          <a-alert banner
                   closable
                   message="导入或输入的密码仅作首次验证使用，并不会存储密码。"
                   type="info"
          />
          <br/>
          <a-form :form="upload_excel_form">

            <a-form-item
              :label-col="formItemLayout.labelCol"
              :wrapper-col="formItemLayout.wrapperCol"
              help="请下载使用该模板填充数据后导入"
              label="模板下载"
            >
              <a download="主机导入模板.xls" href="../../static/file/主机导入模板.xls">主机导入模板.xls</a>
            </a-form-item>

            <a-form-item
              :label-col="formItemLayout.labelCol"
              :wrapper-col="formItemLayout.wrapperCol"
              help="如果Excel中密码为空则使用该密码"
              label="默认密码"
            >
              <a-input
                v-model="default_password"
                placeholder="请输入默认主机密码"
              />
            </a-form-item>

            <a-form-item
              :label-col="formItemLayout.labelCol"
              :wrapper-col="formItemLayout.wrapperCol"
              label="导入数据"
            >

              <div class="clearfix">
                <a-upload v-decorator="[
                    'host_excel',
                    { rules: [{ required: true, message: '请上传文件' }] },
                  ]" :before-upload="beforeExcelUpload" :file-list="excel_fileList"
                          :remove="handleExcelRemove">
                  <a-button>
                    <a-icon type="upload"/>
                    Select Files
                  </a-button>
                </a-upload>

              </div>


            </a-form-item>


          </a-form>
        </div>


      </a-modal>


    </div>

<!--    edit host moeal s s s s -->

  </div>
</template>


<script>

const formItemLayout = {
  labelCol: {span: 4},
  wrapperCol: {span: 10},
};
const columns = [
  {title: 'id', dataIndex: 'id', key: 'id'},
  {title: '类别', dataIndex: 'category_name', key: 'category_name'},
  {title: '主机名称', dataIndex: 'hostname', key: 'hostname'},
  {title: '连接地址', dataIndex: 'ip_addr', key: 'ip_addr'},
  {title: '端口号', dataIndex: 'port', key: 'port'},
  {title: '描述', dataIndex: 'desc', key: 'desc'},
  {title: 'Action', dataIndex: '', key: 'x', scopedSlots: {customRender: 'action'}},
];

export default {
  name: "Host",
  data() {
    return {
      // edit host data
      //edit_host_visible: false,

      //excel批量导入
      excel_model_visible: false,
      excel_fileList: [],
      excel_uploading: false,
      upload_excel_form: this.$form.createForm(this, {name: 'coordinated'}),
      loading: false,
      default_password: '',
      host_excel_url: `${this.$settings.HOST}/host/host_excel/`,


      checkNick: false,
      host_data: [],
      host_category_data: [
        {id: 0, name: ""},
      ],  // 主机类别数据
      formItemLayout,
      selectedRowKeys: [],
      columns,
      visible: false,
      add_host_form: {
        labelCol: {span: 4},
        wrapperCol: {span: 14},
        other: '',
        form: {
          hostname: '',
          category: '',
          username: '',
          ip_addr: '',
          port: 22,
          password: '',
          desc: '',
        },
        rules: {
          hostname: [
            {required: true, message: '请输入主机名称', trigger: 'blur'},
            {min: 1, max: 100, message: 'Length should be 1 to 100', trigger: 'blur'},
          ],
          username: [
            {required: true, message: '请输入主机用户名', trigger: 'blur'},
            {min: 1, max: 100, message: 'Length should be 1 to 100', trigger: 'blur'},
          ],
          ip_addr: [
            {required: true, message: '请输入主机IP地址', trigger: 'blur'},
            {min: 1, max: 100, message: 'Length should be 1 to 100', trigger: 'blur'},
          ],
          port: [
            {required: true, message: '请输入主机端口', trigger: 'blur'},
            {min: 1, max: 100, message: 'Length should be 1 to 100', trigger: 'blur'},
          ],
          password: [
            {required: true, message: '请输入主机密码', trigger: 'blur'},
            {min: 1, max: 100, message: 'Length should be 1 to 100', trigger: 'blur'},
          ],


        },
      },
      host_search_form: {
        form: {
          category: 1,
        }
      }

    }
  },
  created() {
    this.get_host_data();
    this.get_host_category_date();
  },
  methods: {
    delete_one_host(pk) {
      let token = this.$settings.check_login(this);
      var index = null;
      // 前端页面删除
      this.host_data.some((item, i)=>{
        if(item.id === pk){
          index = i;
          return true
        };
      });

      this.host_data.splice(index, 1);
      //后台数据删除
      this.$axios.delete(`${this.$settings.HOST}/host/list/` + pk + '/', {
            headers: {
              'Authorization': `jwt ${token}`
            }
      }).then((res) => {
          this.$message.success('删除主机成功');
      }).catch((error) => {
        this.$message.success('删除主机失败', error);
      })
    },
    //批量导入
    showExcelModal() {
      this.excel_model_visible = true;
    },

    handleExcelOk(e) {
      console.log(e);
      this.excel_model_visible = false;
    },

    handleUploadExcelCancel() {
      this.excel_model_visible = false;
    },
    handleExcelUpload() {
      const formData = new FormData();
      this.excel_fileList.forEach((file_value, file_index) => {
        formData.append('host_excel', file_value);
      });
      formData.append('default_password', this.default_password);
      //验证token
      let token = this.$settings.check_login(this);

      this.$axios.post(`${this.$settings.HOST}/host/host_excel/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `jwt ${token}`
        },

      }).then((res) => {
        this.$message.success('上传成功');
        this.host_data = this.host_data.concat(res.data.data);
        this.excel_model_visible = false;
      }).catch((error) => {
        this.$message.error("上传失败");
      })


    },


    // 选中的想要上传的文件进行删除
    handleExcelRemove(file) {
      const index = this.excel_fileList.indexOf(file);
      const newFileList = this.excel_fileList.slice();
      newFileList.splice(index, 1);
      this.excel_fileList = newFileList;
    },
    // 上传之前将所有文件列表赋值给excel_fileList数据属性
    beforeExcelUpload(file) {
      // console.log('file>>>>>', file)
      this.excel_fileList = [...this.excel_fileList, file];
      // this.excel_fileList = this.excel_fileList.push(file);
      return false;
    },

    handleChange(value) {
      this.$refs.ruleForm.resetFields();
      console.log(`selected ${value}`);
    },
    showModal() {
      this.visible = true;
    },

    handleOk(e) {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          // 前端校验成功之后做的事情
          // alert('submit!');
          // 发送请求携带主机数据到后台进行主机的添加
          // console.log('添加主机的数据>>>>',this.add_host_form.form)

          let token = sessionStorage.token || localStorage.token;
          console.log('>>>', token);
          console.log("发往后台的数据：", this.add_host_form.form)

          this.$axios.post(`${this.$settings.HOST}/host/list/`, this.add_host_form.form, {

            headers: {
              'Authorization': `jwt ${token}`
            }

          }).then((res) => {
            // this.host_category_data = res.data;
            this.host_data.push(res.data);
          }).catch((error) => {
            this.$message.error('请求参数有误！！')
          })


        } else {
          console.log('error submit!!');
          return false;
        }
      });
      console.log(e);
      this.visible = false;
    },

    get_host_category_date() {
      let token = localStorage.token || sessionStorage.token;
      this.$axios.get(`${this.$settings.HOST}/host/categorys/`, {
        headers: {
          'Authorization': `jwt ${token}`
        }
      }).then((res) => {
        console.log("host category", res.data);
        this.host_category_data = res.data;
      }).catch((error) => {

      })

    },

    get_host_data() {
      let token = localStorage.token || sessionStorage.token;
      this.$axios.get(`${this.$settings.HOST}/host/list/`, {
        headers: {
          'Authorization': `jwt ${token}`
        }
      }).then((res) => {
        console.log("host list", res.data);
        this.host_data = res.data;
      }).catch((error) => {
        console.log(error);

      })
    },

    handleSelectChange(value) {
      console.log(value);
    },


  }
}
</script>


<style scoped>
.components-input-demo-size .ant-input {
  width: 200px;
  margin: 0 8px 8px 0;
}
</style>
