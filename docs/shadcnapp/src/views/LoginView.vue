<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-vue-next'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

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

<template>
  <Card class="w-[350px]">
    <CardHeader>
      <CardTitle>Login</CardTitle>
    </CardHeader>
    <CardContent>
      <form @submit.prevent="handleSubmit">
        <TextBox id="username" label="Username" v-model="username" placeholder="username" :error="errors.username" />
        <TextBox id="password" label="Password" type="password" v-model="password" placeholder="password"
          :error="errors.password" />
          <Button :disabled="isLoading" type="submit">
        <Loader2 v-if="isLoading" class="animate-spin" />
        Login
      </Button>
      </form>
    </CardContent>
  </Card>
</template>