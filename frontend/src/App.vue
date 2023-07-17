<script setup>
import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <nav class="navbar">
      <!-- <div class="logo">
            <img src="src\components\icons\logo.png" alt="">
          </div>    
          <div class="lang">
            <select id="language">
              <option value="en">EN</option>
              <option value="vn">VN</option>
            </select>
        </div>
        <div class="user">
          <img src="https://via.placeholder.com/50x50.png?text=User" alt="User">
        </div> -->

      <div class="navbar-title">Fashion Search</div>

      <a href="#" class="toggle-button">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </a>

      <div class="navbar-link">
        <ul>
          <!-- <li><a href="#">Home</a></li>
          <li><a href="#">About</a></li>
          <li><a href="#">Contact</a></li> -->
          <li><router-link to="/">Text</router-link></li>
          <li><router-link to="/">Image</router-link></li>
        </ul>
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



.navbar {
    width: 100%;
    max-width: 100wh;
    height: 4rem;
    margin: 0 auto;
    padding: 0 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    background: var(--tenne-tawny);
    color: #FAFAFA;
}

.navbar-title {
    font-size: 1.5rem;
    margin: 0.5rem;
    text-transform: uppercase;
}

.navbar-link {
    height: 100%;
}

.navbar-link ul {
    display: flex;
    margin: 0;
    padding: 0;
}

.navbar-link li {
    list-style: none;
    transition: 0.5s;
}

.navbar-link li a {
    display: block;
    text-decoration: none;
    color: #FAFAFA;
    padding: 1rem;
    transition: 0.5s;
}

.navbar-link li a:hover {
    color: black;
}

.toggle-button {
    position: absolute;
    top: 1.75rem;
    right: 1rem;
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
}

.toggle-button .bar {
    height: 3px;
    width: 100%;
    background-color: #FAFAFA;
    border-radius: 10px;
}


</style>
