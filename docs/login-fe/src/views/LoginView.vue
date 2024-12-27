<template>
  <div class="max-w-[400px] mx-auto p-5 border border-[#ccc] rounded-lg relative">
    <!-- Full-page spinner -->
    <div v-if="isLoading" class="fixed top-0 left-0 w-screen h-screen bg-white/80 flex justify-center items-center z-[1000]"> Loading </div>

    <!-- Login form -->
    <h2>Login</h2>
    <form @submit.prevent="handleSubmit">
      <TextBox
        id="username"
        label="Username"
        v-model="username"
        placeholder="Enter your username"
        :error="errors.username"
      />
      <TextBox
        id="password"
        label="Password"
        type="password"
        v-model="password"
        placeholder="Enter your password"
        :error="errors.password"
      />
      <button :disabled="isLoading" type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
  import { ref, reactive } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useRouter } from 'vue-router'
  import TextBox from "@/components/TextBox.vue"; // Import the TextBox component

  const router = useRouter() // Access the router

  // Reactive variables
  const authStore = useAuthStore()
  const username = ref('')
  const password = ref('')
  const isLoading = ref(false)
  const errors = reactive({
    username: '',
    password: ''
  })

  // Form validation
  const validateForm = () => {
    let isValid = true

    // Reset errors
    errors.username = ''; errors.password = '';

    if (!username.value) { errors.username = 'Username is required'; isValid = false; }
    if (!password.value) { errors.password = 'Password is required'; isValid = false; }

    return isValid
  }

  // Form submission
  const handleSubmit = async () => {
    if (!validateForm()) return

    isLoading.value = true // Start loading spinner
    try {
      // Simulate an API call
      const success = await authStore.login({
        email: username.value,
        password: password.value
      })
      if (success) {
        // alert("Login successful!");
        router.push({ name: 'home' })
      } else {
        alert('Authentication failed!')
      }
    } catch (error) {
      console.error('Login error:', error)
      alert('Something went wrong.')
    } finally {
      isLoading.value = false // Stop loading spinner
    }
  }
</script>

<style scoped>
form { @apply flex flex-col; }
label { @apply mb-1 font-bold; }
input { @apply mb-3 p-2.5 text-base border border-[#ccc] rounded-md; }
button { @apply p-2.5 bg-[#007bff] text-white text-base border-none rounded-md cursor-pointer; }
button:disabled { @apply bg-[#a0a0a0] cursor-not-allowed; }
button:hover:not(:disabled) { @apply bg-[#0056b3]; }
span { @apply text-red-500 text-[0.875rem]; }
</style>
