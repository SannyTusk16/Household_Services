<template>
  <div id="app">
    <nav class="navigation-bar">
      <div class="nav-container">
      </div>
    </nav>
    <router-view>
    </router-view>
  </div>
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100vh;
  overflow: hidden;
  border: 0;
  background-color: rgb(207, 231, 222);
}

.navigation-bar {
  padding: 1px 0;
  text-align: center;
}

.nav-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.nav-container h2 {
  margin-right: auto;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
}

nav a.router-link-exact-active {
  color: #42b983;
  text-decoration: underline;
}
</style>
<script>
import api from "@/api";
export default {
  name: "App",
};
</script>
<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  box-sizing: border-box;
}
</style>