<script setup>
import { ref, onMounted } from "vue";
import { ElMessageBox, ElNotification, ElMessage } from "element-plus";
import { Copy } from "@icon-park/vue-next";
import { useRouter } from "vue-router";
import useClipboard from "vue-clipboard3";

const { toClipboard } = useClipboard();
const copy = async (msg) => {
  try {
    // 复制
    await toClipboard(msg);
    // 复制成功
  } catch (e) {
    // 复制失败
    console.log(e);
  }
};
const router = useRouter();
//默认值
//初次使用的默认值
//表格数据
const tableData = ref([]);
//表格数据总条数
const recordsTotal = ref(0);
//每页显示条数
const recordsPerPage = ref(8);
//当前页实际条数
const recordsOnPage = ref(0);
//当前页码
const currentPage = ref(1);
//新增规则的弹窗显示的数据
const newRow = ref({});
//操作表格时弹窗显示的数据
const rowCopy = ref({});
//操作表格时该行的原始数据
let rowOrigin = {};
//控制dialog显示
const isMoreInfo = ref(false);
const isAddDialog = ref(false);
//选择录入模式
const isAddTwoDialog=ref(false);
//table是否在加载状态
const isTableLoading = ref(true);
//多次使用的默认值
const defaultValueOnMounted = {
  user: {
    name: "",
    comment: "默认备注",
  },
  queryCondition: {
    is_rule: "",
    is_deprecated: false,
    name: "",
    comment: "",
  },
};
const platformOptions = ref([]);
const ruleOptions = ref([]);
const rawPasswordOptions = ref([]);
const addForm = ref(null);
const addFormTwo=ref(null);
const loadData = () => {
  console.log(defaultValueOnMounted.queryCondition.is_rule);
  window.pywebview.api
    .search_user(
      currentPage.value,
      recordsPerPage.value,
      defaultValueOnMounted.queryCondition.is_deprecated,
      defaultValueOnMounted.queryCondition.name,
      defaultValueOnMounted.queryCondition.comment
    )
    .then((res) => {
      recordsOnPage.value = res.recordOnPage;
      console.log("loadData");
      console.log(res.data);
      tableData.value = res.data;
      recordsTotal.value = res.total;
      newRow.value = JSON.parse(JSON.stringify(defaultValueOnMounted.user));
      isTableLoading.value = false;
    });
};

//新增一条数据的弹窗
const handleAddDialog = () => {
  newRow.value = JSON.parse(JSON.stringify(defaultValueOnMounted.user));
  isAddDialog.value = true;
};
const handleAddTwoDialog=()=>{
  newRow.value=JSON.parse(JSON.stringify(defaultValueOnMounted.user));
  isAddTwoDialog.value=true;
}
//新增一条数据的提交
const handleAddNewRow = () => {
  addForm.value.validate((valid) => {
    if (!valid) {
      ElMessage({
        message: "请检查输入的内容",
        type: "error",
      });
      return;
    } else {
      ElMessageBox.confirm("确定要新增一条规则吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          const raw_password =
            rawPasswordOptions.value[newRow.value["raw_password_id"]]
              .raw_password + newRow.value["platform_alias"];
          const rule = ruleOptions.value[newRow.value["rule_id"]].rule;
          window.pywebview.api
            .add_user(
              newRow.value["name"],
              raw_password,
              true,
              rule,
              newRow.value["comment"]
            )
            .then((res) => {
              if (res.code) {
                ElNotification({
                  title: "插入失败",
                  message: res.message,
                  type: "error",
                });
              } else {
                isTableLoading.value = true;
                setTimeout(() => {
                  loadData();
                }, 200);
                ElNotification({
                  title: "插入成功",
                  message: "已成功新增一条规则,正在刷新网页...",
                  type: "success",
                });
                isAddDialog.value = false;
              }
            });
        })
        .catch((e) => {
          ElNotification({
            title: "已取消",
            message: e,
            type: "info",
          });
        });
    }
  });
};
const handleAddNewRowTwo=()=>{
  addFormTwo.value.validate((valid)=>{
    if(!valid){
      ElMessage({
        message: "请检查输入的内容",
        type: "error",
      });
      return;
    }else{
      ElMessageBox.confirm("确定要录入一条密码吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          const password =
            newRow.value["password"];
          const name=newRow.value["name"];
          const comment=newRow.value["comment"];
          window.pywebview.api
            .add_user(
              name,
              password,
              false,
              null,
              comment
            )
            .then((res) => {
              if (res.code) {
                ElNotification({
                  title: "插入失败",
                  message: res.message,
                  type: "error",
                });
              } else {
                isTableLoading.value = true;
                setTimeout(() => {
                  loadData();
                }, 200);
                ElNotification({
                  title: "插入成功",
                  message: "已成功录入密码,正在刷新网页...",
                  type: "success",
                });
                isAddTwoDialog.value = false;
              }
            });
        })
        .catch((e) => {
          ElNotification({
            title: "已取消",
            message: e,
            type: "info",
          });
        });
    }
  })
};
//查看数据详细信息的弹窗
const handleMoreInfo = (row) => {
  rowCopy.value = JSON.parse(JSON.stringify(row));
  rowOrigin = JSON.parse(JSON.stringify(row));
  isMoreInfo.value = true;
};
const handleCopy = (item) => {
  copy(item);
  ElMessage({
    message: item + "已复制到剪贴板",
    type: "success",
  });
};
//弃用一条数据
const handleDeprecateRow = () => {
  ElMessageBox.confirm("本条规则将进入回收站, 是否继续?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api.deprecate_user(rowCopy.value["id"]).then((res) => {
        if (res.code) {
          ElNotification({
            title: "删除失败",
            message: res.message,
            type: "error",
          });
        } else {
          ElNotification({
            title: "删除成功",
            message: "已删除" + rowCopy.value["name"] + ",请到回收站查看",
            type: "success",
          });
        }
        isMoreInfo.value = false;
        loadData();
      });
    })
    .catch(() => {
      ElNotification({
        title: "删除操作已取消",
        type: "info",
      });
    });
};
//换页
const handleCurrentChange = (page) => {
  currentPage.value = page;
  loadData();
};
//刷新
const handleRefresh = () => {
  isTableLoading.value = true;
  ElNotification({
    title: "刷新中",
    message: "正在刷新网页...",
    type: "success",
    duration: 1000,
  });
  setTimeout(() => {
    loadData();
  }, 200);
};
const handleUpdateRow = () => {
  window.pywebview.api
    .update_user(
      rowCopy.value["id"],
      rowCopy.value["name"],
      rowCopy.value["password"],
      rowCopy.value["comment"]
    )
    .then((res) => {
      if (res.code) {
        ElNotification({
          title: "更新失败",
          message: res.message,
          type: "error",
        });
      } else {
        ElNotification({
          title: "更新成功",
          message: "已成功更新一条规则,正在刷新网页...",
          type: "success",
        });
        isMoreInfo.value = false;
        isTableLoading.value = true;
        setTimeout(() => {
          loadData();
        }, 200);
      }
    });
};
const addRule = ref({
  name: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  rule_id: [{ required: true, message: "请选择规则", trigger: "blur" }],
  platform_id: [{ required: true, message: "请选择平台", trigger: "blur" }],
  raw_password_id: [
    { required: true, message: "请选择原始密码", trigger: "blur" },
  ],
  platform_alias: [
    { required: true, message: "请选择平台别名", trigger: "blur" },
  ],
});
const addTwoRule=ref({
  name:[{ required: true, message: "请输入用户名", trigger: "blur" }],
  password:[{ required: true, message: "请输入密码", trigger: "blur" }]
})
onMounted(() => {
  loadData();
  window.pywebview.api.search_platform_all().then((res) => {
    platformOptions.value = res.data;
    platformOptions.value.forEach((item) => {
      window.pywebview.api.search_platform_alias(item["id"]).then((res) => {
        item["alias"] = res.data.map((item) => JSON.parse(item));
      });
    });
    console.log(platformOptions.value);
  });
  window.pywebview.api.search_rule_all().then((res) => {
    ruleOptions.value = res.data;
  });
  window.pywebview.api.search_raw_password_all().then((res) => {
    rawPasswordOptions.value = res.data;
  });
});
</script>

<template>
  <el-dialog
    v-model="isMoreInfo"
    :center="true"
    draggable
    style="width: fit-content"
  >
    <template #header>
      <span>
        {{ rowCopy["name"] + " 详细信息" }}
      </span>
    </template>
    <el-form label-position="left" label-width="100px" style="max-width: 300px">
      <el-form-item label="用户名">
        <el-input
          v-model="rowCopy['name']"
          :maxlength="20"
          clearable
          show-word-limit
        ></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input
          v-model="rowCopy['password']"
          :maxlength="20"
          clearable
          show-word-limit
        ></el-input>
      </el-form-item>
      <el-form-item label="备注">
        <el-input
          v-model="rowCopy['comment']"
          :maxlength="40"
          clearable
          show-word-limit
          type="textarea"
        ></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button-group>
        <el-button type="danger" @click="handleDeprecateRow">删除</el-button>
        <el-button
          :disabled="JSON.stringify(rowCopy) === JSON.stringify(rowOrigin)"
          type="warning"
          @click="handleUpdateRow"
          >修改
        </el-button>
        <el-button type="primary" @click="isMoreInfo = false">取消</el-button>
      </el-button-group>
    </template>
  </el-dialog>
  <el-dialog
    v-model="isAddDialog"
    :align-center="true"
    :center="true"
    draggable
    style="width: fit-content"
  >
    <template #header>
      <span> 生成密码 </span>
    </template>
    <el-form
      ref="addForm"
      :model="newRow"
      :rules="addRule"
      label-position="left"
      label-width="100px"
      style="max-width: 300px"
    >
      <el-form-item label="用户名" prop="name">
        <el-input
          v-model="newRow['name']"
          :maxlength="20"
          clearable
          show-word-limit
        ></el-input>
      </el-form-item>
      <el-form-item label="规则" prop="rule_id">
        <el-select
          v-model="newRow['rule_id']"
          clearable
          filterable
          placeholder="请选择规则"
        >
          <el-option
            v-for="(item, index) in ruleOptions"
            :key="item.id"
            :label="item.name"
            :value="index"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-alert
        v-if="newRow.hasOwnProperty('rule_id')"
        show-icon
        title="规则说明"
        type="info"
      >
        <p>最小长度: {{ ruleOptions[newRow["rule_id"]].rule.min_length }}</p>
        <p>最大长度: {{ ruleOptions[newRow["rule_id"]].rule.max_length }}</p>
        <p>
          小写字母个数: {{ ruleOptions[newRow["rule_id"]].rule.lower_count }}
        </p>
        <p>
          大写字母个数: {{ ruleOptions[newRow["rule_id"]].rule.upper_count }}
        </p>
        <p>数字个数: {{ ruleOptions[newRow["rule_id"]].rule.number_count }}</p>
        <p>
          特殊字符个数: {{ ruleOptions[newRow["rule_id"]].rule.special_count }}
        </p>
      </el-alert>
      <el-form-item label="原始密码" prop="raw_password_id">
        <el-select
          v-model="newRow['raw_password_id']"
          clearable
          filterable
          placeholder="请选择原始密码"
        >
          <el-option
            v-for="(item, index) in rawPasswordOptions"
            :key="index"
            :label="item.raw_password"
            :value="index"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="平台" prop="platform_id">
        <el-select
          v-model="newRow['platform_id']"
          clearable
          filterable
          placeholder="请选择平台"
        >
          <el-option
            v-for="(item, index) in platformOptions"
            :key="index"
            :label="item.name"
            :value="index"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        v-if="newRow.hasOwnProperty('platform_id')"
        label="平台别名"
        prop="platform_alias_id"
      >
        <el-select
          v-model="newRow['platform_alias']"
          clearable
          filterable
          placeholder="请选择平台别名"
        >
          <el-option
            v-for="(item, index) in platformOptions[newRow['platform_id']]
              .alias"
            :key="index"
            :label="item.name"
            :value="item.name"
          >
            <span style="float: left">{{ item.name }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{
              item.comment
            }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="备注">
        <el-input
          v-model="newRow['comment']"
          :maxlength="40"
          clearable
          show-word-limit
          type="textarea"
        ></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="isAddDialog = false">取消</el-button>
      <el-button type="primary" @click="handleAddNewRow">添加</el-button>
    </template>
  </el-dialog>
  <el-dialog
    v-model="isAddTwoDialog"
    :align-center="true"
    :center="true"
    draggable
    style="width: fit-content"
  >
    <template #header>
      <span> 录入密码 </span>
    </template>
    <el-form
      ref="addFormTwo"
      :model="newRow"
      :rules="addTwoRule"
      label-position="left"
      label-width="100px"
      style="max-width: 300px"
    >
      <el-form-item label="用户名" prop="name">
        <el-input
          v-model="newRow['name']"
          :maxlength="20"
          clearable
          show-word-limit
        ></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
       <el-input
           v-model="newRow['password']"
            :maxlength="20"
            clearable
            show-word-limit
       ></el-input>
      </el-form-item>
      <el-form-item label="备注">
        <el-input
          v-model="newRow['comment']"
          :maxlength="40"
          clearable
          show-word-limit
          type="textarea"
        ></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="isAddDialog = false">取消</el-button>
      <el-button type="primary" @click="handleAddNewRowTwo">添加</el-button>
    </template>
  </el-dialog>
  <div>
    <div style="margin-bottom: 20px">
      <el-button size="large" type="primary" @click="handleAddDialog">
        <el-icon>
          <ele-Plus />
        </el-icon>
        生成密码
      </el-button>
      <el-button size="large" type="primary" @click="handleAddTwoDialog">
        <el-icon>
          <ele-Plus />
        </el-icon>
        录入密码
      </el-button>
      <el-button size="large" type="info" @click="handleRefresh">
        <el-icon>
          <ele-Refresh />
        </el-icon>
        刷新
      </el-button>
      <el-button
        size="large"
        type="warning"
        @click="router.push('/userRubbish')"
      >
        <el-icon>
          <ele-Delete></ele-Delete>
        </el-icon>
        回收站
      </el-button>
    </div>
    <el-table
      v-loading="isTableLoading"
      :data="tableData"
      border
      default-expand-all
      style="width: 100%; user-select: none"
    >
      <el-table-column
        align="center"
        fixed
        label="序号"
        type="index"
        width="60"
      >
      </el-table-column>
      <!-- 数据展示 -->
      <el-table-column align="center" label="id">
        <template #default="scope">
          <el-input v-model="scope.row['id']"  show-password>
            <template #append>
              <el-button @click="handleCopy(scope.row['id'])">
                <Copy />
              </el-button>
            </template>
          </el-input>
        </template>
      </el-table-column>
      <el-table-column align="center" label="用户名">
        <template #default="scope">
          <el-input v-model="scope.row['name']" show-password>
            <template #append>
              <el-button @click="handleCopy(scope.row['name'])">
                <Copy />
              </el-button>
            </template>
          </el-input>
        </template>
      </el-table-column>
      <el-table-column label="密码" align="center">
        <template #default="scope">
          <el-input v-model="scope.row['password']" readonly="readonly" show-password>
            <template #append>
              <el-button @click="handleCopy(scope.row['password'])">
                <Copy />
              </el-button>
            </template>
          </el-input>
        </template>
      </el-table-column>
      <el-table-column label="备注" align="center">
        <template #default="scope">
          <el-input v-model="scope.row['comment']" readonly="readonly" >
          </el-input>
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="150" align="center">
        <template #default="scope">
          <el-button-group>
            <el-button type="primary" @click="handleMoreInfo(scope.row)">
              <el-icon>
                <ele-More />
              </el-icon>
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <div
    style="
      display: flex;
      align-items: center;
      flex-direction: column;
      margin-top: 20px;
    "
  >
    <el-pagination
      layout=" prev, pager, next"
      :total="recordsTotal"
      :page-size="recordsPerPage"
      background
      :hide-on-single-page="true"
      @current-change="handleCurrentChange"
    ></el-pagination>
  </div>
</template>

<style scoped></style>
