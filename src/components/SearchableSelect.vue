<template>
  <div class="searchable-select">
    <label class="block text-sm font-semibold text-gray-700 mb-2">
      {{ label }}
    </label>
    <div class="relative" v-click-outside="closeDropdown">
      <div
        @click="toggleDropdown"
        :class="[
          'w-full px-4 py-3 bg-white border-2 rounded-lg cursor-pointer transition-all duration-200',
          disabled ? 'bg-gray-100 cursor-not-allowed opacity-60' : 'hover:border-blue-400',
          isOpen ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-300'
        ]"
      >
        <div class="flex items-center justify-between">
          <span :class="[
            'truncate',
            selectedLabel ? 'text-gray-800' : 'text-gray-400'
          ]">
            {{ selectedLabel || placeholder }}
          </span>
          <svg
            class="w-5 h-5 text-gray-400 transition-transform duration-200"
            :class="{ 'rotate-180': isOpen }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      <div
        v-if="isOpen && !disabled"
        class="absolute z-50 w-full mt-2 bg-white border-2 border-blue-300 rounded-lg shadow-2xl overflow-hidden"
      >
        <div class="p-3 border-b border-gray-200 bg-gray-50">
          <div class="relative">
            <input
              ref="searchInput"
              v-model="searchQuery"
              type="text"
              placeholder="Search..."
              class="w-full px-4 py-2 pl-10 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200"
            />
            <svg
              class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        <div class="max-h-64 overflow-y-auto custom-scrollbar">
          <div
            v-for="option in filteredOptions"
            :key="option.value"
            @click="selectOption(option)"
            :class="[
              'px-4 py-3 cursor-pointer transition-all duration-150',
              modelValue === option.value
                ? 'bg-blue-500 text-white font-medium'
                : 'hover:bg-blue-50 text-gray-700'
            ]"
          >
            {{ option.label }}
          </div>

          <div
            v-if="filteredOptions.length === 0"
            class="px-4 py-8 text-center text-gray-500"
          >
            No results found
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue';

const props = defineProps({
  label: String,
  options: {
    type: Array,
    default: () => []
  },
  modelValue: String,
  placeholder: {
    type: String,
    default: 'Select an option'
  },
  disabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);
const searchQuery = ref('');
const searchInput = ref(null);

const selectedLabel = computed(() => {
  const selected = props.options.find(opt => opt.value === props.modelValue);
  return selected ? selected.label : '';
});

const filteredOptions = computed(() => {
  if (!searchQuery.value) {
    return props.options;
  }
  const query = searchQuery.value.toLowerCase();
  return props.options.filter(option =>
    option.label.toLowerCase().includes(query)
  );
});

function toggleDropdown() {
  if (props.disabled) return;
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    nextTick(() => {
      searchInput.value?.focus();
    });
  }
}

function closeDropdown() {
  isOpen.value = false;
  searchQuery.value = '';
}

function selectOption(option) {
  emit('update:modelValue', option.value);
  closeDropdown();
}

watch(() => props.modelValue, () => {
  searchQuery.value = '';
});

const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value();
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  }
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}
</style>
