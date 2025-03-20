<template>
  <div class="service-tile" @mouseover="hover = true" @mouseleave="hover = false" @click="goToService">
    <div class="service-content">
      <h3 class="service-name">{{ name }}</h3>
      <p class="service-price">${{ price.toFixed(2) }}</p>
    </div>

    <transition name="fade">
      <div v-if="hover" class="service-description">
        {{ description }}
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "ServiceComponent",
  data() {
    return {
      hover: false,
    };
  },
  props: {
    name: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    price: {
      type: Number,
      required: true,
    },
    serviceId: {
      type: Number,
      required: true,
    },
  },
  methods: {
    goToService() {
      this.$router.push({ path: "/about", query: { id: this.serviceId } });
      localStorage.setItem("service_id", this.serviceId);
    },
  },
};
</script>

<style scoped>
.service-tile {
  position: relative;
  width: 250px;
  height: 160px;
  padding: 15px;
  background: #ffffff;
  border: 2px solid #001429;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden; /* Prevents description from overflowing */
}

.service-content {
  width: 100%;
}

.service-name {
  font-size: 18px;
  font-weight: bold;
  color: #000000;
  margin-bottom: 5px;
}

.service-price {
  font-size: 16px;
  font-weight: bold;
  color: #28a745;
  margin-bottom: 10px;
}

/* Description Box - Now perfectly inside the tile */
.service-description {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 8px;
  text-align: center;
  border-radius: 0 0 10px 10px;
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
  box-sizing: border-box; /* Ensures it stays inside */
  overflow: hidden;
  white-space: nowrap; /* Prevents line breaks */
  text-overflow: ellipsis; /* Adds "..." if text is too long */
}

/* Ensure description doesn't overflow */
.service-tile:hover .service-description {
  opacity: 1;
}

/* Smooth fade effect */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
