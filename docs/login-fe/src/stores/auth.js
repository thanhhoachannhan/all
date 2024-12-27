import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false)
  const user = ref(null)
  const logout = () => { isLoggedIn.value = false; user.value = null; }
  const isAuthenticated = computed(() => isLoggedIn.value)

  const login = async (credentials) => {
    await new Promise((resolve) => setTimeout(resolve, 2000))

    if (credentials.email === 'admin' && credentials.password === 'admin') {
      isLoggedIn.value = true; user.value = { name: 'admin' }; return true;
    }
    return false
  }
  
  return { isLoggedIn, user, isAuthenticated, logout, login, }
})
