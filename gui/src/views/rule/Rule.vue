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
//操作表格时该行的原始数据
let rowOrigin = {};
//控制dialog显示
const isMoreInfo = ref(false);
const isAddDialog = ref(false);
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

const loadData = () => {
  window.pywebview.api
    .search_rule(currentPage.value, recordsPerPage.value, false)
    .then((res) => {
      recordsOnPage.value = res.recordOnPage;
      tableData.value = res.data.map((item) => JSON.parse(item));
      recordsTotal.value = res.total;
      newRow.value = JSON.parse(JSON.stringify(defaultValueOnMounted.rule));
      isTableLoading.value = false;
    });
};
//新增一条数据的弹窗
const handleAddDialog = () => {
  newRow.value = JSON.parse(JSON.stringify(defaultValueOnMounted.rule));
  isAddDialog.value = true;
};
//新增一条数据的提交
const handleAddNewRow = () => {
  ElMessageBox.confirm("确定要新增一条规则吗?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api
        .add_rule(
          newRow.value["name"],
          newRow.value["min_length"],
          newRow.value["max_length"],
          newRow.value["lower_count"],
          newRow.value["upper_count"],
          newRow.value["number_count"],
          newRow.value["special_count"],
          newRow.value["comment"],
          false
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
    .catch(() => {
      ElNotification({
        title: "已取消",
        message: "已取消新增规则",
        type: "info",
      });
    });
};
//查看数据详细信息的弹窗
const handleMoreInfo = (row) => {
  rowCopy.value = JSON.parse(JSON.stringify(row));
  rowOrigin = JSON.parse(JSON.stringify(row));
  isMoreInfo.value = true;
};

//弃用一条数据
const handleDeprecateRow = () => {
  ElMessageBox.confirm("本条规则将进入回收站, 是否继续?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      window.pywebview.api.deprecate_rule(rowCopy.value["id"]).then((res) => {
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
    .update_rule(
      rowCopy.value["id"],
      rowCopy.value["min_length"],
      rowCopy.value["max_length"],
      rowCopy.value["lower_count"],
      rowCopy.value["upper_count"],
      rowCopy.value["number_count"],
      rowCopy.value["special_count"],
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
        <el-input-number
          v-model="rowCopy['min_length']"
          :min="4"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="最大长度">
        <el-input-number
          v-model="rowCopy['max_length']"
          :min="4"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="小写字母个数">
        <el-input-number
          v-model="rowCopy['lower_count']"
          :min="0"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="大写字母个数">
        <el-input-number
          v-model="rowCopy['upper_count']"
          :min="0"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="数字个数">
        <el-input-number
          v-model="rowCopy['number_count']"
          :min="0"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="特殊字符个数">
        <el-input-number
          v-model="rowCopy['special_count']"
          :min="0"
          clearable
        ></el-input-number>
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
    :center="true"
    draggable
    style="width: fit-content"
  >
    <template #header>
      <span> 新增规则 </span>
    </template>
    <el-form label-position="left" label-width="100px" style="max-width: 300px">
      <el-form-item label="规则名称">
        <el-input
          v-model="newRow['name']"
          :maxlength="20"
          clearable
          show-word-limit
        ></el-input>
      </el-form-item>
      <el-form-item label="最小长度">
        <el-input-number
          v-model="newRow['min_length']"
          :min="4"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="最大长度">
        <el-input-number
          v-model="newRow['max_length']"
          :min="4"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="小写字母个数">
        <el-input-number
          v-model="newRow['lower_count']"
          :min="0"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="大写字母个数">
        <el-input-number
          v-model="newRow['upper_count']"
          :min="0"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="数字个数">
        <el-input-number
          v-model="newRow['number_count']"
          :min="0"
          clearable
        ></el-input-number>
      </el-form-item>
      <el-form-item label="特殊字符个数">
        <el-input-number
          v-model="newRow['special_count']"
          :min="0"
          clearable
        ></el-input-number>
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
      <el-button
        size="large"
        type="warning"
        @click="router.push('/ruleRubbish')"
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
        fixed
        type="index"
        width="60"
        align="center"
        label="序号"
      >
      </el-table-column>
      <!-- 数据展示 -->
      <el-table-column label="规则名称" align="center">
        <template #default="scope">
          <el-text>{{ scope.row["name"] }}</el-text>
        </template>
      </el-table-column>
      <el-table-column label="备注" align="center">
        <template #default="scope">
          <el-text>{{ scope.row["comment"] }}</el-text>
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
