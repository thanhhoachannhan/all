<template>
  <div class="max-w-[600px] m-auto p-[5px] text-center">
    <div v-if="isLoading" class="flex justify-center items-center h-screen"> loading </div>
    <div v-else>
      <h1>Welcome, {{ username }}!</h1>
      <Table v-if="!error">
        <TableHeader>
          <TableRow>
            <TableHead class="w-[100px]"> Data </TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Method</TableHead>
            <TableHead class="text-right"> Amount </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="(invoice, index) in data" :key="index">
            <TableCell class="font-medium"> {{ invoice.invoice }} </TableCell>
            <TableCell>{{ invoice.paymentStatus }}</TableCell>
            <TableCell>{{ invoice.paymentMethod }}</TableCell>
            <TableCell class="text-right"> {{ invoice.totalAmount }} </TableCell>
          </TableRow>
        </TableBody>
      </Table>
      <p v-else class="text-red-500 text-[1.2rem] mt-2.5">{{ error }}</p>
      <Button variant="destructive" @click="handleLogout">Logout</Button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

const authStore = useAuthStore()
const router = useRouter()
const username = authStore.user?.name || 'Guest User'
const data = ref([])
const isLoading = ref(true)
const error = ref('')

// Simulated API call
const fetchNames = async () => {
  isLoading.value = true
  error.value = ''
  try {
    // Simulate API latency
    await new Promise((resolve) => setTimeout(resolve, 1000))
    // Simulate response
    const response = [
      { invoice: 'INV001', paymentStatus: 'Paid', totalAmount: '$250.00', paymentMethod: 'Credit Card', },
      { invoice: 'INV002', paymentStatus: 'Pending', totalAmount: '$150.00', paymentMethod: 'PayPal', },
    ]
    data.value = response
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
