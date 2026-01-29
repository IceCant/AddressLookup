<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50">
    <!-- Header -->
    <div
        class="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-blue-600 to-cyan-500 text-white py-4 sm:py-6 px-4 shadow-lg"
    >

    <div class="max-w-4xl mx-auto flex items-center justify-between">

        <h1 class="text-2xl sm:text-4xl font-bold text-center sm:text-left">
          Khmer Address Lookup
        </h1>

        <button
            @click="clearAll"
            class="px-5 py-2.5 bg-red-500 hover:bg-red-600 text-white rounded-lg flex items-center gap-2"
        >
          ✖
        </button>


      </div>
    </div>


    <!-- Main Content -->
    <div class="max-w-4xl mx-auto px-4 pt-28 pb-20">

    <div class="bg-white rounded-2xl shadow-xl p-8">

        <!-- Searchable Dropdowns -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Province -->
          <SearchableSelect
              label="ក្រុង / ខេត្ត"
              :options="provinceOptions"
              v-model="selectedProvince"
              @update:modelValue="onProvinceChange"
              placeholder="Select Province"
          />

          <!-- District -->
          <SearchableSelect
              label="ខណ្ឌ / ស្រុក"
              :options="districtOptions"
              v-model="selectedDistrict"
              @update:modelValue="onDistrictChange"
              placeholder="Select District"
              :disabled="!selectedProvince"
          />

          <!-- Commune -->
          <SearchableSelect
              label="សង្កាត់ / ឃុំ"
              :options="communeOptions"
              v-model="selectedCommune"
              @update:modelValue="onCommuneChange"
              placeholder="Select Commune"
              :disabled="!selectedDistrict"
          />

          <!-- Village -->
          <SearchableSelect
              label="ភូមិ"
              :options="villageOptions"
              v-model="selectedVillage"
              @update:modelValue="onVillageChange"
              placeholder="Select Village"
              :disabled="!selectedCommune"
          />
        </div>

        <!-- Results Section -->
        <div v-if="addressKhmer || addressEnglish" class="mt-8 space-y-4">
          <div class="h-px bg-gradient-to-r from-transparent via-gray-300 to-transparent"></div>

          <h3 class="text-xl font-semibold text-gray-800 mb-4">Generated Address</h3>

          <!-- Khmer Address -->
          <div
              class="bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg p-4 border border-blue-200">
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-600 mb-1">Khmer</p>
                <p class="text-lg text-gray-800 font-khmer">{{ addressKhmer }}</p>
              </div>
              <button
                  @click="copyKhmerToClipboard"
                  class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5 flex items-center gap-2 flex-shrink-0"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
                Copy
              </button>
            </div>
          </div>
          <div class="h-2"></div>
          <!-- English Address -->
          <div
              class="bg-gradient-to-r from-cyan-50 to-blue-50 rounded-lg p-4 border border-cyan-200">
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-600 mb-1">English</p>
                <p class="text-lg text-gray-800">{{ addressEnglish }}</p>
              </div>
              <button
                  @click="copyEnglishToClipboard"
                  class="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white font-medium rounded-lg transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5 flex items-center gap-2 flex-shrink-0"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
                Copy
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <footer
        class="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur border-t border-gray-200 text-center py-2 z-40"
    >
      <p class="text-sm text-gray-600">
        Created by <span class="font-semibold">Ear Techboung</span>
      </p>
    </footer>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from "vue";
import locationsJson from "@/assets/address.json";
import SearchableSelect from "./SearchableSelect.vue";

const locations = ref({});
const selectedProvince = ref("");
const selectedDistrict = ref("");
const selectedCommune = ref("");
const selectedVillage = ref("");
let addressKhmer = ref("");
let addressEnglish = ref("");

onMounted(() => {
  locations.value = locationsJson;
});

const provinceCodes = computed(() => Object.keys(locations.value));

const provinceOptions = computed(() => {
  return provinceCodes.value.map(code => ({
    value: code,
    label: `${locations.value[code].name_kh} / ${locations.value[code].name_en}`
  }));
});

const currentDistricts = computed(() => {
  if (!selectedProvince.value) return {};
  return locations.value[selectedProvince.value].districts || {};
});
const districtCodes = computed(() => Object.keys(currentDistricts.value));

const districtOptions = computed(() => {
  return districtCodes.value.map(code => ({
    value: code,
    label: `${currentDistricts.value[code].name_kh} / ${currentDistricts.value[code].name_en}`
  }));
});

const currentCommunes = computed(() => {
  if (!selectedDistrict.value) return {};
  return currentDistricts.value[selectedDistrict.value].communes || {};
});
const communeCodes = computed(() => Object.keys(currentCommunes.value));

const communeOptions = computed(() => {
  return communeCodes.value.map(code => ({
    value: code,
    label: `${currentCommunes.value[code].name_kh} / ${currentCommunes.value[code].name_en}`
  }));
});

const currentVillages = computed(() => {
  if (!selectedCommune.value) return {};
  return currentCommunes.value[selectedCommune.value].villages || {};
});
const villageCodes = computed(() => Object.keys(currentVillages.value));

const villageOptions = computed(() => {
  return villageCodes.value.map(code => ({
    value: code,
    label: `${currentVillages.value[code].name_kh} / ${currentVillages.value[code].name_en}`
  }));
});

function onProvinceChange() {
  selectedDistrict.value = "";
  selectedCommune.value = "";
  selectedVillage.value = "";
  addressKhmer.value = "";
  addressEnglish.value = "";
}

function onDistrictChange() {
  selectedCommune.value = "";
  selectedVillage.value = "";
  addressKhmer.value = "";
  addressEnglish.value = "";
}

function onCommuneChange() {
  selectedVillage.value = "";
  addressKhmer.value = "";
  addressEnglish.value = "";
}

function onVillageChange() {
  if (parseInt(selectedProvince.value) === 12) {
    addressKhmer.value = `ភូមិ${currentVillages.value[selectedVillage.value].name_kh} សង្កាត់${currentCommunes.value[selectedCommune.value].name_kh} ខណ្ឌ${currentDistricts.value[selectedDistrict.value].name_kh} ${locations.value[selectedProvince.value].name_kh}`;
    addressEnglish.value = `${currentVillages.value[selectedVillage.value].name_en} Village, Sangkat ${currentCommunes.value[selectedCommune.value].name_en}, Khan ${currentDistricts.value[selectedDistrict.value].name_en}, ${locations.value[selectedProvince.value].name_en} City`;
  } else {
    addressKhmer.value = `ភូមិ${currentVillages.value[selectedVillage.value].name_kh} ឃុំ${currentCommunes.value[selectedCommune.value].name_kh} ស្រុក${currentDistricts.value[selectedDistrict.value].name_kh} ខេត្ត${locations.value[selectedProvince.value].name_kh}`;
    addressEnglish.value = `${currentVillages.value[selectedVillage.value].name_en} Village, ${currentCommunes.value[selectedCommune.value].name_en} Commune, ${currentDistricts.value[selectedDistrict.value].name_en} District, ${locations.value[selectedProvince.value].name_en} Province`;
  }
}

function copyEnglishToClipboard() {
  navigator.clipboard.writeText(addressEnglish.value)
      .then(() => {
        showNotification("English address copied!");
      })
      .catch(err => alert("Failed to copy"));
}

function copyKhmerToClipboard() {
  navigator.clipboard.writeText(addressKhmer.value)
      .then(() => {
        showNotification("Khmer address copied!");
      })
      .catch(err => alert("Failed to copy"));
}

function clearAll() {
  selectedProvince.value = "";
  selectedDistrict.value = "";
  selectedCommune.value = "";
  selectedVillage.value = "";
  addressKhmer.value = "";
  addressEnglish.value = "";
}

function showNotification(message) {
  const notification = document.createElement('div');
  notification.textContent = message;
  notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in';
  document.body.appendChild(notification);
  setTimeout(() => {
    notification.classList.add('animate-fade-out');
    setTimeout(() => notification.remove(), 300);
  }, 2000);
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-out {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}

.animate-fade-out {
  animation: fade-out 0.3s ease-out;
}
</style>
