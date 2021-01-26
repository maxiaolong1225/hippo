<template>
  <div class="host">
   <div class="host_search">
      <a-row>
        <a-col :span="6">
          <a-form-item
            label="主机类别："
            :label-col="formItemLayout.labelCol"
            :wrapper-col="formItemLayout.wrapperCol"
          >
            <a-select style="width: 120px;"
                      placeholder="请选择"
                      @change="handleSelectChange"
                      v-model="host_search_form.form.category"
            >

              <a-select-option :value="value.id" v-for="(value, index) in host_category_data" :key="value.id">
                {{value.name}}
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
            <a-button type="primary" icon="sync" style="margin-top: 3px;">
              刷新
            </a-button>
          </router-link>
        </a-col>
      </a-row>

    </div>

        <div class="host_add" style="margin-bottom: 15px;">
      <a-button type="primary" icon="plus" @click="showModal">
        新建
      </a-button>
      <a-button type="primary" icon="import" style="margin-left: 20px;">
        批量导入
      </a-button>
    </div>
    <!--  模态对话框-->
    <div>
      <a-modal v-model="visible" title="新建主机" @ok="handleOk" width="800px">
        <a-form-model
          ref="ruleForm"
          :model="add_host_form.form"
          :rules="add_host_form.rules"
          :label-col="add_host_form.labelCol"
          :wrapper-col="add_host_form.wrapperCol"
        >

          <a-form-model-item label="选择主机类别" prop="category">
            <a-select placeholder="请选择主机类别" v-model="add_host_form.form.category">
              <a-select-option :value="host_category_value.id"
                               v-for="(host_category_value,host_category_index) in host_category_data"
                               :key="host_category_index">
                {{ host_category_value.name }}
              </a-select-option>

            </a-select>
          </a-form-model-item>
          <a-form-model-item ref="hostname" label="输入主机名" prop="hostname">
            <a-input placeholder="请输入主机名"
              v-model="add_host_form.form.hostname"
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
                <a-input placeholder="请输入用户名" addon-before="用户名" v-model="add_host_form.form.username"/>
              </a-col>
              <a-col :span="8">
                <a-input placeholder="请输入IP地址" addon-before="@" v-model="add_host_form.form.ip_addr"/>
              </a-col>
              <a-col :span="8">
                <a-input placeholder="请输入端口号"addon-before="端口号" v-model="add_host_form.form.port"/>
              </a-col>

            </a-row>

          </a-form-model-item>

          <a-form-model-item ref="password" label="输入连接密码" prop="password">
            <a-input placeholder="请输入密码" type="password"
              v-model="add_host_form.form.password"
              @blur="
          () => {
            $refs.password.onFieldBlur();
          }
        "
            />
          </a-form-model-item>

          <a-form-model-item label="描述" prop="desc">
            <a-input placeholder="请输入描述信息" v-model="add_host_form.form.desc" type="textarea"/>
          </a-form-model-item>

        </a-form-model>

      </a-modal>
    </div>


    <div class="host_table">
      <a-table :columns="columns" :data-source="host_data" rowKey="id">
        <a slot="action" slot-scope="text" href="javascript:;">
          <a-button type="link" size="small">编辑 |</a-button>
          <a-button type="link" size="small">删除 |</a-button>
          <a-button type="link" size="small">console</a-button>
        </a>

      </a-table>
    </div>

  </div>
</template>


<script>
const formItemLayout = {
  labelCol: {span: 8},
  wrapperCol: {span: 14},
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
      host_search_form:{
        form:{
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
          console.log("发往后台的数据：",this.add_host_form.form)

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
    }


  }
}
</script>


<style scoped>
/*.components-input-demo-size .ant-input {*/
/*  width: 200px;*/
/*  margin: 0 8px 8px 0;*/
/*}*/
</style>
