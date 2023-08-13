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
const isMoreInfo = ref(false);
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
    is_deprecated: true,
    name: "",
    comment: "",
  },
};
const platformOptions = ref([]);
const ruleOptions = ref([]);
const rawPasswordOptions = ref([]);
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

//查看数据详细信息的弹窗
const handleMoreInfo = (row) => {
  rowCopy.value = JSON.parse(JSON.stringify(row));
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
  ElMessageBox.confirm("本条规则将被彻底删除, 是否继续?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api.delete_user(rowCopy.value["id"]).then((res) => {
        if (res.code) {
          ElNotification({
            title: "删除失败",
            message: res.message,
            type: "error",
          });
        } else {
          ElNotification({
            title: "删除成功",
            message: "已彻底删除" + rowCopy.value["name"],
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
  window.pywebview.api.enable_user(rowCopy.value["id"]).then((res) => {
    if (res.code) {
      ElNotification({
        title: "还原失败",
        message: res.message,
        type: "error",
      });
    } else {
      ElNotification({
        title: "还原成功",
        message: "已还原" + rowCopy.value["name"],
        type: "success",
      });
    }
    isMoreInfo.value = false;
    loadData();
  });
};
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
        <el-text>{{ rowCopy["name"] }}</el-text>
      </el-form-item>
      <el-form-item label="密码">
        <el-text>{{ rowCopy["password"] }}</el-text>
      </el-form-item>
      <el-form-item label="备注">
        <el-text>{{ rowCopy["comment"] }}</el-text>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button-group>
        <el-button type="danger" @click="handleDeprecateRow"
          >彻底删除</el-button
        >
        <el-button type="warning" @click="handleUpdateRow">还原 </el-button>
        <el-button type="primary" @click="isMoreInfo = false">取消</el-button>
      </el-button-group>
    </template>
  </el-dialog>
  <div>
    <div style="margin-bottom: 20px">
      <el-button size="large" type="info" @click="handleRefresh">
        <el-icon>
          <ele-Refresh />
        </el-icon>
        刷新
      </el-button>
      <el-button size="large" type="warning" @click="router.push('/user')">
        <el-icon>
          <ele-Delete></ele-Delete>
        </el-icon>
        返回
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
          <el-input v-model="scope.row['id']" readonly="readonly">
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
          <el-input v-model="scope.row['name']" readonly="readonly">
            <template #append>
              <el-button @click="handleCopy(scope.row['name'])">
                <Copy />
              </el-button>
            </template>
          </el-input>
        </template>
      </el-table-column>
      <el-table-column align="center" label="密码">
        <template #default="scope">
          <el-input v-model="scope.row['password']" readonly="readonly">
            <template #append>
              <el-button @click="handleCopy(scope.row['password'])">
                <Copy />
              </el-button>
            </template>
          </el-input>
        </template>
      </el-table-column>
      <el-table-column align="center" fixed="right" label="操作" width="150">
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
