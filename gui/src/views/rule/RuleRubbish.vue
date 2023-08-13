<script setup>
import { ref, onMounted } from "vue";
import { ElMessageBox, ElNotification } from "element-plus";
import { useRouter } from "vue-router";

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
//控制dialog显示
const isMoreInfo = ref(false);
//table是否在加载状态
const isTableLoading = ref(true);
//多次使用的默认值
const defaultValueOnMounted = {
  rule: {
    name: "默认规则",
    min_length: 8,
    max_length: 12,
    lower_count: 1,
    upper_count: 1,
    number_count: 1,
    special_count: 1,
    comment: "默认备注",
  },
};

const handleMoreInfo = (row) => {
  rowCopy.value = JSON.parse(JSON.stringify(row));
  isMoreInfo.value = true;
};

const loadData = () => {
  window.pywebview.api
    .search_rule(currentPage.value, recordsPerPage.value, true)
    .then((res) => {
      recordsOnPage.value = res.recordOnPage;
      tableData.value = res.data.map((item) => JSON.parse(item));
      recordsTotal.value = res.total;
      newRow.value = JSON.parse(JSON.stringify(defaultValueOnMounted.rule));
      isTableLoading.value = false;
    });
};
//彻底删除一条数据
const handleDelRow = () => {
  ElMessageBox.confirm("本条规则将被彻底删除, 是否继续?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api.del_rule(rowCopy.value["id"]).then((res) => {
        if (res.code) {
          ElNotification({
            title: "删除失败",
            message: res.message,
            type: "error",
          });
        } else {
          ElNotification({
            title: "彻底删除成功",
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
//还原
const handleEnableRow = () => {
  window.pywebview.api.enable_rule(rowCopy.value["id"]).then((res) => {
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
      <el-form-item label="最小长度">
        <el-text>{{ rowCopy["min_length"] }}</el-text>
      </el-form-item>
      <el-form-item label="最大长度">
        <el-text>{{ rowCopy["max_length"] }}</el-text>
      </el-form-item>
      <el-form-item label="小写字母数量">
        <el-text>{{ rowCopy["lower_count"] }}</el-text>
      </el-form-item>
      <el-form-item label="大写字母数量">
        <el-text>{{ rowCopy["upper_count"] }}</el-text>
      </el-form-item>
      <el-form-item label="数字数量">
        <el-text>{{ rowCopy["number_count"] }}</el-text>
      </el-form-item>
      <el-form-item label="特殊字符数量">
        <el-text>{{ rowCopy["special_count"] }}</el-text>
      </el-form-item>
      <el-form-item label="备注">
        <el-text>{{ rowCopy["comment"] }}</el-text>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button-group>
        <el-button type="danger" @click="handleDelRow">彻底删除</el-button>
        <el-button type="warning" @click="handleEnableRow">还原</el-button>
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
      <el-button size="large" type="warning" @click="router.push('/rule')">
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
      <el-table-column align="center" label="规则名称">
        <template #default="scope">
          <el-text>{{ scope.row["name"] }}</el-text>
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template #default="scope">
          <el-text>{{ scope.row["comment"] }}</el-text>
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
