<script setup>
import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
      <nav>
        <div class="logo">
            <img src="src\components\icons\logo.png" alt="">
          </div>    
          <div class="lang">
            <!-- <label for="language">Language:</label> -->
            <select id="language">
              <option value="en">EN</option>
              <option value="vn">VN</option>
            </select>
        </div>
        <div class="user">
          <img src="https://via.placeholder.com/50x50.png?text=User" alt="User">
        </div>
      </nav>
  </header>
  <main>
    <RouterView />
  </main>
<!-- 
  <footer>
    <div class="container">
      <p>&copy; All rights reserved.</p>
    </div>
  </footer> -->
</template>

<style scoped>
  nav {
    display: flex;
    justify-content: flex-end;
    background-color: rgb(254, 254, 252);
    padding: 16px 0;
    border-bottom: 1px solid #c9c8c8;
  }

  .lang {
    display: flex;
    margin-right: 10px;
    justify-content: center;
    align-items: center;
    margin-right: 20px;
  }

  .logo {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-grow: 1;
    /* width: 5px; */
  }

  .logo img {
    width: 70px;
    height: 35px;
  }

  .user {
    margin-right: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    overflow: hidden;
  }

  footer {
    background-color: #f1f1f1;
    padding: 20px;
    text-align: center;
    font-size: 14px;
    color: #888;
    display: flex;
    align-self: flex-end;
  }

  footer .container {
    max-width: 1200px;
    margin: 0 auto;
  }

  footer .container p {
    margin: 0;
  }

</style>
