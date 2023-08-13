<script setup>
import { ref, onMounted, nextTick } from "vue";
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
  platform: {
    name: "默认平台",
    comment: "默认备注",
  },
};
const inputValue = ref("");
const inputVisible = ref(false);
const InputRef = ref(null);
const handleClose = (tag) => {
  ElMessageBox.confirm("确定要删除这个别名吗?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api.delete_platform_alias(tag["id"]).then((res) => {
        if (res.code) {
          ElNotification({
            title: "删除失败",
            message: res.message,
            type: "error",
          });
        } else {
          ElNotification({
            title: "删除成功",
            message: "已成功删除一个别名,正在刷新网页...",
            type: "success",
          });
          isTableLoading.value = true;
          setTimeout(() => {
            loadData();
          }, 200);
        }
      });
    })
    .catch(() => {
      ElNotification({
        title: "已取消",
        message: "已取消删除别名",
        type: "info",
      });
    });
};
const showInput = () => {
  inputVisible.value = true;
  nextTick(() => {
    InputRef.value.input.focus();
  });
};
const handleInputConfirm = (row) => {
  if (inputValue.value) {
    window.pywebview.api
      .add_platform_alias(row["id"], inputValue.value)
      .then((res) => {
        if (res.code) {
          ElNotification({
            title: "添加失败",
            message: res.message,
            type: "error",
          });
        } else {
          ElNotification({
            title: "添加成功",
            message: "已成功添加一个别名,正在刷新网页...",
            type: "success",
          });
          isTableLoading.value = true;
          setTimeout(() => {
            loadData();
          }, 200);
        }
      });
  }
  inputVisible.value = false;
  inputValue.value = "";
};
const loadData = () => {
  window.pywebview.api
    .search_platform(currentPage.value, recordsPerPage.value)
    .then((res) => {
      recordsOnPage.value = res.recordOnPage;
      tableData.value = res.data.map((item) => JSON.parse(item));
      tableData.value.forEach((item) => {
        window.pywebview.api.search_platform_alias(item["id"]).then((res) => {
          item["alias"] = res.data.map((item) => JSON.parse(item));
        });
        item["myAlias"] = "";
      });
      recordsTotal.value = res.total;
      newRow.value = JSON.parse(JSON.stringify(defaultValueOnMounted.platform));
      isTableLoading.value = false;
    });
};
//新增一条数据的弹窗
const handleAddDialog = () => {
  newRow.value = JSON.parse(JSON.stringify(defaultValueOnMounted.platform));
  isAddDialog.value = true;
};
//新增一条数据的提交
const handleAddNewRow = () => {
  ElMessageBox.confirm("确定要新增一个平台吗?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api
        .add_platform(newRow.value["name"], newRow.value["comment"])
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
              message: "已成功新增一个平台,正在刷新网页...",
              type: "success",
            });
            isAddDialog.value = false;
          }
        });
    })
    .catch(() => {
      ElNotification({
        title: "已取消",
        message: "已取消新增平台",
        type: "info",
      });
    });
};

//删除一条数据
const handleDeleteRow = (row) => {
  ElMessageBox.confirm("本平台和其别名将被删除, 是否继续?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api.delete_platform(row["id"]).then((res) => {
        if (res.code) {
          ElNotification({
            title: "删除失败",
            message: res.message,
            type: "error",
          });
        } else {
          ElNotification({
            title: "删除成功",
            message: "已彻底删除本平台和其别名" + row["raw_password"],
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
      <span> 新增平台 </span>
    </template>
    <el-form label-position="left" label-width="100px" style="max-width: 300px">
      <el-form-item label="平台名称">
        <el-input
          v-model="newRow['name']"
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
      <el-table-column align="center" label="平台名称" width="100">
        <template #default="scope">
          <el-text>{{ scope.row["name"] }}</el-text>
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注" width="100">
        <template #default="scope">
          <el-text>{{ scope.row["comment"] }}</el-text>
        </template>
      </el-table-column>
      <el-table-column align="center" label="别名">
        <template #default="scope">
          <el-tag
            v-for="item in scope.row['alias']"
            :key="item"
            closable
            type="info"
            @close="handleClose(item)"
          >
            <el-tooltip :content="item.comment" placement="top">
              <span>{{ item.name }}</span>
            </el-tooltip>
          </el-tag>
          <div style="display: inline-block">
            <el-input
              v-if="inputVisible"
              ref="InputRef"
              v-model="inputValue"
              size="small"
              @blur="handleInputConfirm(scope.row)"
              @keyup.enter="handleInputConfirm(scope.row)"
            />
            <el-button
              v-if="!inputVisible"
              class="button-new-tag ml-1"
              size="small"
              @click="showInput"
            >
              + 新的别名
            </el-button>
          </div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="100">
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
