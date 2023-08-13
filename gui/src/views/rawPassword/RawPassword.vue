<script setup>
import { ref, onMounted } from "vue";
import { ElMessageBox, ElNotification } from "element-plus";
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
//控制dialog显示
const isMoreInfo = ref(false);
const isAddDialog = ref(false);
//table是否在加载状态
const isTableLoading = ref(true);
//多次使用的默认值
const defaultValueOnMounted = {
  password: {
    raw_password: "123456",
    comment: "默认备注",
  },
};

const loadData = () => {
  window.pywebview.api
    .search_raw_password(currentPage.value, recordsPerPage.value)
    .then((res) => {
      recordsOnPage.value = res.recordOnPage;
      tableData.value = res.data.map((item) => JSON.parse(item));
      recordsTotal.value = res.total;
      newRow.value = JSON.parse(JSON.stringify(defaultValueOnMounted.password));
      isTableLoading.value = false;
    });
};
//新增一条数据的弹窗
const handleAddDialog = () => {
  newRow.value = JSON.parse(JSON.stringify(defaultValueOnMounted.password));
  isAddDialog.value = true;
};
//新增一条数据的提交
const handleAddNewRow = () => {
  ElMessageBox.confirm("确定要新增一条密码吗?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api
        .add_raw_password(newRow.value["raw_password"], newRow.value["comment"])
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
              message: "已成功新增一个密码,正在刷新网页...",
              type: "success",
            });
            isAddDialog.value = false;
          }
        });
    })
    .catch(() => {
      ElNotification({
        title: "已取消",
        message: "已取消新增密码",
        type: "info",
      });
    });
};

//删除一条数据
const handleDeleteRow = (row) => {
  ElMessageBox.confirm("本密码将被删除, 是否继续?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api.delete_raw_password(row["id"]).then((res) => {
        if (res.code) {
          ElNotification({
            title: "删除失败",
            message: res.message,
            type: "error",
          });
        } else {
          ElNotification({
            title: "删除成功",
            message: "已彻底删除原始密码" + row["raw_password"],
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
onMounted(() => {
  loadData();
});
</script>

<template>
  <el-dialog
    v-model="isAddDialog"
    :center="true"
    draggable
    style="width: fit-content"
  >
    <template #header>
      <span> 新增原始密码 </span>
    </template>
    <el-form label-position="left" label-width="100px" style="max-width: 300px">
      <el-form-item label="密码">
        <el-input
          v-model="newRow['raw_password']"
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
      <el-button type="primary" @click="handleAddNewRow">添加</el-button>
    </template>
  </el-dialog>

  <div>
    <div style="margin-bottom: 20px">
      <el-button size="large" type="primary" @click="handleAddDialog">
        <el-icon>
          <ele-Plus />
        </el-icon>
        新增
      </el-button>
      <el-button size="large" type="info" @click="handleRefresh">
        <el-icon>
          <ele-Refresh />
        </el-icon>
        刷新
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
      <el-table-column align="center" label="原始密码">
        <template #default="scope">
          <el-text>{{ scope.row["raw_password"] }}</el-text>
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template #default="scope">
          <el-text>{{ scope.row["comment"] }}</el-text>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作">
        <template #default="scope">
          <el-button
            size="small"
            type="danger"
            @click="handleDeleteRow(scope.row)"
            >删除</el-button
          >
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
      :hide-on-single-page="true"
      :page-size="recordsPerPage"
      :total="recordsTotal"
      background
      layout=" prev, pager, next"
      @current-change="handleCurrentChange"
    ></el-pagination>
  </div>
</template>

<style scoped></style>
