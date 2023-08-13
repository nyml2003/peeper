<template>
  <div style="user-select: none">
    <!-- 头部区域 -->
    <div class="header">
      <div class="logo">
        <img alt="logo" src="@/assets/logo/logo.png" />
        <span>窥秘人</span>
      </div>

      <div class="function">
        <el-dropdown size="large" style="top: 20px; margin-right: 24px">
          <span>
            <translate fill="#333" size="24" theme="outline" />
          </span>
          <template #dropdown>
            <el-dropdown-item>中文</el-dropdown-item>
            <el-dropdown-item>English</el-dropdown-item>
          </template>
        </el-dropdown>
        <el-switch
          v-model="isDark"
          :active-icon="Moon"
          :inactive-icon="Sunny"
          inline-prompt
          size="large"
          style="margin-right: 20px"
        ></el-switch>
        <el-button size="large" type="info">
          <el-icon>
            <ele-InfoFilled />
          </el-icon>
          <span> 关于 </span>
        </el-button>
        <el-button size="large" type="danger">
          <el-icon>
            <ele-SwitchButton />
          </el-icon>
          <span> 注销 </span>
        </el-button>
      </div>
    </div>

     <!-- 侧边栏和主体 -->
        <div style="display: flex">
          <!-- 侧边栏导航 -->
          <div ref="sideBar" class="sidebar">
            <el-button
              circle
              class="lock"
              size="large"
              style="border: none"
              @click="toggleSidebar"
            >
              <Pushpin
                v-if="isMenuExpanded"
                :strokeWidth="1"
                fill="#409eff"
                size="24"
                theme="filled"
              />
              <Pushpin
                v-else
                :strokeWidth="1"
                fill="#dbe0e2"
                size="24"
                theme="filled"
              />
            </el-button>
            <el-menu
              :collapse="!(isMenuExpanded || isMouseInside)"
              :default-active="$route.path"
              router
              style="margin-bottom: 10px"
            >
              <el-menu-item index="/">
                <template #title>
                  <span> 首页 </span>
                </template>
                <template #default>
                  <el-icon>
                    <HomeTwo
                      :strokeWidth="1"
                      fill="#333"
                      size="24"
                      theme="filled"
                    />
                  </el-icon>
                </template>
              </el-menu-item>

              <el-menu-item index="/rule">
                <template #title>
                  <span> 规则管理 </span>
                </template>
                <template #default>
                  <el-icon>
                    <Agreement
                      :strokeWidth="1"
                      fill="#333"
                      size="24"
                      theme="filled"
                    />
                  </el-icon>
                </template>
              </el-menu-item>
              <el-menu-item index="/platform">
                <template #title>
                  <span> 平台管理 </span>
                </template>
                <template #default>
                  <el-icon>
                    <ApiApp :strokeWidth="1" fill="#333" size="24" theme="filled" />
                  </el-icon>
                </template>
              </el-menu-item>
              <el-menu-item index="/rawPassword">
                <template #title>
                  <span> 原始密码 </span>
                </template>
                <template #default>
                  <el-icon>
                    <ElectronicDoorLock
                      :strokeWidth="1"
                      fill="#333"
                      size="24"
                      theme="filled"
                    />
                  </el-icon>
                </template>
              </el-menu-item>
              <el-menu-item index="/user">
                <template #title>
                  <span> 用户管理 </span>
                </template>
                <template #default>
                  <el-icon>
                    <User :strokeWidth="1" fill="#333" size="24" theme="filled" />
                  </el-icon>
                </template>
              </el-menu-item>
            </el-menu>
          </div>

          <!-- 主体数据 -->
          <!-- width: 0; 可以限制容器的宽度，不被子元素无限撑开-->
          <div style="flex: 1; width: 0; padding: 10px">
                   <router-view />
          </div>
        </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  HomeTwo,
  Translate,
  Pushpin,
  Moon,
  Sunny,
  Agreement,
  ApiApp,
  ElectronicDoorLock,
  User,
} from "@icon-park/vue-next";

import { useDark } from "@vueuse/core";

const isDark = useDark();
const sideBar = ref(null);
const isMouseInside = ref(false);
const isMenuExpanded = ref(false);

const handleMouseEnter = () => {
  if (isMenuExpanded.value) {
    return;
  }
  isMouseInside.value = true;
};

const handleMouseLeave = () => {
  if (isMenuExpanded.value) {
    return;
  }
  isMouseInside.value = false;
};
const toggleSidebar = () => {
  isMenuExpanded.value = !isMenuExpanded.value;
  const sidebar = document.querySelector(".sidebar");
  if (isMenuExpanded.value) {
    sidebar.classList.remove("collapse");
    sidebar.classList.add("expanded");
  } else {
    sidebar.classList.remove("expanded");
    sidebar.classList.add("collapse");
  }
};
onMounted(() => {
  sideBar.value.addEventListener("mouseenter", handleMouseEnter);
  sideBar.value.addEventListener("mouseleave", handleMouseLeave);
});

// onUnmounted(() => {
//   sideBar.value.removeEventListener('mouseenter', handleMouseEnter);
//   sideBar.value.removeEventListener('mouseleave', handleMouseLeave);
// });
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 64px;
  min-height: calc(100vh - 62px);
  overflow: hidden;
  margin-right: 2px;
  transition: width 0.3s ease-in-out;
}

.sidebar:hover {
  width: 100px;
}

.expanded {
  width: 100px;
}

.collapse {
  width: 64px;
}

.lock {
  top: 10px;
  border-color: #cbcbcd;
  color: #505255;
}

.lock:hover {
  border-color: #c6e2ff;
  color: #409eff;
}

.header {
  height: 60px;
  line-height: 60px;
  display: flex;
  margin: 10px 10px 20px;
}

.logo img {
  left: 20px;
  top: 10px;
  position: relative;
}

.logo span {
  left: 20px;
  position: relative;
}

.function {
  flex: 1;
  text-align: right;
  padding-right: 20px;
}

.el-menu {
  border-right: 0;
}

.el-menu-item * {
  display: flex;
  align-items: flex-end;
}
</style>
