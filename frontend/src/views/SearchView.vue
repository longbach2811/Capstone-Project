<template>
  <div class="container">
    <div class="meal-wrapper">
      <div class="meal-search">
        <h2 class="title">Find Fashion Items For Your Styles</h2>
        <blockquote>Fashion is the armor to survive the relity of everyday life.<br>
          <cite>- Bill Cunningham</cite>
        </blockquote>

        <form class="meal-search-box" @submit.prevent="onSubmit">
          <input v-model="keywords" type="text" class="search-control" placeholder="Enter an item" id="search-input">
          <button type="submit" class="search-btn btn" id="search-btn">
            <i class="fas fa-search"></i>
          </button>
        </form>
      </div>

      <div class="meal-result" v-if="isHavingData">
        <h2 class="subtitle">{{ searchSumary }}</h2>
        <div class="product-card-list">
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
          <SearchCard class="product-card"/>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>

import { ref } from 'vue'
import SearchCard from '../components/SearchCard.vue'
const keywords = ref('')
const searchSumary = ref('')
const isHavingData = ref(false)

async function onSubmit() {
  const response = await fetch(`http://localhost:8000/search-by-word/?var=${keywords.value}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  const data = await response.json();
  console.log(data);
  searchSumary.value = `Your search results (${data.result[0].toLowerCase().slice(0, -1)}):`;
  isHavingData.value = true;
  console.log(searchSumary.value);

}

</script>


<style scoped>
.btn {
  font-family: inherit;
  cursor: pointer;
  outline: 0;
  font-size: 1.05rem;
}

.text {
  opacity: 0.8;
}

.title {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.container {
  min-height: calc(100vh-4rem);
}

.meal-wrapper {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  background: #fff;
  text-align: center;
}

.meal-search {
  margin: 2rem 0;
}

.meal-search cite {
  font-size: 1rem;
}

.meal-search-box {
  margin: 1.2rem 0;
  display: flex;
  align-items: stretch;
}

.search-control,
.search-btn {
  width: 100%;
}

.search-control {
  padding: 0 1rem;
  font-size: 1.1rem;
  font-family: inherit;
  outline: 0;
  border: 1px solid var(--tenne-tawny);
  color: var(--tenne-tawny);
  border-top-left-radius: 2rem;
  border-bottom-left-radius: 2rem;
}

.search-control::placeholder {
  color: var(--tenne-tawny);
}

.search-btn {
  width: 55px;
  height: 55px;
  font-size: 1.8rem;
  background: var(--tenne-tawny);
  color: #fff;
  border: none;
  border-top-right-radius: 2rem;
  border-bottom-right-radius: 2rem;
  transition: all 0.4s linear;
  -webkit-transition: all 0.4s linear;
  -moz-transition: all 0.4s linear;
  -ms-transition: all 0.4s linear;
  -o-transition: all 0.4s linear;
}

.search-btn:hover {
  background: var(--tenne-tawny-dark);
}

.product-card-list {
  display: flex;
  flex-wrap: wrap;
  margin-top: -10px;
  margin-left: -10px;
}


/* Media Queries */
@media screen and (min-width: 600px) {
  .meal-search-box {
    width: 540px;
    margin-left: auto;
    margin-right: auto;
  }
}</style>