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
  background-color: #1e1e1e; /* Black background */
  color: #dcdcdc;            /* White text */
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  min-height: 100vh;
  background-color: #1e1e1e; /* Ensure root app container is black too */
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

.style-btn {
    background-color: #4b4848;
    color: white;
    border: 1px solid #666;
    padding: 10px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9em;
    transition: background-color 0.2s;
  }
  
  .style-btn:hover {
    background-color: #5a5757;
  }
  
  .style-btn:active {
    background-color: #3a3a3a;
  }
  .sidebar-buttons {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .style-dropdown {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #666;
    border-radius: 6px;
    background-color: #4b4848;
    color: white;
    font-size: 0.9em;
  }
  
  .style-dropdown:focus {
    outline: none;
    border-color: #888;
    background-color: #5a5757;
  }
  .exit-btn {
  color: red; 
  cursor: pointer; 
  float: right; 
  font-weight: bold; 
  font-size: 1.5rem;
}
.exit-btn:hover {
  color: rgb(201, 0, 0); 
}
  
</style>
