<template>
  <div class="max-w-[600px] m-auto p-[5px] text-center">
    <div v-if="isLoading" class="flex justify-center items-center h-screen"> loading </div>
    <div v-else>
      <h1>Welcome, {{ username }}!</h1>
      <p>Here’s the list of names:</p>
      <ul v-if="!error">
        <li v-for="(name, index) in names" :key="index">{{ name }}</li>
      </ul>
      <p v-else class="text-red-500 text-[1.2rem] mt-2.5">{{ error }}</p>
      <button @click="handleLogout">Logout</button>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useRouter } from 'vue-router'

  const authStore = useAuthStore()
  const router = useRouter()
  const username = authStore.user?.name || 'Guest User'
  const names = ref([])
  const isLoading = ref(true)
  const error = ref('')

  // Simulated API call
  const fetchNames = async () => {
    isLoading.value = true
    error.value = ''
    try {
      // Simulate API latency
      await new Promise((resolve) => setTimeout(resolve, 2000))
      // Simulate response
      const response = ['Alice', 'Bob', 'Charlie', 'Diana']
      names.value = response
    } catch (err) {
      error.value = 'Failed to load names. Please try again.'
    } finally {
      isLoading.value = false
    }
  }

  const handleLogout = () => {
    authStore.logout()
    router.push({ name: 'login' })
  }

  // Fetch names on component mount
  onMounted(fetchNames)
</script>

<style scoped>
  ul { @apply list-none p-0; }
  li { @apply py-[5px]; }
  button { @apply mt-5 p-2.5 bg-[#007bff] text-white text-base border-none rounded-md cursor-pointer; }
  button:hover { @apply bg-[#0056b3]; }
</style>
