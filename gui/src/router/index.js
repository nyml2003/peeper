import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Layout",
    component: () => import("@/views/AppLayout.vue"),
    redirect: "/home",
    children: [
      {
        path: "home",
        name: "Home",
        component: () => import("@/views/home/HomeView.vue"),
      },
      {
        path: "rule",
        name: "Rule",
        component: () => import("@/views/rule/Rule.vue"),
      },
      {
        path: "ruleRubbish",
        name: "RuleRubbish",
        component: () => import("@/views/rule/RuleRubbish.vue"),
      },
      {
        path: "platform",
        name: "Platform",
        component: () => import("@/views/platform/PlatformManage.vue"),
      },
      {
        path: "rawPassword",
        name: "RawPassword",
        component: () => import("@/views/rawPassword/RawPassword.vue"),
      },
      {
        path: "user",
        name: "User",
        component: () => import("@/views/user/User.vue"),
      },
      {
        path: "userRubbish",
        name: "UserRubbish",
        component: () => import("@/views/user/UserRubbish.vue"),
      },
    ],
  },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// router.beforeEach((to, from, next) => {
//   if (to.path === "/login") {
//     next();
//   } else {
//     const admin = Cookies.get("admin");
//     if (!admin && to.path !== "/login") {
//       next("/login");
//     } else {
//       next();
//     }
//   }
// });

export default router;
