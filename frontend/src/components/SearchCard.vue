<template>
  <figure class="snip1418">
    <img :src=imgSrc alt="sample85" />
    <!-- <div class="add-to-cart"> <i class="ion-android-add"></i><span>Add to Cart</span></div> -->
    <figcaption>
      <h3>{{ productName }}</h3>
      <p>{{ productDesc }}</p>
      <div class="price">
        {{ productPrice }}
      </div>
    </figcaption><a :href=productURL target="_blank"></a>
  </figure>
</template>

<script setup>

import { ref } from 'vue'
// const imgSrc = ref('https://s3-us-west-2.amazonaws.com/s.cdpn.io/331810/sample85.jpg')
const props = defineProps({
  imgSrc: {
    type: String,
    default: 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/331810/sample85.jpg',
  },
  productName: {
    type: String,
    default: 'Pudol Doux',
  },
  productDesc: {
    type: String,
    default: 'All this modern technology just makes people try to do everything at once.',
  },
  productPrice: {
    type: String,
    default: '$24.00',
  },
  productURL: {
    type: String,
    default: 'https://google.com'
  }
})
</script>

<style scoped>
.snip1418 {
  font-family: 'Raleway', Arial, sans-serif;
  position: relative;
  overflow: hidden;
  /* margin: 10px; */
  /* min-width: 230px;
  max-width: 315px; */
  /* width: 100%; */
  width: calc(25% - 10px);
  margin-left: 10px;
  margin-top: 10px;
  background: #ffffff;
  text-align: left;
  color: #000000;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
  font-size: 16px;
  -webkit-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-perspective: 20em;
  perspective: 20em;
}

.snip1418 * {
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  -webkit-transition: all 0.3s ease-out;
  transition: all 0.3s ease-out;
}

.snip1418 img {
  max-width: 100%;
  /* height: 20rem; */
  vertical-align: top;
  position: relative;
}

.snip1418 .add-to-cart {
  position: absolute;
  top: 0;
  right: 0;
  padding-right: 10px;
  color: #ffffff;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.9em;
  opacity: 0;
  background-color: #409ad5;
  -webkit-transform: rotateX(-90deg);
  transform: rotateX(-90deg);
  -webkit-transform-origin: 100% 0;
  -ms-transform-origin: 100% 0;
  transform-origin: 100% 0;
}

.snip1418 .add-to-cart i {
  display: inline-block;
  margin-right: 10px;
  width: 40px;
  line-height: 40px;
  text-align: center;
  background-color: #164666;
  color: #ffffff;
  font-size: 1.4em;
}

.snip1418 figcaption {
  padding: 20px;
}

.snip1418 h3,
.snip1418 p {
  margin: 0;
}

.snip1418 h3 {
  font-size: 1.1em;
  font-weight: 700;
  margin-bottom: 10px;
  text-transform: uppercase;
}

.snip1418 p {
  font-size: 0.9em;
  letter-spacing: 1px;
  font-weight: 400;
}

.snip1418 .price {
  font-weight: 500;
  font-size: 1.5em;
  line-height: 48px;
  letter-spacing: 1px;
}

.snip1418 .price s {
  margin-right: 5px;
  opacity: 0.5;
  font-size: 0.9em;
}

.snip1418 a {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}

.snip1418:hover img {
  transform: scale(1.1);
}

@media screen and (max-width: 1200px) {
  .snip1418 {
    width: calc(33% - 10px);
  }

}

@media screen and (max-width: 800px) {
  .snip1418 {
    width: calc(50% - 10px);
  }

}</style>