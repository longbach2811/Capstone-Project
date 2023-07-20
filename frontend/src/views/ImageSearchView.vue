<template>
  <div class="container">
    <div class="meal-wrapper">
      <div class="meal-search">
        <h2 class="title">Image Search For Your Fashion Styles</h2>
        <blockquote>One look is worth a thousand words.<br>
          <cite>- Fred R. Barnard</cite>
        </blockquote>

        <!-- <form class="meal-search-box" @submit.prevent="onSubmit">
          <input v-model="keywords" type="text" class="search-control" placeholder="Enter an item" id="search-input">
          <button type="submit" class="search-btn btn" id="search-btn">
            <i class="fas fa-search"></i>
          </button>
        </form> -->

        <div class="upload-container" @input.prevent="onInput">
          <input type="file" ref="file" accept="image/jpeg, image/png, image/jpg" hidden @change="onFileChange">
          <div class="img-container">
            <div v-if="!imagePreviewURL" class="img-area" >
              <i class='bx bxs-cloud-upload icon'></i>
              <h3>Upload Image</h3>
              <p>Image size must be less than <span>2MB</span></p>
            </div>
            <img v-else :src="imagePreviewURL" class="img-content-preview" @click="$refs.file.click()" />
            <button class="select-image" @click="$refs.file.click()">Upload</button>
          </div>

        </div>

        <div class="meal-result" v-if="products.length">
        <h2 class="subtitle">{{ searchSumary }}</h2>
        <div class="product-card-list">
          <SearchCard v-for="product in products" :productName=product.productName :imgSrc=product.imgSrc
            :productURL=product.productURL :productDesc=product.productDesc :productPrice=product.productPrice>
          </SearchCard>
        </div>
      </div>

      </div>
    </div>
  </div>
</template>

<script>
// import { Buffer } from "buffer";
import SearchCard from '../components/SearchCard.vue';

export default {
  components: {SearchCard},
  data() {
    return {
      imagePreviewURL: null,
      imageFile: null,
      products: [],
      searchSumary: '',
    }
  },
  methods: {
    onFileChange() {
      let input = this.$refs.file
      let file = input.files
      if (file && file[0]) {
        let reader = new FileReader

        reader.onload = e => {
          this.imagePreviewURL = e.target.result
          this.uploadFile(e.target.result)
        }
        reader.readAsDataURL(file[0])

      }
      
    },
    async uploadFile(base64) {
      // console.log(base64)
      let res = await fetch(base64);
      let blob = await res?.blob();
      console.log(blob)



      // const buffer = Buffer.from(base64, "base64");
      // const blob = new Blob([buffer], { type: '[content-type]' })
      // console.log(blob)

      let formData = new FormData();
      formData.append('file', blob);
      const response = await fetch(
        'http://localhost:8000/search-by-image/', {
          method: 'POST',
          body: formData,
        }
      );
      const data = await response.json();
      this.searchSumary = `Your search results (${data.result[0].toLowerCase().slice(0, -1)}):`;
      this.products = data.result[1].map(
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
      console.log(this.products);
    }
    
  },
}

</script>

<style scoped>
.upload-container {
  max-width: 300px;
  width: 100%;
  background: #ede6e6;
  padding: 30px;
  border-radius: 30px;
  margin: 1.5rem auto;
}

.img-content-preview {
  /* object-fit: fill; */
  width: 100%;
  height: auto;
  margin-bottom: 30px;
  border-radius: 15px;
  cursor: pointer;
  /* width: auto; */
  /* height: auto; */
}

.img-area {
  position: relative;
  width: 100%;
  height: 160px;
  background: #dccabf;
  margin-bottom: 30px;
  border-radius: 15px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  /* cursor: pointer; */
}

.img-area .icon {
  font-size: 60px;
}

.img-area h3 {
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 6px;
}

.img-area p {
  color: #000000;
}

.img-area p span {
  font-weight: 600;
}

.img-area img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  z-index: 100;
}

.img-area::before {
  content: attr(data-img);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, .5);
  color: #731010;
  font-weight: 500;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none;
  opacity: 0;
  transition: all .3s ease;
  z-index: 200;
}

.img-area.active:hover::before {
  opacity: 1;
}

.select-image {
  display: block;
  width: 100%;
  padding: 16px 0;
  border-radius: 15px;
  background: var(--tenne-tawny);
  color: #fafafa;
  font-weight: 500;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all .3s ease;
}

.select-image:hover {
  background: var(--tenne-tawny-dark);
}
</style>