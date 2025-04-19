import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const options = {
  transition: "Vue-Toastification__fade",
  maxToasts: 3,
  timeout: 3000
};

// ✅ Register Toast globally with Vue
Vue.use(Toast, options);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
