import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import AboutView from "../views/AboutView.vue";
import ProfessionalDetailsView from "../views/ProfessionalDetailsView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/home",
    name: "home",
    component: HomeView,
  },
  {
    path: "/",
    name: "login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/about",
    name: "about",
    component: AboutView,
  },
  {
    path: "/professionalDetails",
    name: "professionalDetails",
    component: ProfessionalDetailsView,
  }
];

const router = new VueRouter({
  mode: "history",
  base: "/",
  routes,
});

export default router;
