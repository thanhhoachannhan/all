<template>
  <div class="mb-[15px] flex flex-col">
    <label :for="id" class="mb-[5px] font-bold text-left">{{ label }}</label>
    <input
      :type="type"
      :id="id"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :placeholder="placeholder"
      class="p-[5px] text-[1rem] border border-solid border-[#333] rounded-[4px]"
      :class="{ 'border-[#ff0000]': error }"
    />
    <span v-if="error" class="text-[#ff0000] text-[0.875rem] mt-[5px]">{{ error }}</span>
  </div>
</template>
  
<script setup>
import { defineProps } from "vue";

// Define props for reusability
defineProps({
  modelValue: { type: String, required: true, },
  label: { type: String, required: true, },
  id: { type: String, required: true, },
  placeholder: { type: String, default: "", },
  type: { type: String, default: "text", },
  error: { type: String, default: "", },
});
</script>