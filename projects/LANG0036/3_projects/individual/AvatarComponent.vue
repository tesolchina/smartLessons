<template>
  <div
    class="relative w-48 h-48 rounded-full mx-auto transition-all duration-300"
    :class="faceClasses"
  >
    <!-- Eyes -->
    <div class="absolute top-14 left-12 w-24 h-6 bg-white rounded-full overflow-hidden">
      <div
        class="absolute bg-gray-800 rounded-full w-5 h-5 top-0.5 transition-all duration-300"
        :class="['left-4']"
      ></div>
      <div
        class="absolute bg-gray-800 rounded-full w-5 h-5 top-0.5 transition-all duration-300"
        :class="['right-4']"
      ></div>
    </div>

    <!-- Mouth -->
    <div
      class="absolute bottom-14 left-1/2 -translate-x-1/2 w-12 h-3 bg-gray-800 rounded-full transition-transform duration-300"
      :class="{ 'animate-talk': state === 'speaking' }"
    ></div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  state: {
    type: String,
    default: "idle", // idle | listening | speaking | thinking
  },
  gradientFrom: {
    type: String,
    default: "from-indigo-500",
  },
  gradientTo: {
    type: String,
    default: "to-purple-600",
  },
});

const faceClasses = computed(() => {
  return [
    "bg-gradient-to-br",
    props.gradientFrom,
    props.gradientTo,
    props.state === "listening" ? "animate-pulse shadow-xl shadow-indigo-400/50" : "",
    props.state === "speaking" ? "animate-glow" : "",
  ];
});
</script>

<style scoped>
@keyframes glow {
  0% {
    box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
  }
  100% {
    box-shadow: 0 0 40px rgba(102, 126, 234, 0.8);
  }
}

.animate-glow {
  animation: glow 1s infinite alternate;
}

@keyframes talk {
  0% {
    transform: scaleY(1);
  }
  100% {
    transform: scaleY(2);
  }
}

.animate-talk {
  animation: talk 0.5s infinite alternate;
  transform-origin: center bottom;
}
</style>
