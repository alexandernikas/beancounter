<template>
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav> -->
  <router-view/>
</template>

<style>
/* universal styling */
/* * {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
} */
html, body {
  margin: 0;
  padding: 0;
  background-color: #000; /* Black background */
  color: #dcdcdc;            /* White text */
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  min-height: 100vh;
  background-color: #000; /* Ensure root app container is black too */
  color: #fff;
}

nav {
  padding: 30px;
  
}

nav a {
  font-weight: bold;
  color: #e2e2e2;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
