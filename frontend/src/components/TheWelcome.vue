<template>
  <div class="search-bar">
    
    <form>
      <div class="search-wrapper">
        <input type="text" placeholder="Search..." @input="handleInput" ref="input">
        <!-- <div class="image-upload" @dragover="handleDragOver" @drop="handleDrop">
        </div> -->
      </div>
      <button type="submit" @click.prevent="handleSubmit"><i class="fa fa-search"></i></button>
    </form>
  </div>

</template>

<script>
  export default {
    methods: {
      handleInput(event) {
        console.log("Input changed:", event.target.value);
      },
      handleDragOver(event) {
        event.preventDefault();
        console.log("Dragging over...");
      },
      handleDrop(event) {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        console.log("Dropped file:", file.name);
      },
      handleUpload(event) {
        const file = event.target.files[0];
        console.log("Uploaded file:", file, file.name);
      },
      async handleSubmit() {
        const input = this.$refs.input.value;
        const file = this.$refs.file.files[0];

        if (input && !file) {
          const response = await fetch('http://localhost:8000/search-by-word/', {
            method: 'POST',
            body: JSON.stringify({text: input}),
            headers: {'Content-Type': 'application/json'}
          });
          const data = await response.json();
          console.log('Search result:', data);
        } else if (file && !input) {
          const formData = new FormData();
          formData.append('image', file, file.name);
          // formData.append('filename', file.name);
          // this.uploadService.imageUpload(formData).subscribe((res) => {
          //           console.log('image upload success', res);
          //         });
          const response = await fetch('http://localhost:8000/search-by-image/', {
            method: 'POST',
            body: formData
          });
          const data = await response.json();
          console.log('Search result:', data);
        }
      }
    }
  }
</script>

<style>

  .logo {
    margin-bottom: 20px;
  }

  .search-bar {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    justify-content: center;
    align-items: center;
    width: 1000px;
    border-radius: 30px;
    border: 3px solid #ccc;
    padding: 10px;
  }

  .logo-search {
    position: absolute;
    left: 10px;
  }

  .logo-search img {
    height: 30px;
  }

  form {
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    border-radius: 30px;
    margin-right: 4px;
  }

  input[type="text"] {
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 30px 0 0 30px;
    font-size: 18px;
    background-color: transparent;
    margin-right: -5px;
    width:900px;
  }

  button[type="submit"] {
    padding: 20px;
    background-color: #4285f4;
    color: white;
    border: none;
    border-radius: 30px;
    font-size: 18px;
    cursor: pointer;
  }


</style>