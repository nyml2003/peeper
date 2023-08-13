import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

// 组件库 ElementPlus
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "element-plus/theme-chalk/dark/css-vars.css"; // 暗黑模式
app.use(ElementPlus);

// 图标库 ElementPlus
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(`ele-${key}`, component);
}

import { install } from "@icon-park/vue-next/es/all";

install(app);
// 自定义图标库
import SvgIcon from "@/components/SvgIcon/index.vue";

app.component("SvgIcon", SvgIcon);

// 自定义样式
import "@/assets/main.scss";

// //防抖
// const debounce = (fn, delay) => {
//   let timer = null;
//   return function () {
//     let context = this;
//     let args = arguments;
//     clearTimeout(timer);
//     timer = setTimeout(function () {
//       fn.apply(context, args);
//     }, delay);
//   }
// }

app.use(router).mount("#app");
