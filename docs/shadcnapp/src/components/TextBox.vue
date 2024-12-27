<script setup>
import { defineProps } from "vue";

import Input from "./ui/input/Input.vue";
import { Label } from "./ui/label";

defineProps({ modelValue: {}, label: {}, id: {}, placeholder: {}, type: {}, error: {}, });
</script>

<template>
  <div>
    <Label :for="id">{{ label }}</Label>
    <Input :type="type" :id="id" :placeholder="placeholder" :class="{ 'border-[#ff0000]': error }"
      @input="$emit('update:modelValue', $event.target.value)" />
    <span v-if="error" class="text-[#ff0000]">{{ error }}</span>
  </div>
</template>