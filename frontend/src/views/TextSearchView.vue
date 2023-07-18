<template>
  <div class="container">
    <div class="meal-wrapper">
      <div class="meal-search">
        <h2 class="title">Text Search For Your Fashion Styles</h2>
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

      <div class="meal-result" v-if="products.length">
        <h2 class="subtitle">{{ searchSumary }}</h2>
        <div class="product-card-list">
          <SearchCard 
            v-for="product in products" 
            :productName=product.productName
            :imgSrc=product.imgSrc
            :productURL=product.productURL
            :productDesc=product.productDesc
            :productPrice=product.productPrice
          ></SearchCard>
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
const products = ref([])

async function onSubmit() {
  const response = await fetch(`http://localhost:8000/search-by-word/?var=${keywords.value}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  const data = await response.json();
  console.log(data);
  searchSumary.value = `Your search results (${data.result[0].toLowerCase().slice(0, -1)}):`;
  console.log(searchSumary.value);
  products.value = data.result[1].map(
    (x) => { 
      return {
        productName: x.title,
        imgSrc: x.thumbnail,
        productURL: x.url_path,
        productDesc: x.desc,
        productPrice: x.price
      }
    }
  );
  console.log(products.value)

}

</script>


<style scoped>

</style>